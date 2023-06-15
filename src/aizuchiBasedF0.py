import pyaudio
import matplotlib.pyplot as plt
import numpy as np
import wave
import struct
import datetime
import librosa
import pandas as pd
import random
import subprocess
import time

RATE = 44100
audio = pyaudio.PyAudio()
N = 100
CHUNK = 16384
stream = audio.open(format = pyaudio.paInt16,
        channels = 1,
        rate = RATE,
        frames_per_buffer = CHUNK,
        input = True)

allData = np.empty(0)

def savewav(sig,fileName):
    RATE = 44100 #サンプリング周波数
    #サイン波を-32768から32767の整数値に変換(signed 16bit pcmへ)
    swav = [(int(32767*x)) for x in sig] #32767
    #バイナリ化
    binwave = struct.pack("h" * len(swav), *swav)
    #サイン波をwavファイルとして書き出し
    w = wave.Wave_write("./data/sample_"+fileName+".wav")
    params = (1, 2, RATE, len(binwave), 'NONE', 'not compressed')
    w.setparams(params)
    w.writeframes(binwave)
    w.close()

def aizuchi():
    aizuchi_list = ['うん', 'へー', 'ふーん']
    text = random.choice(aizuchi_list)
    say(text)
    print("相槌: " + text)
    return

def say(text):
    subprocess.call('say "%s"' % text, shell = True)

def waitAizuchi():
    time.sleep(0.5)
    aizuchi()
    time.sleep(1)
    print("音声タイミングの検出を再開します")

while True:
  try:
      input = stream.read(CHUNK, exception_on_overflow = False)
      sig = []
      sig = np.frombuffer(input, dtype = "int16") / 32768
      now_dt = datetime.datetime.now() #現在時刻
      fileName = now_dt.isoformat()
      savewav(sig,fileName)

      filepath = "./data/sample_"+fileName+".wav"
      y, sr = librosa.load(filepath)
      f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin = librosa.note_to_hz('C2'), fmax = librosa.note_to_hz('C7'))
      times = librosa.times_like(f0)

      df_f0 = pd.Series(f0)
      df_f0 = df_f0.dropna(how='all')
      
      if len(df_f0)!=0:
        # print(df_f0.describe())
        pitch_yin = np.average(df_f0)
        if pitch_yin > 80 and pitch_yin < 500:
            minValue = df_f0.min()
            allData = np.append(allData, df_f0)
            allAverage = np.average(allData)
            threshold = allAverage * 0.2
            print("全体の平均: ")
            print(allAverage)
            print("閾値: ")
            print(allAverage - threshold)
            print("今のF0_avrage")
            print(pitch_yin)
            print("今のF0_min")
            print(minValue)
            if minValue < allAverage - threshold:
                print("相槌まで0.5秒")
                waitAizuchi()
		
  except KeyboardInterrupt: ## ctrl+c で終了
		  break

stream.stop_stream()
stream.close()
audio.terminate()