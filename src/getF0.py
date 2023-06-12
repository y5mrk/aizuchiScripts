import pyaudio
import matplotlib.pyplot as plt
import numpy as np
import wave
import struct
import datetime
import librosa
import pandas as pd

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

RATE=44100
audio=pyaudio.PyAudio()
N=100
CHUNK=16384
stream=audio.open(format = pyaudio.paInt16,
        channels = 1,
        rate = RATE,
        frames_per_buffer = CHUNK,
        input = True,
        output = True) # inputとoutputを同時にTrueにする

while True:
  try:
      input = stream.read(CHUNK, exception_on_overflow = False)
      print(len(input))
      sig =[]
      sig = np.frombuffer(input, dtype="int16") / 32768
      now_dt = datetime.datetime.now() #今の時間を取得
      fileName = now_dt.isoformat()
      savewav(sig,fileName)

      filepath = "./data/sample_"+fileName+".wav" # your audiofile
      y, sr = librosa.load(filepath)
      f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))
      times = librosa.times_like(f0)

      df_f0 = pd.Series(f0)
      df_f0 = df_f0.dropna(how='all')
      print(df_f0.describe())

      output = stream.write(input)
		
  except KeyboardInterrupt: ## ctrl+c で終了
		  break

stream.stop_stream()
stream.close()
audio.terminate()