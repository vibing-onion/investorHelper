import requests
import json
from dotenv import load_dotenv
import os


def get_mapping():
    try:
        load_dotenv('functions/.env')

        user_agent : str = os.getenv('USER_AGENT')
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
        print("CIK-Ticker Mapping creation -- SUCCESS")
    except:
        print("Error in mapping creation")
        return
    
    export_path = 'functions/data/cik_mapping.json'
    
    try:
        os.chmod(export_path, 0o755)
        with open(export_path, 'w') as f:
            json.dump(mapping, f)
            f.close()
        os.chmod(export_path, 0o444)
    except:
        print("Error in writing to mapping json")
        return