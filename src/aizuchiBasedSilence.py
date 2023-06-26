#!/usr/bin/env python

# ライブラリの読込
import pyaudio
import wave
import numpy as np
from datetime import datetime
import math

# 音データフォーマット
chunk = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 2

# 閾値
threshold = 65

# 音の取込開始
audio = pyaudio.PyAudio()
stream = audio.open(format = FORMAT,
    channels = CHANNELS,
    rate = RATE,
    input = True,
    frames_per_buffer = chunk
)

cnt = 0

while True:
  try:
    # 音データの取得
    data = stream.read(chunk)

    x = np.frombuffer(data, dtype="int16")
    rms = x.max()
    db = 20 * math.log10(rms) if rms > 0.0 else -math.inf
    print(f"音量：{format(db, '3.1f')}[dB]")

    # 閾値以上の場合はファイルに保存
    if rms > threshold:
        print("声を検出")

  except KeyboardInterrupt: ## ctrl+c で終了
      break

stream.stop_stream()
stream.close()
audio.terminate()