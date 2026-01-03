import pandas as pd
from dotenv import load_dotenv
import os
from fredapi import Fred

load_dotenv(os.path.join(os.getcwd(), 'backend', '.env'))

api_key : str = os.getenv('FRED_API_KEY')
fred = Fred(api_key=api_key)

def third_party_api(dataCategory, dataName):
    try:
        # FRED API
        if dataCategory == 'FRED':
            return fred.get_series(dataName).to_json(orient='split')
        
        # UNKNOWN API
        else:
            print("API not found. Please report to the development team.")
            return None
        
    except:
        print("Error in calling third party api. Please report to the development team.")
        return None