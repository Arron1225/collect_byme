import requests
import pandas as pd
import numpy as np
import csv
import time
from datetime import datetime, timedelta,date,time
import pytz
import pyodbc
import traceback
import pymssql
import struct
import os.path
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from io import StringIO
from sqlalchemy import create_engine,Table,Column,MetaData,String,text
from sqlalchemy.engine import URL
from sqlalchemy import create_engine
from function import get_conn,conver,upload_to_google,connect_setting_mysql,fetch_data_with_retries

# 這裡主要都是函式
TPEX_FOLDER = '1yO3SePD8liVkDeQGbA2hsyAo4LAIvRvc'



# 先創table
def create_table():
    # 資料庫連線 sql server
    conn = get_conn()
    create_table_sql = '''
        CREATE TABLE stock_otc (
            DataDate date NOT NULL,
            CompanyCode nvarchar(25) NOT NULL,
            CompanyName nvarchar(50) NOT NULL,
            [Close] decimal(18,4) NOT NULL,
            [Change] nvarchar(18) NULL,
            [Open] decimal(18,4) NULL,
            High decimal (18,5) NULL,
            Low decimal (18,5) NULL,
            AveragePrice decimal (18,5) NULL,
            TradingShare bigint NULL,
            TransactionAmount bigint NULL,
            TransactionNumber bigint NULL,
            LatestBidPrice decimal (18,5)  NULL,
            LatesAskPrice decimal (18,5)  NULL,
            Capitals varchar(50) NULL,
            NextReferencePrice decimal (18,5)  NULL,
            NextLimitUp decimal (18,5)  NULL,
            NextLimitDown decimal (18,5)  NULL,
            PRIMARY KEY (DataDate,CompanyCode)
        );
    '''
    # 使用 SQL 命令創建新的資料表
    try:
        cursor = conn.cursor()
        cursor.execute(create_table_sql)
        conn.commit()
        print("資料表 stock_otc 創建成功！")
    except Exception as e:
        print(f"創建資料表時出錯：{str(e)}")
    finally:
        # 關閉 cursor 和 conn
        cursor.close()
        conn.close()
        
