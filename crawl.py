import requests
import csv
import pandas as pd
from bs4 import BeautifulSoup
from googletrans import Translator

response = requests.get("https://mops.twse.com.tw/mops/web/t05sr01_1")
tmp_test = []
body_content=[]
body_content_after = []
translator = Translator()
if response.status_code == 200:
    print("success")
    # print("回應：",response.text)
else:
    print("請求失敗",response.status_code)    
soup = BeautifulSoup(response.content, "html.parser")
# table = soup.find("tr",class_="tblHead")

# for test in table.find_all("th"):
#     print(test.text)
#     tmp_test.append(test.text.strip())
# print(tmp_test)
# with open("test.csv" ,"w") as file:
#     writer = csv.writer(file)
#     writer.writerow(tmp_test)
content = soup.find_all("tr",class_="odd")
for c in content:
    # print("c.text.strip()")
    body_content.append(c.text.strip())
    # body_content_after.append(translator.translate(c.text.strip(),dest="English").text)
print(body_content)    
even_content = soup.find_all("tr",class_="even")
for e in even_content:
    # print("e.text.strip()")
    body_content.append(e.text.strip())  
print(body_content)
 
# print(table)
# for body in table.find_all('tr'):
#     for d in body.find_all('td')[3:]:
#         # print(d.text)
#         tmp_test.append(d.text.strip())
#         # tmp_test.append(d.text) 
# print(tmp_test)
        

# # for num in rows:
# #     id = num.find_all('td')[0].text()
# #     print(id)
# # # tmp_test.append({
# #     'id':id
# # })   
# # with open('tmp.csv', 'w') as csv_file:
# #     writer = csv.writer(csv_file)
# #     for tmp in tmp_test:
# #         writer.writerow(tmp)
    
# header = soup.find_all('table')[4]


# # print(header)
# head = header.find_all('th')
# print(head)