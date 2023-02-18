from django.shortcuts import render
from django.views import View
from .utils import chat_gpt, create_prompt, mk_html # mk_htmlを追加


# Create your views here.
class GrammarCorrectionView(View):
    
    def get(self, request):
        
        return render(request, 'proofreading/grammar_correction.html')
    
    def post(self, request):
        
        # 画面に入力した文章を取得
        input_text= request.POST['input_text']
        if input_text:
            # Chat-GPTに投げる命令文を生成
            prompt = create_prompt(input_text, "GrammarCorrection.txt")
            # Chat-GPTへリクエストを投げる
            response = chat_gpt(prompt)
            # htmlデータを生成
            response = mk_html(input_text,response)  #追加
            # 辞書型データを作成する
            context = {'input_text': input_text,
                    'response': response,
                    }

            # テンプレートにデータを渡す
            return render(request, 'proofreading/grammar_correction.html', context)
        else:
            return render(request, 'proofreading/grammar_correction.html')    
