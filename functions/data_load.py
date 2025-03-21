import json
import pandas as pd
import numpy as np
import multiprocessing
import time
import yfinance as yf
from functions.helper.alt_yfinance.download import yf_download_alt
from functions.tenQ_report import get_company_info_by_CIK
from functions.helper.self_rate_limiter.rate_limiter import rate_limited_multiprocessing

def sub_task_load_sector_api(comp_list):
    result = [get_company_info_by_CIK(cik) for cik in comp_list]
    return [comp['client_info'] for comp in result if comp['client_info'] is not None and 'client_info' in comp.keys()]

def load_sector_api():
    try:
        with open('functions/data/cik_mapping.json', 'r') as f:
            comp = json.load(f)
            f.close()
        
        comp_list = ['CIK' + comp[ticker][0] for ticker in comp.keys() if len(comp[ticker]) == 2]
        result = rate_limited_multiprocessing(get_company_info_by_CIK, comp_list, rate_limit_per_second=10)
        result = [comp['client_info'] for comp in result if comp['client_info'] is not None and 'client_info' in comp.keys()]
        
        with open('functions/data/sector_mapping.json', 'w') as f:
            json.dump(result, f)
            f.close()
        return "Success"
        
    except:
        print("Error in loading sector_mapping.json, check directory.")
        return "Failure"
    
def sample_data_load():
    try:
        data = pd.merge(
                    yf_download_alt('^SPX', start = '2023-01-01', end='2024-12-31'),
                    yf_download_alt('COST', start = '2023-01-01', end='2024-12-31'),
                    on='Date', suffixes=('SPX', 'COST')
                )
        data['Time'] = data.index
        data.columns = ['SPX', 'COST', 'Time']
        for c in data.columns[:-1]:
            data[c] = data[c]/data[c][0]
        data = data.values.tolist()
        
        return data
    except:
        print("Error in loading sample data. Please report to the development team.")
        return {}