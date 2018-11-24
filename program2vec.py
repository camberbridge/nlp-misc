# coding: utf-8

import sys, os
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from documents_vectorize import documents_wakati


def program2vec(separated_document_list):
    # Learn a model
    if os.path.exists("./doc2vec.model"):
        m = Doc2Vec.load("./doc2vec.model")
    else:
        # Create training data
        train_data = [TaggedDocument(words = line, tags = [i]) for i, line in enumerate(separated_document_list)]

        # vector_size: A dimension num of a compression vector
        m = Doc2Vec(documents = train_data, dm = 1, vector_size=300, window=8, min_count=10, workers=4)
        m.save("./doc2vec.model")

    return m

def similarities_inference(m, doc_id):
    """
    - input: A document used for learning.
    - Get most a similar doc between parameter(doc ID = tags num) and all docs.
    - return: 10 similarity docs(e.g. [(3, 0.999999), (5, 0.98223333), ...]
    """
    return m.docvecs.most_similar(doc_id)

def any_similarities_inference(m, doc_id1, doc_id2):
    """
    - input: Documents used for learning.
    - return: Degree of similarity(float)
    """
    return m.docvecs.similarity(doc_id1, doc_id2)

def any_similarities_inference_used_unkdocs(m, doc1_words, doc2_words):
    """
    - input: A words list in documents not used for learning.
    - output: Degree of similarity(float)
    """
    return m.docvecs.similarity_unseen_docs(m, doc1_words, doc2_words, alpha=1, min_alpha=0.0001, steps=5)

def dimension_num(m, doc_words):
    """
    - input: A words list in document.
    - return: A compression vector(list)
    """
    return m.infer_vector(doc_words)

def addition(m, *positive):
    """
    - input: A doc num is separated by comma. (e.g. 1, 4, 5)
    - return: A addition result.
    """
    return m.docvecs.most_similar(positive = list(positive))

def subtraction(m, positive_list, negative_list):
    """
    - input: A list of doc num x2.
    - return: A subtraction result.
    """
    return m.docvecs.most_similar(positive = positive_list, negative = negative_list)
    

if __name__ == "__main__":
    separated_document_list = documents_wakati(sys.argv[1])
    model = program2vec(separated_document_list) 

    print(similarities_inference(model, 0))
    print(any_similarities_inference(model, 0, 1))
    print(any_similarities_inference_used_unkdocs(model, separated_document_list[0], separated_document_list[1]))
    print(addition(model, 0, 1, 5, 4))
    print(subtraction(model, positive_list = [0, 100], negative_list = [1, 302, 222]))
