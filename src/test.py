import wave
import numpy as np
import pyaudio # 鳴らすとき使う
import struct # バイナリデータを扱うとき使う

f = 440 # 周波数
fs = 44100 # サンプリング周波数(CD)
sec = 3 # 時間

t = np.arange(0, fs * sec) # 時間軸の点をサンプル数用意
sine_wave = np.sin(2 * np.pi * f * t / fs)

max_num = 32767.0 / max(sine_wave) # int16は-32768~32767の範囲
wave16 = [int(x * max_num) for x in sine_wave] # 16bit符号付き整数に変換

# バイナリ化，'h'が2byte整数のフォーマット
bi_wave = struct.pack("h" * len(wave16), *wave16)

# サイン波をwavファイルとして書き出し
w = wave.Wave_write('src/data/sine440.wav')

# (チャンネル数(1:モノラル,2:ステレオ))
# サンプルサイズ(バイト)
# サンプリング周波数
# フレーム数
# 圧縮形式(今のところNONEのみ)
# 圧縮形式を人に判読可能な形にしたもの？通常、'NONE'に対して'not compressed'が返される)
p = (1, 2, fs, len(bi_wave), 'NONE', 'not compressed')
w.setparams(p)
w.writeframes(bi_wave)
w.close()