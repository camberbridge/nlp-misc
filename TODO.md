# TODO
- サブワード, BERTを使っての構成要素の精度向上

# 施策
- 単語のベクトル表現による番組の定性表現
  - doc2vec(skip-gram model)
- 番組構成要素の導出
  - トピックモデル(LDA)

# テキスト集合生成 
- python doc_gen.py
  - textsディレを作っておく

# テキスト集合(document_set.txt)に対する前処理 
| tr -d "（" | tr -d "）" | tr -d "『" | tr -d "』" | tr -d "→" | tr -d "☆" | tr -d "〈" | tr -d "〉" | tr -d "・"

# What I did[1]
- HDP-LDAをつかって、文書集合のトピックを150個(トピックとそれを構成する単語集合)抽出。そして各文書のトピックを抽出。
- 話し言葉なので、代名詞、指示名詞が多い。あとは量をあらわす副詞が多い
- 解析方法
  - python documents_vectirize.py document_set.txt | ud > hoge.txt
  - hoge.txtにトピックと文書に包含されるトピックが出るの(N番目は0スタート)
  - documents_vectrize.pyはtexts/配下のファイルを名前順にsort(ls -la)した順番なので、N番目はこのときの順番に対応する
  - N番目にあるファイル名が対象のファイルなので、該当ファイルのトピックがN番目の結果となる

# What I did[2]
- Doc2Vecをつかって、番組のベクトル表現&類似度の高い番組を抽出
  - 方法：パラメタの数字+1がtexts/配下のファイルを名前順にsort(ls -la)したときの順番に対応
  - python program2vec.py document_set.txt
    - モデル生成される
- 番組の足し引き算をできるようにした
  - python tv_analysis params

# What I did[3]
- バラエティ番組は雑多な内容が多いので難しい
- テキストファイルとプログラムの出力を整合するプログラムを準備する
- LDAとDoc2Vecの計算結果をJSONに書き込んで読み込むだけにする

# Discovery
- LDAはmecab-ipa-dicの方がいい感じで、Doc2Vecはipa-dicの方がいい感じ. だぶん、Doc2Vecは単語が細かい方が精度がいい気がする
- LDAする際にgensimでextream_fileterをしないと「行く」「食べる」などの一般的すぎる動詞がめちゃめちゃでてくる
- LDA20-2-0.3が上位概念で、HDP-LDAの2-0.3が下位詳細という使い合わせをする
  - 構成要素はLDAによるとXXXで、より詳細に言うとHDP-LDAによるとYYYてきな
