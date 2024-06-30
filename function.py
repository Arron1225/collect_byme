import pymysql
import pytz
import csv
import re
import decimal
import hashlib
import html
import random, string
import os.path
import time
import requests
import pandas as pd
import pyodbc
import pymssql
import struct
import os
import pytz
# from google.oauth2 import service_account
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaFileUpload
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.errors import HttpError
from requests.exceptions import ConnectionError, Timeout, RequestException
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime,date,timedelta
from io import StringIO
from sqlalchemy import create_engine,Table,Column,MetaData,String,text,Date, Time, TEXT ,Integer
from sqlalchemy.dialects.mysql import NVARCHAR
from sqlalchemy.engine import URL
from generateApiKey import generateApiKey
from datetime import datetime, timedelta,date

def out_words():
    res = ''.join(random.choices(string.ascii_uppercase +string.digits, k=16))
    # seed='16'
    # api_key = generateApiKey(res,seed)
    return res 

# 轉換時間(西元---->民國)
def conver(input:str)-> str:
    a = input
    b = a.split('-')
    y = b[0]
    afy = int(y)-1911
    afy = str(afy)
    out = '/'.join([afy,b[1],b[2]])
    return out

# 先建一個連線函式
def get_conn():
    conn_str = (
        r'DRIVER={ODBC Driver 17 for SQL Server};'
        r'SERVER=localhost;'
        r'DATABASE=BeComeRich;'
        r'Trusted_Connection=yes;'
    )
    conn = pyodbc.connect(conn_str)
    return conn
# 上傳雲端
def upload_to_google(file_name_str:str,google_Folder_ID:str):
    UPLOAD_FOLDER = google_Folder_ID
    SCOPES = ['https://www.googleapis.com/auth/drive']
    SERVICE_ACCOUNT_FILE = 'auto-427008-9f517ae0199f.json'

    # 建立憑證
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    # 串連服務  
    service = build('drive', 'v3', credentials=creds)

    # filename = file_name_str+".csv"      # 要上傳檔案的路徑與名稱
    media = MediaFileUpload(file_name_str) 
    file = {'name': file_name_str, 'parents': [UPLOAD_FOLDER]}

    print("開始上傳檔案...")
    file_id = service.files().create(body=file, media_body=media).execute()
    print(file_id)   # 印出上傳檔案後的結果

# 函式，把抓取的格式轉換成yyyy-mm-dd
def preprocess_date(input:str)-> str:
    pattern = r'(\d{4})年(\d{1,2})月(\d{1,2})日'
    match = re.search(pattern, input)
    if match:
        year = match.group(1)
        month = match.group(2).zfill(2)  # 確保月份是二位數
        day = match.group(3).zfill(2)    # 確保日期是二位數
        extracted_date = f"{year}-{month}-{day}"
        print("抓到的日期:", extracted_date)
    else:
        print("未抓到日期匹配")
    return extracted_date

# 昨天日期字串
def get_yesterday()-> str:
    today = datetime.today()

    # 昨天日期
    yesterday = today - timedelta(days=1)
    # 格式轉換
    yesterday_str = yesterday.strftime('%Y-%m-%d')
    return yesterday_str

# 連接mysql
def connect_setting_mysql():
    database_type = 'mysql'
    connector = 'pymysql'
    user = 'root'
    password = ''
    host = 'localhost'
    database_name = 'pwc'
    port = '3307'
    connection_string = f'{database_type}+{connector}://{user}:{password}@{host}:{port}/{database_name}'
    engine = create_engine(connection_string)
    return engine

# 資料處理 decimal
def change_decimal_to_num(input_list):
    tmp = []
    for i in range (len(input_list)):
        tmp.append(input_list[i][0])
    return tmp

# 改檔案名
def rename_files_in_directory(directory_path, old_prefix, new_prefix):
    # 列出目錄中的所有檔案
    files = os.listdir(directory_path)
    
    # 逐一處理每個檔案
    for filename in files:
        # 建立舊檔案名稱和新檔案名稱的完整路徑
        old_filepath = os.path.join(directory_path, filename)
        
        # 檢查是否為檔案而非目錄
        if os.path.isfile(old_filepath):
            # 取得檔案的副檔名
            file_extension = os.path.splitext(filename)[1]
            
            # 建立新的檔案名稱
            new_filename = filename.replace(old_prefix, new_prefix)
            new_filepath = os.path.join(directory_path, new_filename)
            
            # 執行改名操作
            os.rename(old_filepath, new_filepath) 
            print(f"已將檔案名稱由 {filename} 改為 {new_filename}")
            
# 匯入資料後，清空資料夾
def clear_directory(directory_path):
    # 列出目錄中的所有檔案
    files = os.listdir(directory_path)
    
    # 刪除每個檔案
    for file_name in files:
        file_path = os.path.join(directory_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
        print("移除"+file_name)
        
# 查找特定文件的函數
def find_file_name(target, path='.'):
    for root, dirs, files in os.walk(path):
        if target in files:
            return target  #返回文件名稱
    return None

# 創建新圍資料表
def create_news_table():
    engine = connect_setting_mysql()
    table_name = "stock_news"
    metadata = MetaData()
    table = Table(
        table_name, 
        metadata, 
        Column('Head', NVARCHAR(60), nullable=False), 
        Column('Url', NVARCHAR(25), nullable=False), 
        Column('News_date', Date, nullable=False), 
        Column('News_content', TEXT, nullable=True),  
    )
    try: 
        metadata.create_all(engine) 
        print(f"資料表 {table_name} 創建成功！") 
    except Exception as e: 
        print(f"創建資料表時出錯：{str(e)}")