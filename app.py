import sys
import os

dir = [
    'functions',
    'static'
]

for d in dir:
    sys.path.insert(0, os.getcwd() + d)

from flask import Flask, jsonify, render_template, request
from functions.api import initialize, search_cik

app = Flask(__name__, static_folder = "static")

@app.route("/")
def home():
    return render_template("index.html", message = "Investor Helper")

@app.route("/search_cik")
def search_cik_default():
    return render_template("searchCIK.html", message = "CIK Lookup")

@app.route("/search_cik_result", methods= ['POST'])
def search_cik_result():
    req = {key: value for key, value in request.form.items()}
    result = search_cik(req['tickerInput'])
    return render_template("searchCIKresult.html", title = [key for key in result.keys()][0], cik = [val for val in result.values()][0])

if __name__ == '__main__':
    initialize()
    app.run(debug=True, use_reloader=False)