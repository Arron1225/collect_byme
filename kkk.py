import requests
import csv
import pandas as pd
import time
from io import StringIO
import numpy as np
from bs4 import BeautifulSoup
from datetime import datetime, timedelta,date
import traceback
import numpy as np
from datetime import date
import pyodbc
# import pymssql
import struct
from io import StringIO
from sqlalchemy import create_engine,Table,Column,MetaData,String,text
from sqlalchemy.engine import URL
from sqlalchemy import create_engine
# import datetime 
import os
# # tmp = ["2024/03/12","2024/03/111","2024/03/111","2024/02/11","2024/02/11"]
# # tt=[]
# # for i in range(len(tmp)):
# #     a=tmp[i] 
# #     b=a.split('/')
# #     year = b [0]
# #     month = b [1]
# #     day = b [2]
# #     after_year = int(year)+1911
# #     after_year = str(after_year)
# #     a1 = '-'.join([after_year,month,day])
# #     tmp[i]=a1
# # print(tmp)
# def conver(input:str)-> str:
#     a = input
#     b = a.split('-')
#     y = b[0]
#     afy = int(y)-1911
#     afy = str(afy)
#     out = '/'.join([afy,b[1],b[2]])
#     return out
#     # print(out)

# # first_column = df.pop('Name') 
# # df.insert(0, 'Name', first_column) 

# # data = {
# #   "Brand": ["Ford", "Ford", "Ford"],
# #   "Model": ["Sierra", "F-150", "Mustang"],
# #   "Typ"  : ["2.0 GL", "Raptor", ["Mach-E", "Mach-1"]]
# # }
# # df = pd.DataFrame(data)
# # newdf = df.explode('Typ')
# # print(df)

# # print(newdf)
# # response  = requests.get("https://www.tpex.org.tw/openapi/v1/tpex_mainboard_quotes")
# # if response.status_code == 200:
# #     print("success")
# # else:
# #     print("請求失敗",response.status_code) 
# # data = pd.DataFrame.from_dict(response.json(),orient='columns')
# # data.to_csv('test_3.csv')
# # df_1 = pd.read_csv('test3.csv')

# # print(data)

# # df_1 = pd.read_csv('test.csv')
# # df_2 = pd.read_csv('test_1.csv')
# # new_df  = pd.concat([df_1,df_2],axis=0,ignore_index=True)
# # new_df.drop(['Unnamed: 0'], axis = 1,inplace=True)
# # new_df.sort_values(by=['Code', 'Name'], ascending=True,inplace=True)

# # print(new_df)
# # new_df.to_csv('t.csv')
# # tmp = []
# # df_2 = pd.read_csv('test_1.csv')
# # for i in range(len(df_2)):
# #     tmp.append("2024-04-17")
# # # print(tmp)
# # df_2.insert(2,"Date",tmp,True)
# # print(df_2)


# # data = {
# #     'Name': ['_0050_元大台灣50', '_005_元大台灣50', '_50_元大台灣50']
# # }

# # df = pd.DataFrame(data)
# # df.to_csv('table.csv',index=False)

# # df =  pd.read_csv('test.csv')
# # print(df['Code'][0])
# # string = "_0050_元大台灣50"

# # df = pd.read_csv('table.csv')
# # df['Name'] =df['Name'].str.split("_") 
# # for i in range(len(df)):
# #     print(df['Name'][i][1])
# # # print(df['Name'][1][1])
# # # print(type(t))
# # import os

# # 指定目錄的路徑
# # directory = './all_data'

# # # 列出目錄中的所有文件和子目錄
# # for filename in os.listdir(directory):
# #     # 確保只處理檔案，而非子目錄
# #     if os.path.isfile(os.path.join(directory, filename)):
# #         # 假設你想要將檔案名稱中的 "old_" 替換為 "new_"
# #         new_filename = filename.replace('old_', 'new_')
        
# #         # 建立舊檔案和新檔案的完整路徑
# #         old_filepath = os.path.join(directory, filename)
# #         new_filepath = os.path.join(directory, new_filename)
        
# #         # 執行更改名稱的動作
# #         os.rename(old_filepath, new_filepath)
        
# #         print(f"已將檔案名稱由 {filename} 更改為 {new_filename}")





# # 設定目標日期和時間（不包含時區資訊）
# # target_date = datetime.now().date()  # 目標日期為 2024-05-02
# # target_time = time(0, 0, 0)  # 目標時間為 00:00:00

# # # 設定目標時區為台北時區（UTC+8:00）
# # target_timezone = pytz.timezone('Asia/Taipei')

