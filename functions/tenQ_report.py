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
        return {"ticker": None}

    result = {"ticker": "CIK" + cik_mapping[ticker][0] for ticker in ticker_list if ticker in cik_mapping.keys()}
    if result == {}:
        return {"ticker": None}
    return result

def load_env(api: str = None, cik = None) -> dict:
    try:
        load_dotenv('functions/.env')

        user_agent : str = os.getenv('USER_AGENT')
        headers = {
            'User-Agent': user_agent
        }
        
        url = f"{api}{cik}.json"
        print("Load .env variables -- SUCCESS")
        return {"url": url, "headers": headers}
    except:
        print("Error in loading environment variables, check .env file")
        return {"url": None, "headers": None}

def get_company_info_by_CIK(cik) -> dict:
    
    env_var = load_env("https://data.sec.gov/submissions/", cik = cik)
    if env_var["url"] is None or env_var["headers"] is None:
        return {"client_info": None, "contact_info": None}
    
    try:
        res = requests.get(env_var["url"], headers=env_var["headers"]).json()
        client_info = {key: res[key] for key in [
            "cik", "name", "sic", "sicDescription", "ownerOrg"
        ]}
        for key in ["tickers", "exchanges"]:
            client_info[key] = ", ".join(list(set(res[key])))
        contact_info = {
            "mailing_address" : res['addresses']['mailing'],
            "phone" : res['phone']
        }
        with open('functions/data/countrycode_mapping.json', 'r') as f:
            countrycode = json.load(f)
            f.close()
        contact_info["mailing_address"]["Country_Region"] = countrycode[contact_info["mailing_address"]["stateOrCountry"]]
        
        return {"client_info": client_info, "contact_info": contact_info}
    except:
        print("Error in SEC API call, check API validity")
        return {"client_info": None, "contact_info": None}
    
def get_company_info_by_ticker(ticker) -> dict:
    cik_mapping = get_ticker_cik_mapping([ticker])
    if cik_mapping["ticker"] is None:
        return {"client_info": None, "contact_info": None}
    return get_company_info_by_CIK(cik_mapping["ticker"])

def get_latest_10Q_report(ticker):
    
    cik_mapping = get_ticker_cik_mapping([ticker])
    env_var = load_env(api = "https://data.sec.gov/api/xbrl/companyfacts/", cik = cik_mapping["ticker"])
    if env_var["url"] is None or env_var["headers"] is None:
        print("Error in loading environment variables, check .env file")
        return
    
    try:
        res = requests.get(env_var["url"], headers=env_var["headers"]).json()
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