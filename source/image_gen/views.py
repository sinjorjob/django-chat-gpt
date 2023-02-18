from django.shortcuts import render
from django.views import View
from .utils import chat_gpt, create_prompt, stable_diffusion
import io, base64
from django.http import JsonResponse


class CreateImageView(View):
    
    def get(self, request, *args, **kwargs):

        return render(request, 'image_gen/create_image.html')
    
    def post(self, request, *args, **kwargs):

        input_sentence = request.POST.get('input_sentence', None)  #画面で入力した説明文を取得
        print("input_sentence=", input_sentence)
        if input_sentence: 
            # Chat-GPTに投げる命令文を生成
            prompt = create_prompt(input_sentence, "CreateImage.txt")
            response = chat_gpt(prompt)  # Chat-GPTから回答を取得する。
            tranlate_sentence  = "次の文章を日本語に翻訳してください。\n" + response
            response_jp = chat_gpt(tranlate_sentence)   # chat-gptで日本語に変換
            image = stable_diffusion(response)   # 画像生成処理を実行する。
            # 画像データをエンコード
            buffer = io.BytesIO()
            image.save(buffer, format="PNG") # <class 'PIL.Image.Image'>
            img_str = base64.b64encode(buffer.getvalue())  # <class 'bytes'> img_str= b'iVBORw~~~~
            img_str = str(img_str)[2:-1]   # img_strの先頭にある「b'」を除外する。            
            translated_img = 'data:' + 'image/jpeg' + ';base64,' + img_str

            context = {
                'input_sentence':input_sentence,
                'response': response_jp,
                'img_str' : translated_img,
                }
            return JsonResponse(context)
        else:
            return render(request, 'image_gen/create_image.html')