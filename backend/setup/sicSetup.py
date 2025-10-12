from dotenv import load_dotenv
from functions.helper.self_rate_limiter.rate_limiter import rate_limited_multiprocessing
import requests
import os
import json
    
def get_company_info_by_CIK(cik) -> dict:
    
    try:
        load_dotenv(os.path.join(os.getcwd(), '.env'))

        user_agent : str = os.getenv('USER_AGENT')
        setup_relative_dir : str = os.getenv('SETUP_DIR')
        setup_abs_dir = os.path.join(os.getcwd(), setup_relative_dir)
        export_path = os.path.join(setup_abs_dir, 'compInfo.json')
        headers = {
            'User-Agent': user_agent
        }
        print("Load .env variables -- SUCCESS")
        
    except:
        print("Error in loading environment variables, check .env file")
        return {"client_info": None, "contact_info": None}
    
    try:
        res = requests.get(f"https://data.sec.gov/submissions/CIK{cik['cik']}.json", headers=headers).json()
        client_info = {key: res[key] for key in [
            "cik", "name", "sic", "sicDescription", "ownerOrg"
        ]}
        for key in ["tickers", "exchanges"]:
            client_info[key] = ", ".join(list(set(res[key])))
        contact_info = {
            "mailing_address" : res['addresses']['mailing'],
            "phone" : res['phone']
        }
        with open(os.path.join(setup_abs_dir, 'countrycode_mapping.json'), 'r') as f:
            countrycode = json.load(f)
            f.close()
        contact_info["mailing_address"]["Country_Region"] = countrycode[contact_info["mailing_address"]["stateOrCountry"]]
        
        return {"client_info": client_info, "contact_info": contact_info}
    except:
        print("Error in SEC API call, check API validity")
        return {"client_info": None, "contact_info": None}

def sub_task_load_compInfo_api(cik_list):
    result = [get_company_info_by_CIK(cik) for cik in cik_list]
    return [comp['client_info'] for comp in result if comp['client_info'] is not None and 'client_info' in comp.keys()]

def getSector():

    try:
        load_dotenv(os.path.join(os.getcwd(), '.env'))
        
        setup_relative_dir : str = os.getenv('SETUP_DIR')
        setup_abs_dir = os.path.join(os.getcwd(), setup_relative_dir)
        export_path_compInfo = os.path.join(setup_abs_dir, 'compInfo.json')
        export_path_sector = os.path.join(setup_abs_dir, 'sector_mapping.json')
        
        print("Load .env variables -- SUCCESS")
    except:
        print("Error in loading environment variables, check .env file")
        return
    
    try: 
        with open(os.path.join(setup_abs_dir,'ticker.json'), 'r') as f:
            comp_list = json.load(f)
            f.close()
        
        cik_list = [{'cik': comp['cik']} for comp in comp_list]
        compInfo = rate_limited_multiprocessing(get_company_info_by_CIK, cik_list, rate_limit_per_second=10)
        if os.path.exists(export_path_compInfo):
            os.chmod(export_path_compInfo, 0o755)
        
        with open(export_path_compInfo, 'w') as f:
            json.dump(compInfo, f)
            f.close()
        
        sector = [comp['client_info'] for comp in compInfo if 'client_info' in comp.keys() and comp['client_info'] is not None]
        if os.path.exists(export_path_sector):
            os.chmod(export_path_sector, 0o755)
        
        with open(export_path_sector, 'w') as f:
            json.dump(sector, f)
            f.close()
        
        print("Load sector_mapping.json -- SUCCESS")
        return
        
    except:
        print("Error in loading sector_mapping.json, check directory.")
        return