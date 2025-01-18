import sys
import os

dir = [
    'functions',
    'static'
]

for d in dir:
    sys.path.insert(0, os.getcwd() + d)

from flask import Flask, jsonify, render_template, request
from functions.api import initialize_api, search_cik_api, search_company_api

app = Flask(__name__, static_folder = "static")

@app.route("/")
def home():
    return render_template("index.html", message = "Investor Helper")

@app.route("/search_cik")
def search_cik():
    return render_template("searchCIK.html", message = "CIK Lookup")

@app.route("/search_cik_result", methods= ['POST'])
def search_cik_result():
    req = {key: value for key, value in request.form.items()}
    result = search_cik_api(req['tickerInput'])
    return render_template("searchCIKresult.html", title = [key for key in result.keys()][0], cik = [val for val in result.values()][0])

@app.route("/search_company")
def search_company():
    return render_template("searchCompany.html", message = "Company Search")

@app.route("/search_company_result", methods= ['POST'])
def search_company_result():
    req = {key: value for key, value in request.form.items()}
    result = search_company_api(req['companyInput'], req['searchMethod'])
    if result['client_info'] is None or result['contact_info'] is None:
        return render_template("errorPage.html")
    return render_template("searchCompanyResult.html", client_info = result['client_info'], contact_info = result['contact_info'])

if __name__ == '__main__':
    initialize_api()
    app.run(debug=True, use_reloader=False)