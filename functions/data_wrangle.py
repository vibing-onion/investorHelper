import pandas as pd

def historical_10Q_dw(df) -> dict:
    if df.empty:
        return df
    df[['fileDate', 'endDate']] = df[['fileDate', 'endDate']].apply(pd.to_datetime)
    df = df.sort_values(by=['fileDate', 'endDate'])
    df = df.drop_duplicates(subset='fileDate', keep='last')
    df.index = df['fyfp']
    return df['val'].to_dict()

def historical_10Q_merge(data):
    col_name = data.keys()
    data = (pd.concat([pd.Series(data[key]) for key in data.keys()], axis=1))
    data = data.fillna('--')
    data.columns = col_name
    data = data.sort_index()
    idx = data.index.astype(str)
    data.index = idx.str[:-1] + ' Q' + idx.str[-1]
    
    return data.to_dict(), list(data.index)