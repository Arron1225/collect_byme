import requests
import csv
import pandas as pd
import time
from bs4 import BeautifulSoup
import os
import glob

# response  = requests.get("https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL")
# if response.status_code == 200:
#     print("success")
# else:
#     print("請求失敗",response.status_code) 
# data = pd.DataFrame.from_dict(response.json(),orient='columns')

# print(data)
"/Users/arron/Desktop/collect_data"
a= glob.glob(r' Users/arron/Desktop/collect_data/test/*')
print(a)
print(os.getcwd())
dir=os.getcwd()
filename = 'tt.txt'
if os.path.exists('/log/'+filename):
    print("True")
else:
    with open('log/'+filename,'a') as file:
        file.write('hello')
        file.writelines('\n')
    print("false")    