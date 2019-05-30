#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 参考: https://qiita.com/ynakayama/items/2cc0b1d3cf1a2da612e4

from __future__ import print_function
from flask import Flask, render_template, request, redirect, url_for
import numpy as np
import commands
# LDAの処理コマンドに入力テキストのパスを指定して実行する予定(詳細は, Lda.pyの中身を参照のこと)
#from ../LexRank/su mmpy.summpy.Lda_input_text import lda

# 自身の名称を app という名前でインスタンス化する
app = Flask(__name__)

# メッセージをランダムに表示するメソッド
def picked_up():
    messages = [
        "こんにちは、あなたの名前を入力してください",
        "やあ！お名前は何ですか？",
        "あなたの名前を教えてね"
    ]
    # NumPy の random.choice で配列からランダムに取り出し
    return np.random.choice(messages)

# 以下, アプリケーション用のルーティングを記述していく

# "/"(index)にアクセスしたときの処理
@app.route("/")
def index():
    title = u"ようこそ"
    message = picked_up()
    # index.htmlをテンプレーティングする. ※日本語を使うなら, decode('utf-8')せんと使えない
    #return render_template('hoge.html', message = u"ほげ", title = u"ふが")
    return render_template("index.html", message = message.decode("utf-8"), title = title)
    #return "Hello World!<br>This is powered by Python backend." + message

# "/post"にアクセスしたときの処理
@app.route('/post', methods=['GET', 'POST'])
def post():
    title = u"こんにちは"
    if request.method == 'POST':
        # リクエストフォームから「名前」を取得して
        name = request.form['name']
        # pdfminerコマンドをpdfに実行して, その結果を保持する
        #command_output = commands.getoutput('pdf2txt.py ' + '/Users/ruffy/Downloads/ipsj2001t.pdf' + ' ' + '| tr -d "　" | tr -d "," | tr -d " " | tr -d ")" | tr -d "("')
        command_output = commands.getoutput('pdf2txt.py ' + name.encode("utf-8") + ' ' + '| tr -d "　" | tr -d "," | tr -d " " | tr -d ")" | tr -d "("')

        # index.html をテンプレーティングする
        #return render_template('index.html',
        #                       name = name, title = title)
        return render_template('index.html',
                               name = command_output.decode("utf-8"), title = title)
    else:
        # エラーなどでリダイレクトしたい場合はこんな感じで
        return redirect(url_for('index'))

if __name__ == "__main__":
    print('on hello')
    app.debug = True
    app.run(host="127.0.0.1", port=5000)