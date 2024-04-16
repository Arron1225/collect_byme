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
tmp = ["113/03/12","113/03/111","113/03/111","113/02/11","113/02/11"]
tt=[]
for i in range(len(tmp)):
    a=tmp[i] 
    b=a.split('/')
    year = b [0]
    month = b [1]
    day = b [2]
    after_year = int(year)+1911
    after_year = str(after_year)
    a1 = '-'.join([after_year,month,day])
    tmp[i]=a1
print(tmp)

print("Original Dataframe") 
  
first_column = df.pop('Name') 
df.insert(0, 'Name', first_column) 
 