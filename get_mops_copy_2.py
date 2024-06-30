from requests.exceptions import ConnectionError, Timeout, RequestException
from bs4 import BeautifulSoup
import time
import requests
import pandas as pd
import os
from datetime import datetime,date,timedelta
from function import connect_setting_mysql,upload_to_google
UPLOAD_MOPS_FOLDER ='1LOay2IEBWLsx6npLF-6AitXK8pbU17WV'


def fetch_data(url, max_retries=8):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(url, headers=headers, timeout=20)
            response.raise_for_status()
            return response.content
        except (ConnectionError, Timeout) as e:
            retries += 1
            error_msg = f"Error fetching data: {e}\n"
            with open('log/mops_connect_error.txt', 'a', encoding='utf-8') as f:
                f.write(error_msg+'\n')
                
                f.write(f"Connection error: {e}. Retrying {retries}/{max_retries}...")
            print(f"Connection error: {e}. Retrying {retries}/{max_retries}...")
            with open('log/tmp_keep_5.txt', 'a', encoding='utf-8') as f:
                f.write(f"Connection error: {e}. Retrying {retries}/{max_retries}..."+'\n')
            time.sleep(2 ** retries)  # 指數回退
            
        except RequestException as e:
            error_msg = f"Error request: {e}\n"
            with open('log/mops_connect_error.txt', 'a', encoding='utf-8') as f:
                f.write(error_msg+'\n')
                # f.write("日期為:"+str(dateee))
            print(f"Request failed: {e}")
            break

    return None       
    
def extract_data(soup, num):
    try:
        h0 = soup.find('input', {"name": "h"+str(num)+"0"})['value']
        h1 = soup.find('input', {"name": "h"+str(num)+"1"})['value']
        h2 = soup.find('input', {"name": "h"+str(num)+"2"})['value']
        h3 = soup.find('input', {"name": "h"+str(num)+"3"})['value']
        h4 = soup.find('input', {"name": "h"+str(num)+"4"})['value']
        h5 = soup.find('input', {"name": "h"+str(num)+"5"})['value']
        h6 = soup.find('input', {"name": "h"+str(num)+"6"})['value']
        h7 = soup.find('input', {"name": "h"+str(num)+"7"})['value']
        h8 = soup.find('input', {"name": "h"+str(num)+"8"})['value']
        
        return [h0, h1, h2, h3, h4, h5, h6, h7, h8]
    except Exception as e:
        error_msg = f"Error extracting data: {e}\n"
        with open('log/mop_data_error.txt', 'a', encoding='utf-8') as f:
            f.write(error_msg)
            
        return None
    
def main(start:date,end:date):
    res_list = []


    get_start_date = str(start)
    while start>=end:
        try:
            year = f"{start.year-1911:03d}"
            month=f"{start.month:02d}"
            day=f"{start.day:02d}"
            url = f"https://mops.twse.com.tw/mops/web/t05st02?encodeURIComponent=1&step=1&step00=0&firstin=1&off=1&TYPEK=all&year={year}&month={month}&day={day}"
            time.sleep(5)
            content= fetch_data(url)
           
            soup = BeautifulSoup(content, 'html.parser')
            num = 0
            
            while num >=0:
                data = extract_data(soup,num)
                if data is None:
                    print(str(start))#日期上面是當天日期的所有筆數
                    with open('log/tmp_keep_5.txt', 'a', encoding='utf-8') as f:
                        f.write(str(start)+'\n')
                    break
                res_list.append(data)
                with open('log/tmp_keep_5.txt', 'a', encoding='utf-8') as f:
                    f.write(str(num)+'\n')
                print(num)   
                num += 1
        except requests.exceptions.RequestException as e:
            error_msg = f"Error fetching data: {e}\n"
            with open('log/mops_connect_error.txt', 'a', encoding='utf-8') as f:
                f.write(error_msg+ '\n')
                f.write("日期為："+ str(start)+ '\n')
                f.write("---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")

                
        finally:
            start -= timedelta(days=1)
    if res_list:
        df = pd.DataFrame(res_list, columns=["CompanyName", "CompanyCode", "DataDate", "DataTime", "Subject", "SeqNum", "Terms", "OccurDate", "Illustrate"])
        df.drop_duplicates()
        df.to_csv('mop_'+get_start_date+'.csv', index=False, encoding='utf-8-sig')
        print("資料已成功儲存。")
    else:
        print("沒有任何資料被存儲。")
        
if __name__ == "__main__":
    SUM =0
    #處理每天重訊
    st = datetime.now().date()
    # 這個算前三天
    before_data = st - timedelta(days=1)
    end_before_data = st - timedelta(days=2)
    # end = datetime(2024,6,18).date()
   
    # 這個找出每天的重訊
    main(st,st) 
    
    # 這個找出每天的重訊
    main(before_data,end_before_data)     
    today_df = pd.read_csv("mop_"+str(st)+".csv")
    yesterday_df = pd.read_csv("mop_"+str(before_data)+".csv")
    
    # 如果要自訂的話
    # today_df = pd.read_csv("mop_2024-06-21.csv")
    # yesterday_df = pd.read_csv("mop_2024-06-20.csv")
    # upload_to_google("mop_2024-06-21.csv",UPLOAD_MOPS_FOLDER)
    
    # 上傳雲端
    upload_to_google("mop_"+str(st)+".csv",UPLOAD_MOPS_FOLDER)
    
    filter_columns = ['CompanyName','CompanyCode','DataDate','DataTime','Subject']

    # 合併兩個DataFrame，并使用 indicator 參數標示哪些行只出現在 filter_df 中
    merged_df = today_df.merge(yesterday_df, on=filter_columns, how='left', indicator=True)

    # 過濾只出現在 filter_df 中的行
    combine_df = merged_df[merged_df['_merge'] == 'left_only'].drop(columns=['_merge','SeqNum_y','Terms_y','OccurDate_y','Illustrate_y'])
    combine_df.rename(columns={'SeqNum_x':'SeqNum','Terms_x':'Terms','OccurDate_x':'OccurDate','Illustrate_x':'Illustrate'},inplace=True) 
    combine_df['DataTime'] = combine_df['DataTime'].apply(lambda x: str(x).split(' ')[-1])
    print(len(combine_df))
    coco_df = pd.read_csv("mops_code.csv")
    coco_df['CompanyCode'] = coco_df['CompanyCode'].str.lower()
    engine = connect_setting_mysql()
    combine_df['CompanyCode'] =combine_df['CompanyCode'].astype(str)
    for i in range(len(coco_df)):
        table_name = "mops_"+coco_df['CompanyCode'][i]
        code = coco_df['CompanyCode'][i]
        inser_df = combine_df[combine_df['CompanyCode'] == code]
        # print(inser_df)
        SUM += len(inser_df)
        inser_df.to_sql(table_name,con=engine,index=False,if_exists='append')
        
        # 查看現在累積到哪裡
        print(SUM)
        print(f"成功將 DataFrame 寫入mysql 資料表 {table_name} 中！")
    if  SUM == len(combine_df): 
        print(f"成功把{str(SUM)}筆資料存到資料中")
        # 如果成功就把前一天刪掉
        os.remove("mop_"+str(before_data)+".csv")
    else:
        print(f"應該要存{str(len(combine_df))}筆資料，但只有存到{str(SUM)}筆資料")   
        