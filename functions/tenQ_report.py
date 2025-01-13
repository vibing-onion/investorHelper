import requests
import json
from dotenv import load_dotenv
import os
import pandas as pd

def get_ticker_cik_mapping(ticker_list):
    try:
        with open('functions/data/cik_mapping.json', 'r') as f:
            cik_mapping = json.load(f)
            f.close()
    except:
        print("Error in loading cik_mapping.json, check directory")
        return

    return {ticker: "CIK" + cik_mapping[ticker][0] for ticker in ticker_list}

def get_latest_10Q_report(ticker):
    
    cik_mapping = get_ticker_cik_mapping([ticker])
    try:
        load_dotenv('functions/.env')

        user_agent : str = os.getenv('USER_AGENT')
        headers = {
            'User-Agent': user_agent
        }
        
        url = f"https://data.sec.gov/api/xbrl/companyfacts/{cik_mapping[ticker]}.json"
        print("Load .env variables -- SUCCESS") 
    except:
        print("Error in loading environment variables, check .env file")
        return
    
    try:
        res = requests.get(url, headers=headers).json()
        files = pd.DataFrame(res['facts']['dei']['EntityCommonStockSharesOutstanding']['units']['shares'])
        info = pd.DataFrame(res['facts']['us-gaap'].keys())
        ten_Q = files[files["form"] == '10-Q'].iloc[-1,:].loc[['val', 'accn', 'frame']]
    except:
        print("Error in SEC API call, check API validity")
        return

    with open('functions/data/10Q_report_keys.json', 'w') as f:
        json.dump(info.to_dict(), f)
        f.close()
    print(ten_Q)

    print("10Q report download -- SUCCESS")