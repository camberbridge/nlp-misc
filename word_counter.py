# coding: utf-8

import collections
from misc import tools
from misc.mecab_segmenter import word_segmenter_ja
from gensim import corpora, models, similarities
import sys


def word_count(sentences):
    words_list = []
    sent_tf_list = {}

    # sentences to TF
    for sent in sentences:
        words = word_segmenter_ja(sent)
        words_list.extend(words)

    sent_tf_list = collections.Counter(words_list)

    return sent_tf_list


def main(text):
    # Separate documents by new line. 
    sentences = list(tools.sent_splitter_ja(text))
    return word_count(sentences)


if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        text = f.read()

    print(main(text))
