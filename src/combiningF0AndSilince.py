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
import math
import os

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

# 閾値
soundLevelThreshold = 45.0

enableAizuchi = False
poseTime = 0.5
detectedTime = time.perf_counter()

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
  allData = np.empty(0) # 相槌を打ったらデータをリセットする
  print("データをリセット")
  return

def say(text):
  subprocess.call('say "%s"' % text, shell = True)

def soundLevelMeter(data):
  rms = data.max()
  db = 20 * math.log10(rms) if rms > 0.0 else -math.inf
  if db > soundLevelThreshold:
    print(f"音を検知：{db}")

while True:
  if enableAizuchi:
    if time.perf_counter() - detectedTime > poseTime:
      aizuchi()
      time.sleep(2)
      enableAizuchi = False
      print("相槌タイミングの検出を再開します")
  try:
      input = stream.read(CHUNK, exception_on_overflow = False)
      sig = []
      sig = np.frombuffer(input, dtype="int16") / 32768
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
        pitch_yin = np.average(df_f0)
        if pitch_yin > 80 and pitch_yin < 500:
          if enableAizuchi:
            enableAizuchi = False
            print("発話が続いているため相槌をキャンセル")
          minValue = df_f0.min()
          allData = np.append(allData, df_f0)
          allAverage = np.average(allData)
          threshold = allAverage * 0.2
          print(f"平均: {allAverage}, 閾値: {allAverage - threshold}, 今のF0_min: {minValue}")
          if minValue < allAverage - threshold and (not enableAizuchi):
            enableAizuchi = True
            detectedTime = time.perf_counter()
            print("相槌まで%s秒" % poseTime)
      
      # os.remove(filepath)
		
  except KeyboardInterrupt: ## ctrl+c で終了
    break

stream.stop_stream()
stream.close()
audio.terminate()