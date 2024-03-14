# import requests

# res = requests.get('https://pala.tw/python-web-crawler/')
# print(res.text)
# import wave
# import sys

# import pyaudio


# CHUNK = 1024

# if len(sys.argv) < 2:
#     print(f'Plays a wave file. Usage: {sys.argv[0]} filename.wav')
#     sys.exit(-1)

# with wave.open(sys.argv[1], 'rb') as wf:
#     # Instantiate PyAudio and initialize PortAudio system resources (1)
#     p = pyaudio.PyAudio()

#     # Open stream (2)
#     stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
#                     channels=wf.getnchannels(),
#                     rate=wf.getframerate(),
#                     output=True)

#     # Play samples from the wave file (3)
#     while len(data := wf.readframes(CHUNK)):  # Requires Python 3.8+ for :=
#         stream.write(data)

#     # Close stream (4)
#     stream.close()

#     # Release PortAudio system resources (5)
#     p.terminate()
# import os 
# file_path = './.wav'
# filename = os.path.basename(file_path)
# print(filename)
import requests
import csv
import pandas as pd
import time
from bs4 import BeautifulSoup
from urllib.parse import unquote
from selenium import webdriver
head_tmp=[]
urls_tmp=[]
browser = webdriver.Chrome()
browser.get('https://tw.news.yahoo.com/search?p=股票&fr=uh3_news_web&fr2=p%3Anews%2Cm%3Asb&.tsrc=uh3_news_web')
item=[]
# last = browser.execute_script("return document.body.scrollHeight")  # Browser window height
# i = 1
# while True:
#     # Scroll down
#     browser.execute_script("window.scrollTo(0,document.body.scrollHeight);")
#     # i += 1
#     # time.sleep(3)
#     new = browser.execute_script("return document.body.scrollHeight")
#     if new == last:
#         break
#     last =new
    # Check if reaching the end of the page
    # scroll_height = browser.execute_script("return document.body.scrollHeight;")
    # if screen_height * i > scroll_height:
    #     break
# screen_height = browser.execute_script("return window.screen.height;")   # get the screen height of the web
# i = 1
last_height = browser.execute_script("return document.body.scrollHeight")
while True:
    # Scroll down to the bottom
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait for new page segment to load
    time.sleep(5)  # Adjust the sleep duration based on your network speed

    # Calculate new scroll height and compare with last scroll height
    new_height = browser.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# while True:
#     # scroll one screen height each time
#     browser.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
#     i += 1
#     time.sleep(5)
#     # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
#     scroll_height = browser.execute_script("return document.body.scrollHeight;")  
#     # Break the loop when the height we need to scroll to is larger than the total scroll height
#     if (screen_height) * i > scroll_height:
#         break 
# Fetch the data using BeautifulSoup after all data is loaded
soup = BeautifulSoup(browser.page_source, "html.parser")
# Process and save the data as needed
head = soup.find_all("a",class_="Fw(b) Fz(20px) Lh(23px) Fz(17px)--sm1024 Lh(19px)--sm1024 mega-item-header-link Td(n) C(#0078ff):h C(#000) LineClamp(2,46px) LineClamp(2,38px)--sm1024 not-isInStreamVideoEnabled")
# print(head)
for h in head:
    head_tmp.append(h.text.strip())
    urls_tmp.append(h.get('href'))
print(head_tmp) 
print(urls_tmp)
# Close the WebDriver session
browser.quit()



