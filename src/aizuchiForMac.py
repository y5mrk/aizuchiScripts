import urllib.request, urllib.error
from bs4 import BeautifulSoup
import subprocess
import random
import logging
import time
import speech_recognition as sr

isPlaying = True

def aizuchi():
    aizuchi_list = ['うん', 'うんうん', 'へー', 'ふーん', 'うん、うん']
    text = random.choice(aizuchi_list)
    say(text)
    return

def interval():
    sleepTime = random.uniform(1.5, 10)
    print(sleepTime)
    time.sleep(sleepTime)

def say(text):
    subprocess.call('say "%s"' % text, shell=True)

def stop():
    isPlaying = False
    print(isPlaying)

def listen():
  r = sr.Recognizer()
  with sr.Microphone(sample_rate=16_000) as source:
      print("なにか話してください")
      audio = r.listen(source)
      print("音声を取得しました")
  try:
      recognized_text = r.recognize_google(audio, language='ja-JP')
      print(recognized_text)
      aizuchi()
  except sr.UnknownValueError:
      print("認識できませんでした")

if __name__ == "__main__":
  while True:
    if isPlaying:
        listen()
        # print('Conversation started!')
        # interval()
        # aizuchi()
    else:
        print('Press button to start conversation...')
