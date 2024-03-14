import pyaudio
import wave
import os.path
from datetime import datetime
import time
import speech_recognition 
from googletrans import Translator


# 錄音基本參數設定
chunk = 1024                     # 記錄聲音的樣本區塊大小
format = pyaudio.paInt16         # 樣本格式，可使用 paFloat32、paInt32、paInt24、paInt16、paInt8、paUInt8、paCustomFormat
channels = 1                     # 聲道數量                      
rate = 44100                     # 取樣頻率
filename = "test.wav"                   # 錄音檔名
seconds = 20                     # 錄音秒數
i = 1
to_lang = "en"



    

# def begin(file,record_second):

# begin(filename,seconds)
# record_voice(filename ,seconds)
def record_voice(file , second):
    p = pyaudio.PyAudio()           
    print("開始錄音...")
    stream = p.open(format=format, channels=channels, rate=rate, frames_per_buffer=chunk, input=True)
    wave_file = wave.open(file,'wb')
    wave_file.setnchannels(channels)                        # 聲道設置
    wave_file.setsampwidth(p.get_sample_size(format))       # 樣本格式設置
    wave_file.setframerate(rate)                            # 頻率設置
    for _ in range(0, int(rate * second / chunk)):
        data = stream.read(chunk)                           # 讀取區塊
        wave_file.writeframes(data)                         # 寫入資料
    stream.stop_stream() 
    stream.close()
    p.terminate()
    wave_file.close()
    print("錄音結束...")
date_time_file = time.strftime("%Y%m%d-%H%M%S.wav")
filename = date_time_file
record_voice(filename,seconds)

r = speech_recognition.Recognizer()
audio = speech_recognition.AudioFile(filename)
language_select = "ja-JP"
with audio as source:
    r.adjust_for_ambient_noise(source)
    audio = r.record(source)                  
    result = r.recognize_google(audio ,language="ja-JP")
    
# print(result)
    
try:
    print("Result: \n" + result)
except speech_recognition.UnknownValueError:
    print("Unknown Error")    
    
    
translator= Translator()
translation = translator.translate(result).text
print("First translate to English :\n" + translation)
fn = translator.translate(translation,dest="EN-US").text
print("Finally Result :\n" +fn)
# print("After translator : \n" + translation)