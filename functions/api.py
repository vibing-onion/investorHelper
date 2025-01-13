from functions.tenQ_report import get_ticker_cik_mapping
from functions.cik_mapping import get_mapping

def initialize():
    print("Initializing data...")
    get_mapping()
    print("Data initialization -- SUCCESS")

def search_cik(ticker):
    cik_mapping = get_ticker_cik_mapping([ticker])
    return cik_mapping