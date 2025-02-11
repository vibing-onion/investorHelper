import json
import numpy as np
import multiprocessing
import time
import yfinance as yf
from functions.tenQ_report import get_company_info_by_CIK

def sub_task_load_sector_api(comp_list):
    result = [get_company_info_by_CIK(cik) for cik in comp_list]
    return [comp['client_info'] for comp in result if comp['client_info'] is not None and 'client_info' in comp.keys()]

def load_sector_api():
    try:
        with open('functions/data/cik_mapping.json', 'r') as f:
            comp = json.load(f)
            f.close()
        
        comp_list = ['CIK' + comp[ticker][0] for ticker in comp.keys() if len(comp[ticker]) == 2]
        cpu_count = multiprocessing.cpu_count()
        sub_task_size = len(comp_list) // cpu_count
        
        with multiprocessing.Pool(cpu_count) as p:
            result = p.map(sub_task_load_sector_api, [comp_list[sub_task_size*i:sub_task_size*(i+1)] for i in range(cpu_count)])
        result = np.concatenate(result).tolist()
        
        with open('functions/data/sector_mapping.json', 'w') as f:
            json.dump(result, f)
            f.close()
        return "Success"
        
    except:
        print("Error in loading sector_mapping.json, check directory.")
        return "Failure"
    
def sample_data_load():
    try:
        data = yf.download('^SPX COST', start = '2023-01-01', end='2024-12-31')['Close']
        data.index = data.index.strftime('%Y-%m-%d')
        data['Time'] = data.index
        data.columns = ['SPX', 'NASDAQ', 'Time']
        for c in data.columns[:-1]:
            data[c] = data[c]/data[c][0]
        data = data.values.tolist()
        
        return data
    except:
        print("Error in loading sample data. Please report to the development team.")
        return {}