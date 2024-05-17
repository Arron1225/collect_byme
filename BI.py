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

import requests
from bs4 import BeautifulSoup
import csv

# 目标URL
base_url = 'https://ifoodie.tw'
target_url = f'{base_url}/explore/高雄市/list/中山大學附近美食'

head_tmp =[]
response = requests.get(target_url)
if response.status_code == 200:
   soup = BeautifulSoup(response.content, "html.parser")
#    head = soup.find_all("div",class_="jsx-320828271 title")
#    for h in head:
#     head_tmp.append(h.text.strip())
# print(head_tmp)


# time_tmp =[]
# timeing = soup.find_all("div","jsx-320828271 info")  
# for t in timeing:
#     time_tmp.append(t.text.strip())
# print(time_tmp)

# comment_tmp =[]
# comment = soup.find_all("div","jsx-2373119553 text")  
# for c in comment:
#     comment_tmp.append(c.text.strip())
# print(comment_tmp)

# address_tmp =[]
# address = soup.find_all("div","jsx-320828271 address-row")  
# for ad in address:
#     address_tmp.append(ad.text.strip())
# print(address_tmp)


tmp_url =[]
url = soup.find_all("a","jsx-1565883303 message")
for u in url:
    tmp_url.append(u.get('href'))
print(tmp_url)

complete_url = []
for link in tmp_url:
    complete_url.append("https://ifoodie.tw"+ link)
print(complete_url)

  