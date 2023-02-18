
import openai
import os
from django.conf import settings
import difflib

APK_KEY = "APIKEYをセット"

def chat_gpt(prompt):
    openai.api_key = APK_KEY #API KEYをセット
    openai.Model.list() #OpenAIのインスタンスを生成
  
    #APIを使ってリクエストを投げる
    response = openai.Completion.create(
    model = "text-davinci-003",
    prompt= prompt,
    temperature=0,
    max_tokens=300,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=0.0

    )
    response = (response["choices"][0]["text"]).strip()
    return response 


def create_prompt(input_text, file_name):
    prompt_file = os.path.join(settings.BASE_DIR, 'template', file_name)
    with open(prompt_file, encoding="utf-8") as f:
        file_read = f.read()
    #Chat-GTPへ投げるフォーマットに入力文をセットする。
    prompt = file_read.replace("[input]", input_text)
    return prompt


def highlight(word, identifier):
    """
    質問文と回答文の差異を可視化する
    追加された部分→ 背景を黄色＆アンダーラインを引く
    削除された部分→ 取り消し線を引く
    """
    if identifier == '+':
        return '<span class="lint-mark-warning">{}</span>'.format(word)
    elif identifier == '-':
        return '<span class="lint-mark-del">{}</span>'.format(word)
    


def mk_html(question, response):
    
    #HTMLデータを作成する
    html = ''
    for difference_data in difflib.ndiff(question, response):
        if difference_data[0]==' ':
            html += difference_data[2]
        elif difference_data[0]=='+':
            html += highlight(difference_data[2], '+')
        elif difference_data[0] == '-':
            html += highlight(difference_data[2], '-')
    return html


