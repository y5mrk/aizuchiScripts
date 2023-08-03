import whisper
import wave
import MeCab
import os
import openai
import urllib.parse
from dotenv import load_dotenv

load_dotenv()
openai.organization = os.environ['API_ORG']
openai.api_key = os.environ['API_KEY']
openai.Model.list()

def join_waves(inputs, output):
    '''
    inputs : list of filenames
    output : output filename
    '''
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
        print("エラー")

    except Exception:
        print('unexpected error')

def analyse(text):
    tagger = MeCab.Tagger()
    node = tagger.parseToNode(text)
    terms = []

    while node:
        term = node.surface
        pos = node.feature.split(',')[0]
        
        if pos == '名詞':
          if term != '?':
            terms.append(term)

        node = node.next
    
    print("名詞：%sを検出" % terms)

    if len(terms) > 1:
      completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
          {"role": "system", "content": "あなたは友達のように、ユーザの日常について、簡潔に質問するアシスタントです。"},
          {"role": "user", "content": "「"+ terms[0] +"」「" + terms[1] + "」に関して何か1つ話題を振ってください"}
        ]
      )

      print(completion.choices[0].message.content)
      question = urllib.parse.unquote_to_bytes(completion.choices[0].message.content)
      print(question.decode('utf-8'))

if __name__ == '__main__':
    # inputs = ['./data/sample_2023-07-31T09:04:08.395652.wav', './data/sample_2023-07-31T09:04:08.848872.wav', './data/sample_2023-07-31T09:04:09.219620.wav', './data/sample_2023-07-31T09:04:09.648862.wav', './data/sample_2023-07-31T09:04:12.818426.wav', './data/sample_2023-07-31T09:04:13.226912.wav', './data/sample_2023-07-31T09:04:13.641956.wav', './data/sample_2023-07-31T09:04:14.117327.wav', './data/sample_2023-07-31T09:04:14.642688.wav', './data/sample_2023-07-31T09:04:14.986939.wav', './data/sample_2023-07-31T09:04:15.286424.wav', './data/sample_2023-07-31T09:04:15.609611.wav', './data/sample_2023-07-31T09:04:15.942428.wav', './data/sample_2023-07-31T09:04:16.295658.wav', './data/sample_2023-07-31T09:04:16.747996.wav', './data/sample_2023-07-31T09:04:17.164935.wav', './data/sample_2023-07-31T09:04:17.702540.wav', './data/sample_2023-07-31T09:04:18.123290.wav', './data/sample_2023-07-31T09:04:18.511959.wav', './data/sample_2023-07-31T09:04:18.954710.wav', './data/sample_2023-07-31T09:04:19.304141.wav', './data/sample_2023-07-31T09:04:19.757831.wav', './data/sample_2023-07-31T09:04:20.184153.wav', './data/sample_2023-07-31T09:04:20.517585.wav', './data/sample_2023-07-31T09:04:20.827779.wav', './data/sample_2023-07-31T09:04:21.132559.wav', './data/sample_2023-07-31T09:04:21.494974.wav', './data/sample_2023-07-31T09:04:21.924451.wav']
    # output = './data/sample.wav'
    # join_waves(inputs, output)

    model = whisper.load_model("base")
    result = model.transcribe("./data/sample.wav")
    print(result["text"])
    analyse(result["text"])