# 寫入資料庫
def insert_to_sqlserver(inpt_df):
    conn_str = (
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=localhost;'
    r'DATABASE=BeComeRich;'
    r'Trusted_Connection=yes;'
    )
    connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": conn_str})

    engine = create_engine(connection_url)
    # 資料庫連線 sql server
    try:
        table_name = 'stock_otc'
        inpt_df.to_sql(table_name,con=engine,index=False,if_exists='append',schema='dbo')
        print(f"成功將 DataFrame 寫入 SQL Server 資料表 {table_name} 中！")
    except Exception as e:
        error_message = f"將 DataFrame 寫入 SQL Server 資料表時發生錯誤: {str(e)}"
        
        # 將錯誤訊息寫入到文字檔案中
        filename = "sql_error_log.txt"
        with open('log/'+filename, 'a',encoding='utf-8') as file:
            file.write(error_message + '\n')
        
            file.write("----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
            print("錯誤已記錄到檔案:", filename,"SQL錯誤")
  
  
  
# 這邊我要改成從sql server那邊抓資料過來 
def insert_to_mysql(input_df):
    engine = connect_setting_mysql()
    co_id  = input_df['CompanyCode']
    for i in range(len(co_id)):
        table_name = co_id[i]
        filrt_df = input_df[input_df['CompanyCode']==table_name]
        filrt_df.to_sql(name=table_name,con=engine,if_exists='append',index=False)
        print(f"{table_name}成功輸入資料庫")
        
        
    


# 這裡是主要跑歷史資料的程式
# 備註:有問題可以單獨用來測試(例如沒抓到資料)
def get_history_data(start:date,end:date):
    while start>= end:
        param = conver(str(start))
        try:       
            link = f'http://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_download.php?l=zh-tw&d={param}&s=0,asc,0'
            content = fetch_data_with_retries(link)
            # r = requests.get(link)
            # lines = r.text.replace('\r', '').split('\n')
            if content:
                lines = content.replace('\r', '').split('\n')
                df = pd.read_csv(StringIO("\n".join(lines[3:])), header=None)
                df.columns = list(map(lambda l: l.replace(' ',''), lines[2].split(',')))
                df.index = df['代號']
                df = df.drop(['代號'], axis=1)
                df.to_csv('test_tpex.csv')
                
                
                # 原本的寫法
                df_cleaned = df.apply(lambda x: x.str.strip().replace('---', 0))
                df_cleaned = df_cleaned.dropna(subset=['收盤','漲跌','開盤','最高','最低'],axis=0, how='all')
                # 更新的寫法
                # df_cleaned = df.replace('---', 0)
                # df_cleaned = df_cleaned.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
                # df_cleaned = df_cleaned.dropna(subset=['收盤','漲跌','開盤','最高','最低'], axis=0, how='all')

                
                
                # df.replace(['---', '----'], 0, inplace=True)
                # df_cleaned = df.dropna(axis=1, how='all')
                df_cleaned.to_csv('ok.csv')
                
                df_names = pd.read_csv('final_otc_code_代號中文.csv')
                # 第二個 DataFrame：存放名字和其他資料
                df_names_addresses = pd.read_csv('ok.csv')
                merged_df = pd.merge(df_names_addresses, df_names, on='代號', how='inner')
                # 正常會有'最後買量(千股)','最後賣量(千股)'，但在2020/4/28沒了，所以暫時先註解
                # merged_df.drop(['最後賣量(千股)','最後買量(千股)'],axis=1,inplace=True)
                # merged_df.drop(['Unnamed: 0_y','Unnamed: 0_x'],axis=1,inplace=True)
                
                # 新增日期欄位， 因為日期欄位會被創到最後一個，所以會將他移到第一個，將最後一欄移動到第一欄
                merged_df = merged_df.assign(DataDate=start)
                last_column_name = merged_df.columns[-1]
                merged_df = merged_df[[last_column_name] + [col for col in merged_df.columns if col != last_column_name]]
                # 原本欄位名是中文，將他改名成英文
                merged_df.rename(columns={'代號':'CompanyCode','名稱':'CompanyName','收盤':'Close','漲跌':'Change','開盤':'Open','最高':'High','最低':'Low','成交股數':'TradingShare','均價':'AveragePrice','成交金額(元)':'TransactionAmount','次日參考價':'NextReferencePrice','成交筆數':'TransactionNumber','發行股數':'Capitals','最後賣價':'LatesAskPrice','最後買價':'LatestBidPrice','次日漲停價':'NextLimitUp','次日跌停價':'NextLimitDown'},inplace=True)
                merged_df['CompanyName']=merged_df['CompanyName'].replace(r'[+]+','plus',regex=True).replace(r'[-]+','dash',regex=True).replace(r'[&]+','and',regex=True).astype(str)
                merged_df['TradingShare']=merged_df['TradingShare'].str.replace(',', '')
                merged_df['TransactionAmount']=merged_df['TransactionAmount'].str.replace(',', '')
                merged_df['TransactionNumber']=merged_df['TransactionNumber'].str.replace(',', '')
                # upload_file_name ="tpex_"+str(start)+'.csv'
                # merged_df.to_csv(upload_file_name,index=False)
                # 備份到雲端
                # upload_to_google(upload_file_name,TPEX_FOLDER)
                
                # 還需要加到mysql
                # insert_to_mysql(merged_df)
                
                insert_to_sqlserver(merged_df)


                print("成功抓取日期：",str(start))
                print('oooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo')
            
        except Exception as e:
            error_message = f"錯誤訊息: {str(e)}"
            # traceback_info = traceback.format_exc()
            # 將錯誤訊息寫入到文字檔案中
            filename = "data_error_log.txt"
            with open('log/'+filename, 'a',encoding='utf-8') as file:
                file.write(error_message + '\n')
                # file.write("Traceback 訊息:\n")
                # file.write(traceback_info)
                file.write("日期為："+ str(start))
                file.write("---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
                print("錯誤已記錄到檔案:", filename,"日期為：",str(start))
        finally:
            start -= timedelta(days=1)

# 以下是原本的寫法
# 保留原本的寫法，如果有些沒抓到再用來看看問題在哪裡
def get_oneday_data():
    link = f'http://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_download.php?l=zh-tw&d=104/07/07&s=0,asc,0'
    r = requests.get(link)
    lines = r.text.replace('\r', '').split('\n')
    df = pd.read_csv(StringIO("\n".join(lines[3:])), header=None)
    df.columns = list(map(lambda l: l.replace(' ',''), lines[2].split(',')))
    df.index = df['代號']
    df = df.drop(['代號'], axis=1)
    df.to_csv('test_tpex.csv')

    # 寫好的，資料前處理，處理空值問題
    df = pd.read_csv('test_tpex.csv')
    df_cleaned = df.apply(lambda x: x.str.strip().replace('---', np.nan))
    df_cleaned = df_cleaned.dropna(subset=['收盤','漲跌','開盤','最高','最低'],axis=0, how='any')
    df_cleaned.to_csv('ok.csv')

    #合併資料欄位以及移除不必要欄位，第二個 DataFrame：存放名字和其他資料，使用 merge() 函數根據名字合併兩個 DataFrame
    df_names = pd.read_csv('final_otc_code_代號中文.csv')
    df_names_addresses = pd.read_csv('ok.csv')
    merged_df = pd.merge(df_names_addresses, df_names, on='代號', how='inner')
    # 正常會有'最後買量(千股)','最後賣量(千股)'，但在2020/4/28沒了，所以暫時先註解
    merged_df.drop(['Unnamed: 0'],axis=1,inplace=True)
    merged_df.drop_duplicates(inplace=True)
    # merged_df.drop(['Unnamed: 0_y','Unnamed: 0_x'],axis=1,inplace=True)
    
    #新增日期欄位，因為日期欄位會被創到最後一個，所以會將他移到第一個
    specific_date = date(2015,7,7) 
    merged_df = merged_df.assign(DataDate=specific_date)
    last_column_name = merged_df.columns[-1]
    merged_df = merged_df[[last_column_name] + [col for col in merged_df.columns if col != last_column_name]]
     
    #原本欄位名是中文，將他改名成英文
    merged_df.rename(columns={'代號':'CompanyCode','名稱':'CompanyName','收盤':'Close','漲跌':'Change','開盤':'Open','最高':'High','最低':'Low','成交股數':'TradingShare','均價':'AveragePrice','成交金額(元)':'TransactionAmount','次日參考價':'NextReferencePrice','成交筆數':'TransactionNumber','發行股數':'Capitals','最後賣價':'LatesAskPrice','最後買價':'LatestBidPrice','次日漲停價':'NextLimitUp','次日跌停價':'NextLimitDown'},inplace=True)
    merged_df['CompanyName']=merged_df['CompanyName'].replace(r'[+]+','plus',regex=True).replace(r'[-]+','dash',regex=True).replace(r'[&]+','and',regex=True).astype(str)
    merged_df['TradingShare']=merged_df['TradingShare'].str.replace(',', '')
    merged_df['TransactionAmount']=merged_df['TransactionAmount'].str.replace(',', '')
    merged_df['TransactionNumber']=merged_df['TransactionNumber'].str.replace(',', '')
    merged_df.to_csv('fin.csv')
    #輸入資料庫
    insert_to_sqlserver(merged_df)
    
# 四捨五入，更新小數點後第二位問題(可以再微調)(目前是微調上市那邊的)(這裡是更新歷史全部的)
def update_value():
    """
    Doing stuff
    """
    # 資料庫連線 sql server
    conn = get_conn()
    df = pd.read_csv('table.csv')
    cols = ['TenDayMovingAverage','TwentyDayMovingAverage','SixtyDayMovingAverage']
    for i in range(len(cols)):
        col_name = cols[i]
        for j in range(len(df)):
            name = col_name
            table = df['table_name'][j]
            sql_select = f"""SELECT {name},ROUND({name}, 2) AS RoundedValue FROM {table} """

            cursor = conn.cursor()
            cursor.execute(sql_select)
            result = cursor.fetchall()
            for row in result:
                original_value = row[0]  #原始的 decimal 值
                rounded_value = row[1]   #四捨五入後的值

             # 更新資料庫中的字段，將四捨五入後的值寫回原來欄位
                sql_update = f"""UPDATE {table} SET {name} = ? WHERE {name} = ?"""
                cursor.execute(sql_update, (rounded_value, original_value))
                conn.commit()
                print("更新成功:",table,"的",name,"欄位")

# 只更新當天的四捨五入函式
def only_update_today():
    """
    fuck
    """
    today_date = datetime.now().strftime('%Y-%m-%d')
    datatime = "DataDate"
    conn = get_conn()
    df = pd.read_csv('table.csv')
    cols = ['TenDayMovingAverage','TwentyDayMovingAverage','SixtyDayMovingAverage']
    for i in range(len(cols)):
        col_name = cols[i]
        for j in range(len(df)):
            name = col_name
            table = df['table_name'][j]
            sql_select = f"SELECT {name},ROUND({name}, 2) AS RoundedValue FROM {table} WHERE  CONVERT(date, {datatime}) = ?"

            cursor = conn.cursor()
            cursor.execute(sql_select, (today_date,))
            result = cursor.fetchall()
            for row in result:
                original_value = row[0]  #原始的 decimal 值
                rounded_value = row[1]   #四捨五入後的值

             # 更新資料庫中的字段，將四捨五入後的值寫回原來欄位
                sql_update = f"""UPDATE {table} SET {name} = ? WHERE {name} = ? AND CONVERT(date, {datatime}) = ?"""
                cursor.execute(sql_update, (rounded_value, original_value,today_date))
                conn.commit()
                print("更新成功:",table,"的",name,"欄位")

# 新增欄位
def alter_col():
    conn  = get_conn()
    insert_cols = ['FiveDayMovingAverage','TenDayMovingAverage','TwentyDayMovingAverage','SixtyDayMovingAverage','TradeVolumeFiveDayMovingAverage','TradeVolumeTenDayMovingAverage','TradeVolumeTwentyDayMovingAverage','TradeVolumeSixtyDayMovingAverage']
    
    data_type = "decimal (18,5)"
    for i in range(len(insert_cols)):
        new_col = insert_cols[i]
        sql_alter = f"ALTER TABLE stock_otc ADD {new_col} {data_type} NULL"    
        cursor = conn.cursor()
        cursor.execute(sql_alter)
        conn.commit()
        print("欄位創建成功"+new_col)
        
# 更新均線(價格)
def update_price_movingaverage(update_col:str ,type_num:str ,start:date ,end:date):
    conn = get_conn()
    cursor = conn.cursor()
   
    df= pd.read_csv('tpex_code.csv')
    tpex_code=df['CompanyCode']
    while start>=end:
        for i in range(len(tpex_code)):
            code = tpex_code[i]
            
            sql_update_mv = f"""
                UPDATE stock_otc
                SET {update_col} = (
                    SELECT AVG([Close])
                    FROM (
                        SELECT TOP {type_num} [Close]
                        FROM [BeComeRich].[dbo].[stock_otc]
                        WHERE DataDate <= ?
                        AND CompanyCode = ?
                        ORDER BY DataDate DESC
                    ) AS SubQuery
                )
                WHERE DataDate = ?
                AND CompanyCode = ?
            """
            cursor.execute(sql_update_mv,(start,code,start,code))
            conn.commit()
            print(f"更新成功 {update_col} for {code} on {start}")
        start -= timedelta(days=1)

def update_valume_movingaverage(update_col:str ,type_num:str ,start:date ,end:date):
    conn = get_conn()
    cursor = conn.cursor()
    # update_col = ['FiveDayMovingAverage','TenDayMovingAverage','TwentyDayMovingAverage','SixtyDayMovingAverage']
    df= pd.read_csv('tpex_code.csv')
    tpex_code=df['CompanyCode']
    while start>=end:
        for i in range(len(tpex_code)):
            code = tpex_code[i]
            
            sql_update_mv = f"""
                UPDATE stock_otc
                SET {update_col} = (
                    SELECT AVG([TradingShare])
                    FROM (
                        SELECT TOP {type_num} [TradingShare]
                        FROM [BeComeRich].[dbo].[stock_otc]
                        WHERE DataDate <= ?
                        AND CompanyCode = ?
                        ORDER BY DataDate DESC
                    ) AS SubQuery
                )
                WHERE DataDate = ?
                AND CompanyCode = ?
            """
            cursor.execute(sql_update_mv,(start,code,start,code))
            conn.commit()
            print(f"更新成功 {update_col} for {code} on {start}")
        start -= timedelta(days=1)   
        
def dump_ma():
    conn_str = (
        r'DRIVER={ODBC Driver 17 for SQL Server};'
        r'SERVER=localhost;'
        r'DATABASE=BeComeRich;'
        r'Trusted_Connection=yes;'
    )
    connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": conn_str})

    engine = create_engine(connection_url)
    df = pd.read_csv('table.csv')
    table = df["table_name"][0]
    name = "TwentyDayMovingAverage"
    sql_select = f"""SELECT {name},ROUND({name}, 2) AS RoundedValue FROM {table} """
   
    df = pd.read_sql(sql_select,engine)
    df.to_csv('TwentyDayMovingAverage.csv', index=False, encoding='utf-8')
        
        
        
def dump_to_mysql():     
    sum=0
    conn_str = (
        r'DRIVER={ODBC Driver 17 for SQL Server};'
        r'SERVER=localhost;'
        r'DATABASE=BeComeRich;'
        r'Trusted_Connection=yes;'
    )
    connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": conn_str})

    engine = create_engine(connection_url)
    st = datetime.now().date()
    dd = str(st)
    sql = f"SELECT * FROM stock_otc WHERE DataDate = '{dd}'"
    df = pd.read_sql(sql,engine)
    # df.to_csv('tpday_otc.csv',index=False)
    code_df = df['CompanyCode'].str.lower
    engine = connect_setting_mysql()
    for code in code_df:
        table_name = code
        insert_df = df[df['CompanyCode']==table_name]
        insert_df.to_sql(table_name,con=engine,index=False,if_exists='append')
        sum +=len(insert_df)
        print(sum)
        print(f"已成功輸入{table_name}的資料")
     
    
    
    
#備註: 
if __name__ == "__main__":
    # # 抓取歷史資料
    start_date = datetime(2009,12,31).date()
    end_date = datetime(2007,1,1).date()   
    get_history_data(start_date,end_date)
    
    # 如果有問題，抓一天試試看  104 7/7 
    # get_oneday_data()
    # 抓當天的也用一樣的，我懶得改
    # start_date = datetime(2024,7,3).date()
    # today_data_date = datetime.now().date()
    # get_history_data(start_date,start_date)
    

    
    # # # 更新股價均線 
    st = datetime.now().date()
    # st= datetime(2024,6,17).date()
    end = datetime(2024,6,20).date()
    # update_price_movingaverage("FiveDayMovingAverage","5",st,end)
    # update_price_movingaverage("TenDayMovingAverage","10",st,end)
    # update_price_movingaverage("TwentyDayMovingAverage","20",st,end)
    # update_price_movingaverage("SixtyDayMovingAverage","60",st,end)
    ## 更新交易量均線
    # update_valume_movingaverage("TradeVolumeFiveDayMovingAverage","5",st,end)
    # update_valume_movingaverage("TradeVolumeTenDayMovingAverage","10",st,end)
    # update_valume_movingaverage("TradeVolumeTwentyDayMovingAverage","20",st,end)
    # update_valume_movingaverage("TradeVolumeSixtyDayMovingAverage","60",st,end)
    
    
    
    # 從sql server轉移到mysql
    # dump_to_mysql()
    
    # 這個是把當天抓到的資料(平均線那些四捨五入到小數點後兩位)(還要改，存資料庫是正常，但取出來要四捨五入到第二位)
    # only_update_today()
    
    # 把資料dump出來時，四捨五入
    # dump_ma()
   
    #新增欄位，應該暫時用不到
    # alter_col() 
    
    # create_table().
    