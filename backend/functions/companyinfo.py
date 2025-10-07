# this file includes all features about company informations, including:
# ** 10-K | 10-Q
# ** peer companies

# for high level management of functions

from edgardata import getStatements

import pandas as pd

def getFundamentals(ticker):
    
    quarterly_data = {
        'income_statement': getStatements(ticker, form='10-Q', statement = 'income_statement').to_dict(),
        'balance_sheet': getStatements(ticker, form='10-Q', statement = 'balance_sheet').to_dict(),
        'cashflow_statement': getStatements(ticker, form='10-Q', statement = 'cashflow_statement').to_dict()
    }
    annual_data = {
        'income_statement': getStatements(ticker, form='10-K', statement = 'income_statement').to_dict(),
        'balance_sheet': getStatements(ticker, form='10-K', statement = 'balance_sheet').to_dict(),
        'cashflow_statement': getStatements(ticker, form='10-K', statement = 'cashflow_statement').to_dict()
    }
    
    return quarterly_data, annual_data

