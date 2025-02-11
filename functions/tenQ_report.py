import requests
import json
from dotenv import load_dotenv
import os
import pandas as pd
from datetime import datetime
import time

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
    
    attempt = 0
    max_attempt = 3
    while attempt < max_attempt:
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
            
            time.sleep(0.3)
            return {"client_info": client_info, "contact_info": contact_info}
        except:
            attempt += 1
            time.sleep(0.5)
            if attempt == max_attempt:
                print("Error in SEC API call, check API validity")
                return {"client_info": None, "contact_info": None}
    
def get_company_info_by_ticker(ticker) -> dict:
    cik_mapping = get_ticker_cik_mapping([ticker])
    if cik_mapping["ticker"] is None:
        return {"client_info": None, "contact_info": None}
    return get_company_info_by_CIK(cik_mapping["ticker"])

def get_report_by_CIK(cik, reportType=["10-Q", "10-K"]) -> dict:
    env_var = load_env(api = "https://data.sec.gov/api/xbrl/companyfacts/", cik = cik)
    if env_var["url"] is None or env_var["headers"] is None:
        print("Error in loading environment variables, check .env file")
        return {}
    
    try:
        res = requests.get(env_var["url"], headers=env_var["headers"]).json()
        data = res['facts']['us-gaap']
        dei = res['facts']['dei'] if "dei" in res['facts'].keys() else None
        market_val = dei['EntityPublicFloat'] if dei is not None and "EntityPublicFloat" in dei.keys() else None
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
                record_list = [{'val': item['val'], 'fileDate': item['filed'], 'fyfp': str(item['fy']) + item['fp'][1], 'endDate': item['end']} for item in data[key]['units'][k] if item['form'] in reportType]
            record_list = historical_10Q_dw(pd.DataFrame(record_list))
            if len(record_list) < 4:
                continue
            result["data"][key] = record_list
        if market_val is not None:
            result['metadata']["EntityPublicFloat"] = {'label': market_val['label'], 'description': market_val["description"]}
            result['data']["EntityPublicFloat"] = historical_10Q_dw(
                pd.DataFrame([
                    {'val': item['val'], 'fileDate': item['filed'], 'fyfp': str(item['fy']) + str(4), 'endDate': item['end']} 
                    for item in market_val['units']['USD'] if item['form'] == '10-K'
                ])
            )
        result['data'], result['time'] = historical_10Q_merge(result['data'])
        
        print(f"{reportType} report loaded -- SUCCESS")
        return result
    
    except:
        print("Error in SEC API call, check API validity")
        return {}

def get_report_by_ticker(ticker, reportType="10-Q") -> dict:
    cik_mapping = get_ticker_cik_mapping([ticker])
    if cik_mapping["ticker"] is None:
        return {}
    return get_report_by_CIK(cik_mapping["ticker"], reportType=reportType)