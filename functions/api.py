from functions.tenQ_report import get_ticker_cik_mapping, get_company_info_by_CIK, get_company_info_by_ticker, get_10Q_report_by_CIK, get_10Q_report_by_ticker
from functions.cik_mapping import get_mapping

def initialize_api():
    print("Initializing data...")
    get_mapping()
    print("Data initialization -- SUCCESS")

def search_cik_api(ticker):
    cik_mapping = get_ticker_cik_mapping([ticker])
    if cik_mapping["ticker"] is None:
        return {str(ticker):"The above ticker is invalid."}
    return cik_mapping

def search_company_api(company, search_method):
    if search_method == "CIK number":
        company_info = get_company_info_by_CIK(company)
    else:
        company_info = get_company_info_by_ticker(company)
    return company_info

def historical_10Q_api(company, search_method):
    if search_method == "CIK number":
        historical_10Q = get_10Q_report_by_CIK(company)
    else:
        historical_10Q = get_10Q_report_by_ticker(company)
    return historical_10Q