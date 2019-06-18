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
from collections import Counter, defaultdict
from array import array
from scipy.sparse import csr_matrix
from bm25 import BM25Transformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import json


def by_countvectorizer(documents):
    vocabulary = defaultdict()
    vocabulary.default_factory = vocabulary.__len__
    j_indices = array('i')
    indptr = array('i')
    indptr.append(0)

    for document in documents:
        for word in document:
            j_indices.append(vocabulary[word])
        indptr.append(len(j_indices))

    j_indices = np.frombuffer(j_indices, dtype=np.intc)
    indptr = np.frombuffer(indptr, dtype=np.intc)
    values = np.ones(len(j_indices))

    X = csr_matrix((values, j_indices, indptr),
                   shape=(len(indptr) - 1, len(vocabulary)))
    X.sum_duplicates()

    return X

def by_counter_dictvectorizer(documents):
    tf_list = []
    for document in documents:
        tf = Counter(document)
        tf_list.append(tf)

    v = DictVectorizer(sort=False)
    X = v.fit_transform(tf_list)

    v.fit_transform(tf_list).toarray()

    return X, v.get_feature_names()

def tf_idf(X):
    # normalizeはl2で、sublinear_tfも使う設定で実行してみる
    tfidf_transformer = TfidfTransformer(norm='l2', sublinear_tf=True)
    tfidf = tfidf_transformer.fit_transform(X)
    return tfidf

if __name__ == "__main__":
    """
    # lil_matrix(from scipy import sparse)
    - To numpy.ndarray: toarray()
    - To numpy.matrix: todense()
    - To csr_matrix: tocsr()
    - To csc_matrix: tocsc()
    # Model: row: sample(doc), column: feature
    """

    # Calculate Rank
    #model = np.load("saved_model.npy")
    model = np.load("tfidf_model.npy")
    #features = np.load("saved_features.npy")
    features = np.load("tfidf_features.npy")
    def calculate_rank(doc_num):
        """
        - return: ["a", "b", ..., "z"]
        """
        li = []
        for feature, score in zip(features, model[doc_num]):
            if score > 0:
                li.append([feature, score])

        return map(lambda x: x[0], sorted(li,key=lambda l:l[1], reverse=True)[:10])

    json_data = {}
    for i in range(504):
        json_data[str(i)] = calculate_rank(i)

    with open("tfidf.json", "w") as f:
        json.dump(json_data, f, indent=4, sort_keys=True, separators=(',', ': '))

    """
    # with TF-IDF
    separated_document_list = documents_wakati(sys.argv[1])

    X, feature_list = by_counter_dictvectorizer(separated_document_list)

    X_tfidf = tf_idf(X)
    X_tfidf = X_tfidf.toarray()  # ndarray

    np.save("tfidf_model", X_tfidf)
    np.save("tfidf_features", feature_list)
    """

    """
    # with TF-IDF
    separated_document_list = documents_wakati(sys.argv[1])

    # Document-Term Matrix
    #X = by_countvectorizer(separated_document_list)  # csr
    X, feature_list = by_counter_dictvectorizer(separated_document_list)

    # Calculate BM25 from DTM
    bm = BM25Transformer()
    bm.fit(X)
    X_bm25 = bm.transform(X)

    X_bm25 = X_bm25.toarray()  # ndarray

    np.save("saved_model", X_bm25)
    np.save("saved_features", feature_list)
    """
