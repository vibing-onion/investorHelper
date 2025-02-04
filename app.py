#!/opt/homebrew/bin/python3.11

import sys
import os

dir = [
    'functions',
    'static'
]

for d in dir:
    sys.path.insert(0, os.getcwd() + d)

from flask import Flask, jsonify, render_template, request
from functions.api import initialize_api, search_cik_api, search_company_api, historical_10Q_api, search_sector_api
from functions.data_load import load_sector_api

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
    return render_template("searchCompany.html", message = {'heading': 'Company Search', 'action': '/search_company_result'})

@app.route("/search_company_result", methods= ['POST'])
def search_company_result():
    req = {key: value for key, value in request.form.items()}
    result = search_company_api(req['companyInput'], req['searchMethod'])
    if result['client_info'] is None or result['contact_info'] is None:
        return render_template("errorPage.html")
    return render_template("searchCompanyResult.html", client_info = result['client_info'], contact_info = result['contact_info'])

@app.route("/historical_10Q")
def historical_10Q():
    return render_template("searchCompany.html", message = {'heading': 'Historical 10Q', 'action': '/historical_10Q_result'})

@app.route("/historical_10Q_result", methods= ['POST'])
def historical_10Q_result():
    req = {key: value for key, value in request.form.items()}
    result = historical_10Q_api(req['companyInput'], req['searchMethod'])
    return render_template("historical_10Q_result.html", data = result, len = len(result['time']))

@app.route("/load", methods=['POST'])
def load():
    req = {key: value for key, value in request.form.items()}
    print(req)
    if req['loadData'] == "sectordata":
        return render_template("loadPage.html", result = load_sector_api(), return_url = '/sector_search')
    else:
        return render_template("errorPage.html")

@app.route("/sector_search", methods=['GET', 'POST'])
def sector_search():
    if request.method == 'POST':
        req = {key: value for key, value in request.form.items()}
        api_res = search_sector_api(req['sicInput'])
    else:
        api_res = search_sector_api()
    return render_template("sectorSearch.html", message = "Sector Search", 
                           category = api_res['opt'], result = api_res['res'], res_display = api_res['res_display'])

if __name__ == '__main__':
    initialize_api()
    app.run(debug=True, use_reloader=False)