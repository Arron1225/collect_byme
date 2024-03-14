import sys
from PyQt5.QtWidgets import *
import pyaudio
import wave
import os.path
from datetime import datetime
import time
import speech_recognition 
from googletrans import Translator
# app = QApplication(sys.argv)
# widget = QWidget()
# widget.resize(800,600)
# widget.setWindowTitle("test")
# QWidget,QApplication,QPushButton,QGridLayout, QVBoxLayout,QTextEdit
chunk = 1024                     # 記錄聲音的樣本區塊大小
format = pyaudio.paInt16         # 樣本格式，可使用 paFloat32、paInt32、paInt24、paInt16、paInt8、paUInt8、paCustomFormat
channels = 1                     # 聲道數量                      
rate = 44100                     # 取樣頻率
filename = "test.wav"                   # 錄音檔名
seconds = 20                     # 錄音秒數

# widget.show()
# sys.exit(app.exec())
class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        # date_time_file = time.strftime("%Y%m%d-%H%M%S.wav")
        self.filename = time.strftime("%Y%m%d-%H%M%S.wav")
        # self.resize(800,600)  
        self.setWindowTitle("test")
        self.resize(350, 450)
        layout = QVBoxLayout()
        self.box1 = QSpinBox()        
        self.box1.setRange(0,200)
        
        
        #startButton setting
        self.setLayout(layout)
        self.startButton = QPushButton('start',self)
        self.startButton.resize(300,150)
        self.startButton.setStyleSheet("background-color: green")
        self.startButton.clicked.connect(self.record)
        layout.addWidget(self.startButton)
        
        #stopButton setting
        # self.stopButton = QPushButton('stop', self)
        # self.stopButton.resize(300,150)
        # self.stopButton.setStyleSheet("background-color: red")
        # layout.addWidget(self.stopButton)
        
        #language select
        self.languageSelect = QComboBox()
        self.languageSelect.addItems(["Japanese", "English","Korean"])
        layout.addWidget(self.languageSelect)
        
        
        self.orignTextArea = QTextEdit()
        self.orignTextArea.setReadOnly(True)
        layout.addWidget(self.orignTextArea)
        
        
       
        
        self.afterTextArea = QTextEdit()
        self.afterTextArea.setReadOnly(True)
        layout.addWidget(self.afterTextArea)
        layout.addWidget(self.box1)
        layout.addStretch()
        self.setLayout(layout)
        
        
    def record(self):
        p = pyaudio.PyAudio()           
        print("開始錄音...")
        stream = p.open(format=format, channels=channels, rate=rate, frames_per_buffer=chunk, input=True)
        wave_file = wave.open(self.filename,'wb')
        wave_file.setnchannels(channels)                        # 聲道設置
        wave_file.setsampwidth(p.get_sample_size(format))       # 樣本格式設置
        wave_file.setframerate(rate)                            # 頻率設置
        for _ in range(0, int(rate * self.box1.value() / chunk)):
            data = stream.read(chunk)                           # 讀取區塊
            wave_file.writeframes(data)                         # 寫入資料
        stream.stop_stream() 
        stream.close()
        p.terminate()
        wave_file.close()
        print("錄音結束...")    
        r = speech_recognition.Recognizer()
        audio = speech_recognition.AudioFile(self.filename)
        # language_select = "ja-JP"
        with audio as source:
            r.adjust_for_ambient_noise(source)
            audio = r.record(source)                  
        result = r.recognize_google(audio ,language="ja-JP")  
        self.orignTextArea.setText(result)
        translator= Translator()
        translation = translator.translate(result).text 
        fn = translator.translate(translation,dest="zh-tw").text
        self.afterTextArea.setText(fn) 
        try:
            print("Result: \n" + result)
        except speech_recognition.UnknownValueError:
            print("Unknown Error")    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyWidget()
    w.show()
    sys.exit(app.exec_())