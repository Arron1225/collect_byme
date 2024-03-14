# yahoo
import requests
import csv
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import unquote

response = requests.get("https://tw.news.yahoo.com/search?p=股票&fr=uh3_news_web&fr2=p%3Anews%2Cm%3Asb&.tsrc=uh3_news_web")
tmp = []
head_tmp=[]
urls_tmp=[]
decoder_urls=[]
each_content=[]
result =""
if response.status_code == 200:
    print("success")
else:
    print("請求失敗",response.status_code)  
soup = BeautifulSoup(response.content, "html.parser")     
head = soup.find_all("a",class_="Fw(b) Fz(20px) Lh(23px) Fz(17px)--sm1024 Lh(19px)--sm1024 mega-item-header-link Td(n) C(#0078ff):h C(#000) LineClamp(2,46px) LineClamp(2,38px)--sm1024 not-isInStreamVideoEnabled")
# print(head)
for h in head:
    head_tmp.append(h.text.strip())
    urls_tmp.append(h.get('href'))
# print(head_tmp) 
# print(urls_tmp)
# https://tw.news.yahoo.com/期交所-明起調高漢唐股票期貨保證金為1-5倍-3月26日恢復-082747481.html

for link in urls_tmp:
    decoder_urls.append("https://tw.news.yahoo.com"+ unquote(link))
# print(decoder_urls)    

# print(urls_tmp[0])
# result = unquote(urls_tmp[0])
# result =  + result
# print(result)

# test = decoder_urls[2]
# second_soup = requests.get(test)
# if second_soup.status_code == 200:
#     print('success')
# else:
#     print("請求失敗",second_soup.status_code)    
# print(len(decoder_urls))



# for i in range(len())
for i in range(len(decoder_urls)):
    
    sss = requests.get(decoder_urls[i])
    soup_content = BeautifulSoup(sss.content, "html.parser")
    content = soup_content.find_all("p")
    # each_content.append(content)
    for c in content:
        result =result + c.text.strip()
    each_content.insert(i,result)
    result =""
    
# print(each_content)
print(len(each_content))
print(len(head_tmp))
print(len(decoder_urls))
df = pd.DataFrame({
    "head":head_tmp,
    "url":decoder_urls,
    "content": each_content   
})        
print(df)
df.to_csv('dataset/yahoo.csv')