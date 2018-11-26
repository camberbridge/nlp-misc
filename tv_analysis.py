# coding: utf-8

import json, sys
from gensim.models.doc2vec import Doc2Vec, TaggedDocument

def program2vec():
    m = Doc2Vec.load("./doc2vec.model")

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

    if types == 0:
        """
        - Most sim infer.
        - arg: e.g. 0
        """
        param = int(sys.argv[2])
        print("\n")
        print("A most sim to ", result_list[param][3:], " are ")
        for c in similarities_inference(model, [param]):
            print(c[1], result_list[c[0]][3:])
        print("\n") 
    elif types == 1:
        """ 
        - Most sim between doc1 and doc2.
        - arg: e.g. 0 1
        """
        params1 = int(sys.argv[2])
        params2 = int(sys.argv[3])
        print("\n")
        print("Similarity between")
        print(result_list[params1][3:])
        print("and")
        print(result_list[params2][3:])
        print(any_similarities_inference(model, params1, params2))
        print("\n") 
    elif types == 2:
        """
        - Addition
        - arg: e.g. 0 1 2 3 4
        """
        positive_list = []
        print("\n")
        print("Addition: ")
        for i in xrange(2, len(sys.argv)):
            positive_list.append(int(sys.argv[i]))
            print(result_list[int(sys.argv[i])])
        print("≒")
        for c in addition(model, positive_list):
            print(c[1], result_list[c[0]][3:])
        print("\n")
    elif types == 3:
        """
        - Subtraction
        - arg: e.g. 1,2,3,4,5 6,7,8,9
        """
        positive_list = []
        negative_list = []
        _positive_list = sys.argv[2].split(",")
        _negative_list = sys.argv[3].split(",") 
        print("\n")
        print("Calculate: ")
        for index in _positive_list:
            print("+", result_list[int(index)][3:])
            positive_list.append(int(index))
        for index in _negative_list:
            print("-", result_list[int(index)][3:])
            negative_list.append(int(index))
        print("≒")
        for c in subtraction(model, positive_list, negative_list):
            print(c[1], result_list[c[0]][3:])
        print("\n")
