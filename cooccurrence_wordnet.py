# coding: utf-8

from misc.mecab_segmenter import word_segmenter_ja
import sys
import os
import itertools
import collections
import numpy as np
from collections import Counter
from sklearn.feature_extraction import DictVectorizer
import math
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import json

def plot_network(data, edge_threshold=0., fig_size=(8, 8), file_name=None, dir_path=None, w_score_dict=None):
    nodes = list(set(data['node1'].tolist()+data['node2'].tolist()))
    G = nx.Graph()

    #  頂点の追加
    G.add_nodes_from(nodes)
    #  辺の追加
    for i in range(len(data)):
        row_data = data.iloc[i]
        if row_data['value'] > edge_threshold:
            G.add_edge(row_data['node1'], row_data['node2'], weight=row_data['value'])

    # 孤立したnodeを削除
    isolated = [n for n in G.nodes if len([i for i in nx.all_neighbors(G, n)]) == 0]
    for n in isolated:
        G.remove_node(n)

    plt.figure(figsize=fig_size)
    pos = nx.spring_layout(G, k=0.3)  # k = node間反発係数
    pr = nx.pagerank(G)

    # nodeの大きさ
    if w_score_dict != None:
        for w, s in pr.items():
            try: 
                pr[w] = w_score_dict[w]
            except Exception as e:
                print(e)
                print(w)
    size_weight = 5000
    nx.draw_networkx_nodes(G, pos, node_color=list(pr.values()),
                           cmap=plt.cm.Reds,
                           alpha=0.7,
                           node_size=[v*size_weight for v in pr.values()])

    # 日本語ラベル
    nx.draw_networkx_labels(G, pos, fontsize=12, font_family='YuGothic', font_weight="bold")

    # エッジの太さ調節
    thickness_weight = 1
    edge_width = [d["weight"] * thickness_weight for (u, v, d) in G.edges(data=True)]
    nx.draw_networkx_edges(G, pos, alpha=0.4, edge_color="darkgrey", width=edge_width)
    plt.axis('off')

    if file_name is not None:
        if dir_path is None:
            dir_path = Path('.').joinpath('image')
        if not dir_path.exists():
            dir_path.mkdir(parents=True)
        plt.savefig(dir_path.joinpath(file_name), bbox_inches="tight")

    plt.show()
    #plt.savefig("hoge.png")

def by_counter_dictvectorizer(document_list):
    tf = Counter(document_list)
    v = DictVectorizer(sort=False)
    X = v.fit_transform(tf)
    v.fit_transform(tf).toarray()
    return X, v.get_feature_names()

def word_set(sentences):
    sentence_combinations = [list(itertools.combinations(sentence, 2)) for sentence in sentences]
    sentence_combinations = [[tuple(sorted(words)) for words in sentence] for sentence in sentence_combinations]
    return sentence_combinations

def cal_p_xy(line_list):
    combination = word_set(line_list)
    target_comb = []
    for c in combination:
        target_comb.extend(c)
    p_xy = collections.Counter(target_comb)

    return dict(p_xy)

def cal_tf(line_list):
    fitted_freq, word_list = by_counter_dictvectorizer([j for sub in line_list for j in sub])
    freq_list = fitted_freq.toarray()
    tf_dict = {}
    for w, f in zip(word_list, freq_list[0]):
        tf_dict[w] = f

    return tf_dict

def cal_pmi(p_xy_dict, tf_dict, N):
    pmi_dict = {}
    for xy, xy_score in p_xy_dict.items():
        upper = xy_score * N
        lower = tf_dict[xy[0]] * tf_dict[xy[1]]
        pmi_dict[xy] = math.log(upper/lower, 2)

    return pmi_dict

def sort_dict(dic, reverse=False):
    for k, v in sorted(dic.items(), key=lambda x: -x[1], reverse=reverse):
        print(k, v)

def create_df(dic):
    # Convert dataframe
    word_association  = []
    for k, v in dic.items():
        word_association.append([k[0], k[1], v])
    word_association = pd.DataFrame(word_association, columns=['word1', 'word2', 'value'])

    #n_word_lower = 150
    # word_association.query('count1 >= @n_word_lower & count2 >= @n_word_lower', inplace=True)
    word_association.rename(columns={'word1':'node1', 'word2':'node2'}, inplace=True)

    return word_association

def word_rank(doc_num, f_type):
    if f_type == 0:
        model = np.load("/Users/ruffy/Desktop/ts2text/RandD/models/tfidf_model.npy")
        features = np.load("/Users/ruffy/Desktop/ts2text/RandD/models/tfidf_features.npy")
    elif f_type == 1:
        model = np.load("/Users/ruffy/Desktop/ts2text/RandD/models/saved_model.npy")
        features = np.load("/Users/ruffy/Desktop/ts2text/RandD/models/saved_features.npy")

    dic = {}
    for f, s in zip(features, model[doc_num]):
        if s != 0:
            dic[f] = s

    return dic

def create_doc_dict(doc_num):
    doc_dict = {}  # {"0": ["A", "B", ...,"Z"], ..., "504": ["AA", ...,"zz"]}
    N = 0

    # For N
    def cal_len(list_2d):
        list_len = 0
        if type(list_2d[0]) is list:
            list_len = sum([len(l) for l in list_2d])
        else:
            list_len = len(list_2d)
        return list_len

    if os.path.exists("/Users/ruffy/Desktop/ts2text/RandD/models/doc_dict.json"): 
        with open("/Users/ruffy/Desktop/ts2text/RandD/models/doc_dict.json", "r") as f:
            doc_dict = json.load(f)
            list_2d = doc_dict[str(doc_num)]
            N = cal_len(list_2d)

        return list_2d, N
    else:
        counter = 0
        with open("document_set.txt", "r") as f:
            for l in f:
                line_list = []

                for line in l.split("."):
                    line_words = word_segmenter_ja(line)

                    if len(line_words) >= 2:  # Freq 0 word measures.
                        line_list.append(line_words)

                doc_dict[str(counter)] = line_list
                counter += 1

            with open("doc_dict.json", "w") as f:
                json.dump(doc_dict, f, indent=4, sort_keys=True, separators=(',', ': '))

        return doc_dict[str(doc_num)], cal_len(doc_dict[str(doc_num)])

if __name__ == "__main__":
    doc_num = 0

    line_list, N = create_doc_dict(doc_num)

    # Feature value
    f_type = 0  # 0: TF-IDF, 1: BM25
    feature_dict = word_rank(doc_num, f_type)

    # Calculate P(X, Y)
    p_xy_dict = cal_p_xy(line_list)
    # Calculate P(X), P(Y) as TF
    tf_dict = cal_tf(line_list)
    # Calculate PMI
    pmi_dict = cal_pmi(p_xy_dict, tf_dict, N)

    # Plot net
    word_association = create_df(p_xy_dict)
    #word_association.to_csv("./models/word_associaation.csv", encoding="utf8")
    edge_threshold = 1  # For pruning. If TF: 1<, else: N<
    plot_network(data=word_association, edge_threshold=edge_threshold, w_score_dict=feature_dict)
