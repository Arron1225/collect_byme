import requests
import csv
import pandas as pd
import time
from bs4 import BeautifulSoup
from datetime import datetime, timedelta,date
import numpy as np
from datetime import date
import requests
from bs4 import BeautifulSoup
import csv









# 目標URL
# base_url = 'https://ifoodie.tw'
# target_url = f'{base_url}/explore/高雄市/list/中山大學附近美食?page='

# head_tmp =[]
# time_tmp =[]
# comment_tmp =[]
# address_tmp =[]
# for page in range(1,4):
#     response = requests.get(target_url + str(page))
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, "html.parser")
#         head = soup.find_all("div",class_="jsx-320828271 title")
#         timeing = soup.find_all("div","jsx-320828271 info")  
#         comment = soup.find_all("div","jsx-2373119553 text")  
#         address = soup.find_all("div","jsx-320828271 address-row")  

        
#         for h in head:
#             head_tmp.append(h.text.strip())     
#         for t in timeing:
#             time_tmp.append(t.text.strip())  
#         for c in comment:
#             comment_tmp.append(c.text.strip())
#         for ad in address:
#             address_tmp.append(ad.text.strip())
# # print(head_tmp)
# df = pd.DataFrame(columns=[])
# data = {
#     'name':head_tmp,
#     'comment':comment_tmp,
#     'opentime':time_tmp,
#     'address':address_tmp
# }
# df = pd.DataFrame(data)
# df.to_csv('food.csv')

# url = ['https://hoolee.tw/zongpushi/','https://hoolee.tw/zongpushi/','https://hoolee.tw/zongpushi/','https://nellydyu.tw/blog/post/41749510',
#        'https://nigi33.tw/xinglong-ju-liuhe/','https://nigi33.tw/mis-cafe/','https://www.walkerland.com.tw/article/view/309305','https://after-sleep.com/shoreline-coffee-amp-roaster-sizihwan/','https://damei17.com/zhao-yue/',
#        'https://www.viviyu.com/archives/50552','https://kaikay.tw/biggest-oden/','https://ifoodie.tw/post/6413307f77b9e9728ebf4454-高雄柴山超人氣景觀咖啡廳%21遼闊海景一望無','https://nigi33.tw/hen-pon/',
#        'https://realplay.tw/50911/chicken-steak/','https://ww.bosomgirl.com/2022/09/shichu.html','https://travel.yam.com/article/128785','https://ihappyday.tw/blog/post/arthousetaiwan','https://travelchia.com/oceanside/','https://after-sleep.com/haishan-coffee/',
#        'https://ifoodie.tw/post/61c060d8a6272860c68f7df5-愛馬仕盤子盛裝讓你享受貴婦片刻時光Hi-','https://today.line.me/tw/v2/article/BPDJQQ','https://sweetday.tw/【哈瑪星美食】胖師傅火鍋-啃一整隻大龍骨超狂-白/','https://ifoodie.tw/post/61724d5182828715f71544c3-家味堂專業炒飯-中山大學美食地圖-巴豆妖','https://ifoodie.tw/post/6172cda98282874025786259-桶一天下現滷滷味-高雄西子灣店-銷魂暖胃','https://nellydyu.tw/blog/post/axue',
tmp=[]
tmmm=[]
url = ["https://hoolee.tw/xiangyu/","https://yama.tw/donkeypie/"]

ur = url[0]
response = requests.get(ur)
soup = BeautifulSoup(response.text, "html.parser")
head = soup.find_all("p")
for h in head:
    tmp.append(h.text.strip()) 
df = pd.DataFrame(data=tmp)
df.to_csv("tmp.csv")

ur = url[1]
response = requests.get(ur)
soup = BeautifulSoup(response.text, "html.parser")
hess = soup.find_all("p")
for h in hess:
    tmmm.append(h.text.strip()) 
df = pd.DataFrame(data=tmmm)
df.to_csv("tmmm.csv")






