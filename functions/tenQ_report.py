import requests
import json
from dotenv import load_dotenv
import os
import pandas as pd
from datetime import datetime

from functions.data_wrangle import historical_10Q_dw, historical_10Q_merge

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

def get_10Q_report_by_CIK(cik) -> dict:
    env_var = load_env(api = "https://data.sec.gov/api/xbrl/companyfacts/", cik = cik)
    if env_var["url"] is None or env_var["headers"] is None:
        print("Error in loading environment variables, check .env file")
        return {}
    
    try:
        res = requests.get(env_var["url"], headers=env_var["headers"]).json()
        data = res['facts']['us-gaap']
        metadata = {
            key: {
                "label": data[key]["label"],
                "description": data[key]["description"]
            }
            for key in data.keys()
        }
        result = {"metadata": metadata, "data": {}}
        for key in metadata.keys():
            for k in data[key]['units'].keys():
                record_list = [{'val': item['val'], 'fileDate': item['filed'], 'fyfp': str(item['fy']) + item['fp'][1], 'endDate': item['end']} for item in data[key]['units'][k] if item['form'] == "10-Q"]
            record_list = historical_10Q_dw(pd.DataFrame(record_list))
            if len(record_list) < 4:
                continue
            result["data"][key] = record_list
        result['data'], result['time'] = historical_10Q_merge(result['data'])
        
        print("10Q report loaded -- SUCCESS")
        return result
    
    except:
        print("Error in SEC API call, check API validity")
        return {}

def get_10Q_report_by_ticker(ticker) -> dict:
    cik_mapping = get_ticker_cik_mapping([ticker])
    if cik_mapping["ticker"] is None:
        return {}
    return get_10Q_report_by_CIK(cik_mapping["ticker"])