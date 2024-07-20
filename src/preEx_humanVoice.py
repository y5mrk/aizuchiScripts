import pyaudio
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
import speech_recognition as sr
import MeCab
import whisper
import threading
from dotenv import load_dotenv
import openai
from playsound import playsound

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
waitingSilence = False

detectedSilence = False
detectedSilenceTime = time.perf_counter()

wavFiles = []
terms = []

load_dotenv()
openai.organization = os.environ['API_ORG']
openai.api_key = os.environ['API_KEY']
openai.Model.list()

def savewav(sig,filePath):
  RATE = 44100 #サンプリング周波数
  #サイン波を-32768から32767の整数値に変換(signed 16bit pcmへ)
  swav = [(int(32767*x)) for x in sig] #32767
  #バイナリ化
  binwave = struct.pack("h" * len(swav), *swav)
  #サイン波をwavファイルとして書き出し
  w = wave.Wave_write(filePath)
  params = (1, 2, RATE, len(binwave), 'NONE', 'not compressed')
  w.setparams(params)
  w.writeframes(binwave)
  w.close()

def aizuchi():
  fileList = ['./wavs/un1.wav', './wavs/hai5.wav', './wavs/un4.wav', './wavs/un6.wav', './wavs/un7.wav', './wavs/un8.wav','./wavs/un9.wav','./wavs/hai1.wav', './wavs/hai2.wav', './wavs/hai3.wav', './wavs/hai4.wav','./wavs/hai5.wav','./wavs/haihai1.wav', './wavs/u-n1.wav', './wavs/u-n2.wav', './wavs/unun1.wav']
  choicedFile = random.choice(fileList)
  playsound(choicedFile)
  print(choicedFile)

def say(text):
  subprocess.call('say "%s"' % text, shell = True)

def soundLevelMeter(data):
  rms = data.max()
  db = 20 * math.log10(rms) if rms > 0.0 else -math.inf
  if db > soundLevelThreshold:
    print(f"音を検知：{db}")

def requestGPTAPI(words):
  if len(words) > 1:
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "あなたは友達のように、ユーザの日常について、簡潔に質問するアシスタントです。"},
        {"role": "user", "content": "「"+ words[0] +"」「" + words[1] + "」に関して何か1つ話題を振ってください"}
      ]
    )

    print(completion.choices[0].message.content)
    say(completion.choices[0].message.content)

def analyse(text):
  tagger = MeCab.Tagger()
  node = tagger.parseToNode(text)

  while node:
      term = node.surface
      pos = node.feature.split(',')[0]
      
      if pos == '名詞':
        if term != '?':
          terms.append(term)

      node = node.next
  
  print("名詞：%sを検出" % terms)

def joinWaves(inputs, output):
  try:
    fps = [wave.open(f, 'r') for f in inputs]
    fpw = wave.open(output, 'w')

    fpw.setnchannels(fps[0].getnchannels())
    fpw.setsampwidth(fps[0].getsampwidth())
    fpw.setframerate(fps[0].getframerate())
    
    for fp in fps:
        fpw.writeframes(fp.readframes(fp.getnframes()))
        fp.close()
    fpw.close()

  except wave.Error:
    print("wavの統合エラー")

  except Exception:
    print('wavの統合エラー（unexpected error）')

def transcribeWav():
  global wavFiles
  while True:
    if len(wavFiles) < 2:
      time.sleep(0.5)
      continue
    inputFiles = wavFiles
    print(inputFiles)
    wavFiles = []
    outputFilePath = './data/sample.wav'
    joinWaves(inputFiles,outputFilePath)
    model = whisper.load_model("base")
    result = model.transcribe(outputFilePath)
    print(result["text"])
    analyse(result["text"])

def detectSilence():
  global detectedSilence
  global detectedSilenceTime
  if detectedSilence:
    if time.perf_counter() - detectedSilenceTime > 10:
      print("10秒以上沈黙")
      if len(terms) >= 2:
        words = []
        words.append(terms.pop(-1))
        words.append(terms.pop(-1))
        requestGPTAPI(words)
      detectedSilence = False
  else:
    detectedSilence = True
    detectedSilenceTime = time.perf_counter()

def detectAizuchi():
  global enableAizuchi
  global allData
  global wavFiles
  global detectedSilence
  global detectedSilenceTime
  global waitingSilence
  while True:
    if enableAizuchi:
      if time.perf_counter() - detectedTime > poseTime:
        aizuchi()
        time.sleep(2)
        enableAizuchi = False
        waitingSilence = False
        print("相槌タイミングの検出を再開します")
    try:
        input = stream.read(CHUNK, exception_on_overflow = False)
        sig = []
        sig = np.frombuffer(input, dtype="int16") / 32768
        now_dt = datetime.datetime.now() #現在時刻
        isoDate = now_dt.isoformat()
        filePath = "./data/sample_"+isoDate+".wav"

        savewav(sig,filePath)
        # wavFiles.append(filePath)

        y, sr = librosa.load(filePath)
        f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin = librosa.note_to_hz('C2'), fmax = librosa.note_to_hz('C7'))
        times = librosa.times_like(f0)

        df_f0 = pd.Series(f0)
        df_f0 = df_f0.dropna(how='all')
        
        if len(df_f0)!=0:
          pitch_yin = np.average(df_f0)
          if pitch_yin > 80 and pitch_yin < 500:
            detectedSilence = False
            if enableAizuchi:
              enableAizuchi = False
              waitingSilence = True
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
        #   else:
        #     if detectedSilence:
        #       if time.perf_counter() - detectedSilenceTime > 0.5:
        #         if waitingSilence:
        #           print("0.5秒以上沈黙")
        #           enableAizuchi = True
        #         detectedSilence = False
        #     else:
        #       detectedSilence = True
        #       detectedSilenceTime = time.perf_counter()
        # else:
        #   if detectedSilence:
        #     if time.perf_counter() - detectedSilenceTime > 0.5:
        #       if waitingSilence:
        #         print("0.5秒以上沈黙")
        #         enableAizuchi = True
        #       detectedSilence = False
        #   else:
        #     detectedSilence = True
        #     detectedSilenceTime = time.perf_counter()

        # os.remove(filePath)
      
    except KeyboardInterrupt: ## ctrl+c で終了
      break

  stream.stop_stream()
  stream.close()
  audio.terminate()

if __name__ == "__main__":
  detectAizuchi()