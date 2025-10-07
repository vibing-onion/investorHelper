from functions.helper.self_rate_limiter.rate_limiter import rate_limited_multiprocessing

import requests
import json
from dotenv import load_dotenv
import os

def getUsualTicker(feed):
    print(feed)
    cik = str(feed['cik'])
    headers = feed['headers']
    company_facts = requests.get(f"https://data.sec.gov/submissions/CIK{cik}.json", headers=headers).json()
    if len(company_facts["exchanges"]) > 0:
        exchange = company_facts["exchanges"][0]
    else:
        return None
    if exchange in ['Nasdaq', 'NYSE']:
        return {
            "cik": feed["cik"],
            "ticker": feed["ticker"],
            "company_name": feed["company_name"]
        }
    return None

def get_mapping():
    try:
        load_dotenv(os.path.join(os.getcwd(), '.env'))

        user_agent : str = os.getenv('USER_AGENT')
        setup_relative_dir : str = os.getenv('SETUP_DIR')
        setup_abs_dir = os.path.join(os.getcwd(), setup_relative_dir)
        headers = {
            'User-Agent': user_agent
        }

        url = "https://www.sec.gov/files/company_tickers.json"
        print("Load .env variables -- SUCCESS") 
    except:
        print("Error in loading environment variables, check .env file")
        return
    
    try:
        res = requests.get(url, headers=headers).json()
    except:
        print("Error in SEC API call, check API validity")
        return

    try:
        mapping = {
            val['ticker']: [
                str(val['cik_str']).zfill(10),
                val['title']
            ]
            for key, val in res.items()
        }
        print("Load CIK-Ticker Mapping -- start")
        usualTickers = (rate_limited_multiprocessing(getUsualTicker, [{'cik': str(val['cik_str']).zfill(10), 'ticker': val['ticker'], 'company_name': val['title'], 'headers': headers} for key, val in res.items()][:5]))
        
        print("CIK-Ticker Mapping creation -- SUCCESS")
    except:
        print("Error in mapping creation")
        return
    
    export_path = setup_abs_dir + '/ticker.json'
    if not os.path.exists(setup_abs_dir):
        os.makedirs(setup_abs_dir)
    
    try:
        if os.path.exists(export_path):
            os.chmod(export_path, 0o755)        
        with open(export_path, 'w') as f:
            json.dump(list(usualTickers), f)
            f.close()
        os.chmod(export_path, 0o444)
    except:
        print("Error in writing to mapping json")
        return