import pandas as pd
import json
from functions.helper.alt_yfinance.download import yf_download_alt

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

def sic_info_load():
    try:
        with open('data/sector_mapping.json', 'r') as f:
            sic_data = json.load(f)
            f.close()
        return sic_data
    except:
        print("Error in loading sector data. Please report to the development team.")
        return {}