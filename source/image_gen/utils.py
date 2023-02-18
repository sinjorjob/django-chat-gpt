
import openai
import os
from django.conf import settings
from diffusers import StableDiffusionPipeline

APK_KEY = "APIKEYをセット"
MODEL_ID = "prompthero/midjourney-v4-diffusion"
DEVICE = "cpu"


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


def null_safety(images, **kwargs):
    return images, False


def stable_diffusion(prompt):
    pipe = StableDiffusionPipeline.from_pretrained(MODEL_ID)
    pipe = pipe.to(DEVICE)
    pipe.safety_checker = null_safety
    image = pipe(prompt).images[0]
    return image



 
 


