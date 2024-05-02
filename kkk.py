import requests
import csv
import pandas as pd
import time
import numpy as np
from bs4 import BeautifulSoup
from datetime import date
from datetime import datetime
# import datetime 
import os
# tmp = ["113/03/12","113/03/111","113/03/111","113/02/11","113/02/11"]
# tt=[]
# for i in range(len(tmp)):
#     a=tmp[i] 
#     b=a.split('/')
#     year = b [0]
#     month = b [1]
#     day = b [2]
#     after_year = int(year)+1911
#     after_year = str(after_year)
#     a1 = '-'.join([after_year,month,day])
#     tmp[i]=a1
# print(tmp)


# first_column = df.pop('Name') 
# df.insert(0, 'Name', first_column) 

# data = {
#   "Brand": ["Ford", "Ford", "Ford"],
#   "Model": ["Sierra", "F-150", "Mustang"],
#   "Typ"  : ["2.0 GL", "Raptor", ["Mach-E", "Mach-1"]]
# }
# df = pd.DataFrame(data)
# newdf = df.explode('Typ')
# print(df)

# print(newdf)
# response  = requests.get("https://www.tpex.org.tw/openapi/v1/tpex_mainboard_quotes")
# if response.status_code == 200:
#     print("success")
# else:
#     print("請求失敗",response.status_code) 
# data = pd.DataFrame.from_dict(response.json(),orient='columns')
# data.to_csv('test_3.csv')
# df_1 = pd.read_csv('test3.csv')

# print(data)

# df_1 = pd.read_csv('test.csv')
# df_2 = pd.read_csv('test_1.csv')
# new_df  = pd.concat([df_1,df_2],axis=0,ignore_index=True)
# new_df.drop(['Unnamed: 0'], axis = 1,inplace=True)
# new_df.sort_values(by=['Code', 'Name'], ascending=True,inplace=True)

# print(new_df)
# new_df.to_csv('t.csv')
# tmp = []
# df_2 = pd.read_csv('test_1.csv')
# for i in range(len(df_2)):
#     tmp.append("2024-04-17")
# # print(tmp)
# df_2.insert(2,"Date",tmp,True)
# print(df_2)


# data = {
#     'Name': ['_0050_元大台灣50', '_005_元大台灣50', '_50_元大台灣50']
# }

# df = pd.DataFrame(data)
# df.to_csv('table.csv',index=False)

# df =  pd.read_csv('test.csv')
# print(df['Code'][0])
# string = "_0050_元大台灣50"

df = pd.read_csv('table.csv')
df['Name'] =df['Name'].str.split("_") 
for i in range(len(df)):
    print(df['Name'][i][1])
# print(df['Name'][1][1])
# print(type(t))
import os

# 指定目錄的路徑
# directory = './all_data'

# # 列出目錄中的所有文件和子目錄
# for filename in os.listdir(directory):
#     # 確保只處理檔案，而非子目錄
#     if os.path.isfile(os.path.join(directory, filename)):
#         # 假設你想要將檔案名稱中的 "old_" 替換為 "new_"
#         new_filename = filename.replace('old_', 'new_')
        
#         # 建立舊檔案和新檔案的完整路徑
#         old_filepath = os.path.join(directory, filename)
#         new_filepath = os.path.join(directory, new_filename)
        
#         # 執行更改名稱的動作
#         os.rename(old_filepath, new_filepath)
        
#         print(f"已將檔案名稱由 {filename} 更改為 {new_filename}")


# print("所有檔案名稱更新完成！")