# # # 組合日期和時間，得到完整的目標日期時間
# # target_datetime = datetime.combine(target_date, target_time)

# # # 將目標日期時間設定為指定時區
# # target_datetime_with_timezone = target_timezone.localize(target_datetime)



# # print("目標日期時間（包含時區資訊）：", target_datetime_with_timezone)


# # # 起始日期
# # start_date = datetime(2024, 5, 1).date()
# # # 設定迴圈結束的日期
# # end_date = datetime(2024, 4, 25).date()
# # while start_date>= end_date:
# #     param = conver(str(start_date))
# #     link = f'http://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_download.php?l=zh-tw&d={param}&s=0,asc,0'

# #     # ddd = conver(str(start_date))
# #     # rw = f'dfada{ddd}'
# #     # print(rw)
# #     print(link)
# #     time.sleep(3)
# #     print(str(start_date))
# #     start_date -= timedelta(days=1)


# start_date = datetime(2024, 4, 24).date()

# end_date = datetime(2024, 4, 10).date()
# while start_date>= end_date:
#     param = conver(str(start_date))
#     try:
        
#         link = f'http://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_download.php?l=zh-tw&d={param}&s=0,asc,0'
#         r = requests.get(link)
#         lines = r.text.replace('\r', '').split('\n')
#         df = pd.read_csv(StringIO("\n".join(lines[3:])), header=None)
#         df.columns = list(map(lambda l: l.replace(' ',''), lines[2].split(',')))
#         df.index = df['代號']
#         df = df.drop(['代號'], axis=1)
#         # df.to_csv(str(start_date)+'.csv')
        
        
#         # df = pd.read_csv('test_tpex.csv')
#         df_cleaned = df.apply(lambda x: x.str.strip().replace('---', np.nan))
#         df_cleaned = df_cleaned.dropna(subset=['收盤','漲跌','開盤','最高'],axis=0, how='all')
#         # df_cleaned.to_csv('ok.csv')
#         # specific_date = date(2024, 4, 26)  
#         df_names = pd.read_csv('only_name_tpex.csv')
#         # 第二個 DataFrame：存放名字和其他資料
#         # df_names_addresses = pd.read_csv('ok.csv')
#         merged_df = pd.merge(df_cleaned, df_names, on='名稱', how='inner')
#         merged_df.drop(['最後買量(千股)','最後賣量(千股)','Unnamed: 0_y','Unnamed: 0_x'],axis=1,inplace=True)
#         # 新增日期欄位
#         merged_df = merged_df.assign(DataDate=start_date)
#         # 因為日期欄位會被創到最後一個，所以會將他移到第一個
#         last_column_name = merged_df.columns[-1]
#         # 將最後一欄移動到第一欄
#         merged_df = merged_df[[last_column_name] + [col for col in merged_df.columns if col != last_column_name]]
#         # 原本欄位名是中文，將他改名成英文
#         merged_df.rename(columns={'代號':'CompanyCode','名稱':'CompanyName','收盤':'Close','漲跌':'Change','開盤':'Open','最高':'High','最低':'Low','成交股數':'TradingShare','均價':'AveragePrice','成交金額(元)':'TransactionAmount','次日參考價':'NextReferencePrice','成交筆數':'TransactionNumber','發行股數':'Capitals','最後賣價':'LatesAskPrice','最後買價':'LatestBidPrice','次日漲停價':'NextLimitUp','次日跌停價':'NextLimitDown'},inplace=True)
#         merged_df['CompanyName']=merged_df['CompanyName'].replace(r'[+]+','plus',regex=True).replace(r'[-]+','dash',regex=True).replace(r'[&]+','and',regex=True).astype(str)
#         insert_to_sqlserver(merged_df)
        
  
#         print("成功抓取日期：",str(start_date))
#     except Exception as e:
#         # 在 except 塊中處理錯誤
#         error_message = f"錯誤訊息: {str(e)}"
#         traceback_info = traceback.format_exc()
#         # 將錯誤訊息寫入到文字檔案中
#         filename = "error_log.txt"
#         with open('log/'+filename, 'a') as file:
#             file.write(error_message + '\n')
#             file.write("Traceback 訊息:\n")
#             file.write(traceback_info)
#             file.write("----------------------------\n")
#             print("錯誤已記錄到檔案:", filename,"日期為：",str(start_date))
#     finally:
#         # print(str(start_date))
#         start_date -= timedelta(days=1)




df = pd.read_csv('table.csv')
tmp = ['fff','ddd','vvv']

for i in range(len(tmp)):
    col = tmp[i]
    for j in range(3):
        name = col
        table = df['Name'][j]
        sql = f"ssss {table} fum {name}"
        print(sql)