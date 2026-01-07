import sys
import os

dir = [
    'functions',
]
[sys.path.insert(0, os.getcwd() + d) for d in dir]

from flask import Flask, jsonify
from flask_cors import CORS
from functions.api import sample_data_api, ticker_list_api, sic_info_api, dashboard_data_api, sector_data_api, fin_report_api

from setup.mainSetup import masterSetup

# Create Flask app
app = Flask(__name__)
CORS(app)

# API endpoint
@app.route('/api/v1/test', methods=['GET'])
def testapi():
    return jsonify({'message': 'Hello from Flask!'})

@app.route("/api/v1/sampleData", methods=["GET"])
def home():
    return jsonify(sample_data_api())

@app.route("/api/v1/dashboardData/<string:dataCategory>/<string:dataName>/<string:BATCH_RETRIEVE>", methods=["GET"])
def getDashboardData(dataCategory, dataName, BATCH_RETRIEVE):
    return jsonify(dashboard_data_api(dataCategory, dataName, True)) if BATCH_RETRIEVE == 'True' else jsonify(dashboard_data_api(dataCategory, dataName))

@app.route("/api/v1/companySectorList", methods=["GET"])
def getCompanySectorList():
    return jsonify(sector_data_api())

@app.route("/api/v1/companyInfo/", methods=["GET"])
def companyInfoDefault():
    return jsonify(sic_info_api())

@app.route("/api/v1/companyInfo/<string:ticker>/", methods=["GET"])
def companyInfoSpecific(ticker):
    return jsonify(fin_report_api(ticker))

@app.route("/api/v1/companyData/<string:dataCategory>/<string:ticker>/", methods=["POST"])
def companyInfo(dataCategory, ticker):
    return jsonify(sample_data_api())

if __name__ == '__main__':
    # masterSetup()
    app.run(host='0.0.0.0', port=5000, debug=True)