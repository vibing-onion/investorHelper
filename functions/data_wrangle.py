import pandas as pd
import json
import os

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

def read_json(filepath):
    if os.path.isfile(filepath):
        with open(filepath, 'r') as f:
            data = json.load(f)
            f.close()
        return data
    
    return [{}]

def get_sector_options_results(filter_sector = "--", filepath = "functions/data/sector_mapping.json"):
    if not os.path.isfile(filepath):
        return {"opt" : [], "res" : [], "res_display" : "none", "ini_alert" : "inline-block"}
    
    try:
        filter_sector = filter_sector[0:3]
        data = pd.read_json(filepath)
        data['sic'] = data['sic'].str[:-1]
        d_opt = data.groupby('sic')['sicDescription'].apply(lambda x: ' | '.join(x.unique())).drop(['000',''])
        d_opt = pd.DataFrame([d_opt.index,d_opt]).T
        d_opt.columns = ['sic','sicDescription']
        
        return {
            "opt" : (d_opt['sic'] + '0 : ' + d_opt['sicDescription']).to_list(),
            "res" : data[data['sic'] == filter_sector][["tickers", "name", "cik", 'sic', 'sicDescription']].values.tolist(),
            "res_display" : "inline-block",
            "ini_alert" : "none"
            }
    except:
        print("Error in loading sectors.")
        return []