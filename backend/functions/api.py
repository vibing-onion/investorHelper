from functions.data_load import sample_data_load, sector_data_load
from functions.edgardata import getStatements

def sample_data_api():
    return sample_data_load()

def ticker_list_api():
    return ticker_list

def sector_data_api():
    return sector_data_load()