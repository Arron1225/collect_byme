import requests
import csv
import pandas as pd
import time
import numpy as np
from bs4 import BeautifulSoup
from datetime import date
import datetime 
import os

import glob

# response  = requests.get("https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL")
# if response.status_code == 200:
#     print("success")
# else:
#     print("請求失敗",response.status_code) 
# data = pd.DataFrame.from_dict(response.json(),orient='columns')
# data.to_csv('test.csv')
# print(data)
# "/Users/arron/Desktop/collect_data"
# a= glob.glob(r' Users/arron/Desktop/collect_data/test/*')
# print(os.getcwd())
# dir=os.getcwd()
# filename = 'tt.txt'
# if os.path.exists('/log/'+filename):
#     print("True")
# else:
#     with open('log/'+filename,'a') as file:
#         file.write('hello')
#         file.writelines('\n')
#     print("false") 
   

# print(code_list)    

# response =requests.get("https://www.twse.com.tw/rwd/zh/afterTrading/STOCK_DAY?date=20240414&stockNo=0051&response=html")



code_list =[]
df = pd.read_csv('test.csv')
print(df['Code'][0])
for i in range(df.shape[0]):
    code_list.append(df['Code'][i])
def convert_1d_to_2d(input_array, row, col):
    output_array = [[0 for j in range(col)] for i in range(row)]
    k = 0
    for i in range(row):
        for j in range(col):
            output_array[i][j] = input_array[k]
            k += 1
    return output_array
tmp_add=[]
final_list=[]
data_tmp =[]
headings = []
tonow = datetime.date.today()
get_date = str(tonow).replace("-","")
for i in range(5):
    url = f"https://www.twse.com.tw/rwd/zh/afterTrading/STOCK_DAY?date={get_date}&stockNo={code_list[i]}&response=html"
    response =requests.get(url)
    if response.status_code == 200:  
        soup = BeautifulSoup(response.content, "html.parser") 
        all_td = soup.find_all("td")
        for h in all_td:
            data_tmp.append(h.text.strip())
        
        for i in range(len(data_tmp)):
            tmp_add.append(data_tmp[i])
        final_list = convert_1d_to_2d(tmp_add, (int)(len(tmp_add)/9), 9)
    else:
        print(response.request)
com_table = pd.DataFrame(data=final_list)
com_table.to_csv("ttest.csv")










# for item in soup.find_all("th"):
#     item = (item.text).rstrip("\n")
#     headings.append(item)
# del headings[0]
# com_table = pd.DataFrame(data=final_list,columns=headings)
# print(com_table)