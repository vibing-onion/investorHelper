from functions.data_load import sample_data_load, sector_data_load
from functions.third_party_data import third_party_api
from functions.edgardata import getStatements

def sample_data_api():
    return sample_data_load()

def ticker_list_api():
    return ticker_list

def sector_data_api():
    return sector_data_load()

def dashboard_data_api(dataCategory, dataName, BATCH_RETRIEVE = False):
    thirdPartyData = ['FRED',]
    
    if BATCH_RETRIEVE:
        # Retrieve multiple data (same dataCategory & different dataName)
        if dataCategory in thirdPartyData:
            return {x: third_party_api(dataCategory, x) for x in dataName.split(',')}
    else:
        # Retrieve single data
        if dataCategory in thirdPartyData:
            return {dataName: third_party_api(dataCategory, dataName)}
        else:
            return None