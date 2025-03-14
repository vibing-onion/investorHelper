from functions.tenQ_report import get_ticker_cik_mapping, get_company_info_by_CIK, get_company_info_by_ticker, get_report_by_CIK, get_report_by_ticker
from functions.cik_mapping import get_mapping
from functions.data_wrangle import read_json, get_sector_options_results
from functions.data_load import sample_data_load

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
        historical_10Q = get_report_by_CIK(company)
    else:
        historical_10Q = get_report_by_ticker(company)
    return historical_10Q

def search_sector_api(filter_sector = "--"):
    return get_sector_options_results(filter_sector=filter_sector)

def sample_data_api():
    return sample_data_load()