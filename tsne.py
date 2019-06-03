# coding: utf-8

import sys, os
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from documents_vectorize import documents_wakati
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import pandas as pd
import numpy as np
import matplotlib

font = {'family' : 'YuGothic'}
matplotlib.rc('font', **font)


def program2vec(separated_document_list):
    # Learn a model
    if os.path.exists("./improveD2V.model"):
        m = Doc2Vec.load("./improveD2V.model")
    else:
        # Create training data
        train_data = [TaggedDocument(words = line, tags = [i]) for i, line in enumerate(separated_document_list)]

        # vector_size: A dimension num of a compression vector
        m = Doc2Vec(documents = train_data, dm = 1, vector_size=300, window=8, min_count=10, workers=4)
        m.save("./improveD2V.model")

    return m

def w2t(m, emb_tuple, words_list, word_counter):
    skip = 0
    limit = word_counter  # Upper limit of word num.

    X = np.vstack(emb_tuple)
    print(X.shape)

    model = TSNE(n_components=2, random_state=0)
    np.set_printoptions(suppress=True)
    model.fit_transform(X) 

    plt.figure(figsize=(8, 6))  # Figure size.
    x_list = model.embedding_[skip:limit, 0]
    y_list = model.embedding_[skip:limit, 1]
    plt.scatter(x_list, y_list)

    count = 0
    for label, x, y in zip(words_list, model.embedding_[:, 0], model.embedding_[:, 1]):
        count +=1
        if(count<skip):continue
        plt.annotate(label, xy=(x, y), xytext=(0, 0), textcoords='offset points')
        if(count==limit):break

    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()
    

if __name__ == "__main__":
    separated_document_list = documents_wakati(sys.argv[1])

    model = program2vec(separated_document_list) 

    # Output any word vec: model[word]
    # Output any doc vec: model.docvecs[document_name(tag)]
    words = separated_document_list[0]
    words_vec = []
    words_list = []
    word_counter = 0
    for w in words:
        try:
            word_vec = model[w]
            words_vec.append(word_vec)
            words_list.append(w)
            word_counter += 1
        except:
            #print("ERROR: ", w)
            words.remove(w)

    w2t(model, tuple(words_vec), words_list, word_counter)
