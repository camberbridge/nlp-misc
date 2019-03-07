# coding: utf-8

import json, sys
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

def program2vec():
    m = Doc2Vec.load("./doc2vec.model")

    return m

def similarities_inference(m, doc_id, _topn):
    """
    - input: A document used for learning.
    - Get most a similar doc between parameter(doc ID = tags num) and all docs.
    - return: _topn(default: 10) similarity docs(e.g. [(3, 0.999999), (5, 0.98223333), ...]
    """
    return m.docvecs.most_similar(doc_id, topn=_topn)

def any_similarities_inference(m, doc_id1, doc_id2):
    """
    - input: Documents used for learning.
    - return: Degree of similarity(float)
    """
    return m.docvecs.similarity(doc_id1, doc_id2)

def addition(m, positive_list):
    """
    - input: A list.
    - return: A addition result.
    """
    return m.docvecs.most_similar(positive = positive_list)

def subtraction(m, positive_list, negative_list):
    """
    - input: A list of doc num x2.
    - return: A subtraction result.
    """
    return m.docvecs.most_similar(positive = positive_list, negative = negative_list)

def formatting(l):
    tv = l[3]
    txt = l[6]
    rating = l[5]
    ch = l[4]
    time = l[0] + "-" + l[1]
    return tv, rating, time, ch, txt

if __name__ == "__main__":
    # 0-3
    types = int(sys.argv[1])

    model = program2vec()

    with open("texts/tv_program.json", "r") as f:
        tv_program = json.load(f)

    result_list = []
    with open("files.txt", "r") as f:
        counter = 0
        for l in f:
            #print(counter, l.split()[8], tv_program[l.split()[8].replace(".txt", "")])
            result_list.append(tv_program[l.split()[8].replace(".txt", "")] + [l.split()[8]])
            counter += 1

    topn = 10

    if types == 0:
        """
        - Most sim infer.
        - arg: e.g. N
        """
        param = int(sys.argv[2])
        result = formatting(result_list[param])

        print("\n")
        print("A most sim to ", result, " are ")
        for c in similarities_inference(model, [param], topn):
            print(c[1], formatting(result_list[c[0]]))
        print("\n") 

        print("==============")

        """
        - Most dissim infer.
        - arg: e.g. N
        """
        print("\n") 
        print("A most dissim to ", formatting(result_list[param]), " are ")
        dissim_list = similarities_inference(model, [param], _topn=len(result_list))
        dissim_list.reverse()
        for c in dissim_list[:topn]:
            print(c[1], formatting(result_list[c[0]]))
        print("\n")
        
    elif types == 1:
        """ 
        - Most sim between doc1 and doc2.
        - arg: e.g. N M
        """
        params1 = int(sys.argv[2])
        params2 = int(sys.argv[3])
        result1 = formatting(result_list[params1])
        result2 = formatting(result_list[params2])

        print("\n")
        print("Similarity between")
        print(result1)
        print("and")
        print(result2)
        print(any_similarities_inference(model, params1, params2))
        print("\n") 
    elif types == 2:
        """
        - Addition
        - arg: e.g. N M L K
        """
        positive_list = []
        print("\n")
        print("Addition: ")
        for i in xrange(2, len(sys.argv)):
            positive_list.append(int(sys.argv[i]))
            print(formatting(result_list[int(sys.argv[i])]))
        print("≒")
        for c in addition(model, positive_list):
            print(c[1], formatting(result_list[c[0]]))
        print("\n")
    elif types == 3:
        """
        - Subtraction
        - arg: e.g. N,M,L K,J
        """
        positive_list = []
        negative_list = []
        _positive_list = sys.argv[2].split(",")
        _negative_list = sys.argv[3].split(",") 
        print("\n")
        print("Calculate: ")
        for index in _positive_list:
            print("+", formatting(result_list[int(index)]))
            positive_list.append(int(index))
        for index in _negative_list:
            print("-", formatting(result_list[int(index)]))
            negative_list.append(int(index))
        print("≒")
        for c in subtraction(model, positive_list, negative_list):
            print(c[1], formatting(result_list[c[0]]))
        print("\n")
