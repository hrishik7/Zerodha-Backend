import zipfile
import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler
import urllib.request
from urllib.request import Request, urlopen
from datetime import datetime
import time
from django.core.cache import cache


def extract_and_parse(filename):
    # read the dataset using the compression zip
    data = pd.read_csv(filename, compression='zip')
    # display dataset
    print("Data Loaded")
    return data


def download():
    url = 'https://www.bseindia.com/download/BhavCopy/Equity/EQ130421_CSV.ZIP'
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    filename = "data" + datetime.today().strftime("%Y-%m-%d") + '.zip'
    with urllib.request.urlopen(req) as dl_file:
        with open(filename, 'wb') as out_file:
            out_file.write(dl_file.read())
    return filename


def save_to_db(data):
    data = data[["SC_CODE" , "SC_NAME" , "OPEN" , "HIGH" , "LOW" , "CLOSE"]]
    data.columns = ['code' , 'name' , 'open' , 'high' , 'low' , 'close']
    print(data.head())
    data = data.to_dict('records')
    # from equity_data.models import EquityData
    # equity_data = []
    for i , row in enumerate(data):
        # equity_data.append(EquityData(code = row['SC_CODE'] , name = row['SC_NAME'] , open = row['OPEN'] , high = row['HIGH'] , low = row['LOW'] , close = row['CLOSE']))
        cache.set("STDATA:" + str(i) + ":" + row['name'] ,row )
    # EquityData.objects.bulk_create(equity_data)

def download_and_save_equity_from_site():
    filename = download()
    data = extract_and_parse(filename)
    save_to_db(data)


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(download_and_save_equity_from_site,
                      'cron', hour=18 , minute=0 )
    scheduler.start()