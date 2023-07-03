import speech_recognition as sr
import MeCab
import subprocess
import random

r = sr.Recognizer()
mic = sr.Microphone()

def say(text):
    print("相槌: %s" % text)
    subprocess.call('say "%s"' % text, shell=True)

def aizuchi():
    aizuchi_list = ['うん', 'うんうん', 'へー', 'ふーん']
    text = random.choice(aizuchi_list)
    say(text)
    return

def analyse(text):
    tagger = MeCab.Tagger()
    node = tagger.parseToNode(text)
    terms = []

    while node:
        term = node.surface
        pos = node.feature.split(',')[1]
        
        if pos == '終助詞':
            terms.append(term)

        node = node.next
    
    print("終助詞を%sつ検出" % len(terms))

    if len(terms) > 0:
      aizuchi()

while True:
    print("話してください")

    with mic as source:
        r.adjust_for_ambient_noise(source) #雑音対策
        audio = r.listen(source)

    print ("音声認識しています")

    try:
        sprec_text = r.recognize_google(audio, language='ja-JP')
        print(sprec_text)
        analyse(sprec_text)

    # 以下は認識できなかったときに止まらないように。
    except sr.UnknownValueError:
        print("音声認識できませんでした")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
    except KeyboardInterrupt:
        break
