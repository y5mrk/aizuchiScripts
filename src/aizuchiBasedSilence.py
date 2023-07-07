#!/usr/bin/env python

# ライブラリの読込
import pyaudio
import numpy as np
import math
import time
import random
import subprocess

# 音データフォーマット
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 2

# 閾値
threshold = 45.0

# 音の取込開始
audio = pyaudio.PyAudio()
stream = audio.open(format = FORMAT,
    channels = CHANNELS,
    rate = RATE,
    input = True,
    frames_per_buffer = chunk
)

isSpeaking = False
speakingTime = 0
speakingStart = 0
silenceStart = 0
silenceEnd = 0

enableAizuchi = False

def aizuchi():
    aizuchi_list = ['うん', 'へー', 'ふーん']
    text = random.choice(aizuchi_list)
    say(text)
    print("相槌: " + text)
    return

def say(text):
    subprocess.call('say "%s"' % text, shell = True)

while True:
  try:
    data = stream.read(chunk, exception_on_overflow = False)
    x = np.frombuffer(data, dtype="int16")
    rms = x.max()
    db = 20 * math.log10(rms) if rms > 0.0 else -math.inf

    current = time.perf_counter()
    silenceTime = current - silenceStart 

    if silenceTime > 1.0 and silenceStart - speakingStart > 0 and enableAizuchi:
      print(f"沈黙時間：{ silenceTime }秒")
      aizuchi()
      enableAizuchi = False

    if db > threshold:
      if not isSpeaking:
        isSpeaking = True
        speakingStart = time.perf_counter()
        print(f"音を検知：{db}")
    else:
      if isSpeaking:
        silenceStart = time.perf_counter()
        
        # 0.2秒より短い音を検知した場合は、相槌を打たない
        if silenceStart - speakingStart > 0.2:
          print(f"しゃべってた時間：{ silenceStart - speakingStart }秒")
          enableAizuchi = True
        isSpeaking = False

  except KeyboardInterrupt: ## ctrl+c で終了
      break

stream.stop_stream()
stream.close()
audio.terminate()