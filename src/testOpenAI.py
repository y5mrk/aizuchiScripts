import os
import openai
openai.organization = "org-pdCw9g7lFMPWmKG46qtGZhJi"
openai.api_key = "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"
openai.Model.list()

completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "あなたは友達のように、ユーザの日常について、簡潔に質問するアシスタントです。"},
    {"role": "user", "content": "「暑い」に関して何か1つ話題を振ってください"}
  ]
)

print(completion.choices[0].message)