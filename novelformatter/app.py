from dotenv import load_dotenv
import os
from flask import Flask, render_template, request
import openai

app = Flask(__name__)

def load_api_key():
    # .env ファイルを読み込む
    load_dotenv()
    # 環境変数から API キーを取得する
    return os.getenv('OPENAI_API_KEY')

def format_novel(input_text):
    # OpenAI APIを使用してテキスト処理を行う
    response = openai.Completion.create(
        engine="text-davinci-003",  # 使用するGPT-3モデル
        prompt=input_text,  # 入力テキスト
        max_tokens=2000,  # 出力テキストの最大トークン数
        temperature=0.8,  # 出力の多様性を制御する温度パラメータ
    )
    return response.choices[0].text.strip()  # 処理結果のテキストを取得

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/format', methods=['POST'])
def format():
    prompt = request.form['prompt']  # プロンプト入力欄の内容を取得
    text = request.form['text']  # 本文入力欄の内容を取得
    input_text = prompt + ' ' + text  # プロンプトと本文を結合してAPIに渡すテキストを作成

    formatted_novel = format_novel(input_text)  # APIにテキストを渡して処理結果を取得
    return render_template('result.html', formatted_novel=formatted_novel)

if __name__ == '__main__':
    # APIキーの読み込み
    openai.api_key = load_api_key()

    app.run(debug=True)
