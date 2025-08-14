import requests
import pandas as pd
import datetime
import time

def date_to_sec(date):
    return int(datetime.datetime.strptime(date, "%Y-%m-%d").timestamp())

def yf_download_alt(ticker, start, end, column = ['Close']):
    try:
        start_in_sec, end_in_sec = date_to_sec(start), date_to_sec(end)
        url = f"https://query2.finance.yahoo.com/v8/finance/chart/{ticker}?period1={start_in_sec}&period2={end_in_sec}&interval=1d"
        res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        
        res_json = res.json()
        data = res_json['chart']['result'][0]['indicators']['quote'][0]
        df = pd.DataFrame(
            {'timestamp': res_json['chart']['result'][0]['timestamp'], 'Close': data['close'], 'Open': data['open'], 'High': data['high'], 'Low': data['low'], 'Volume': data['volume']})
        df['Time'] = pd.to_datetime(df['timestamp'], unit='s')
        df['Date'] = df['Time'].apply(lambda x: x.strftime('%Y-%m-%d'))
        df.index = df['Date']

        print(f"Downloaded {ticker} from {start} to {end}")
        return df[column]
    
    except:
        print(f"Error downloading {ticker} from {start} to {end}")
        return pd.DataFrame([])