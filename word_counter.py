# coding: utf-8

import collections
from misc import tools
from misc.mecab_segmenter import word_segmenter_ja
import sys


def word_count(sentences):
    # sentence -> tf every line.
    sent_tf_list = []
    for sent in sentences:
        words = word_segmenter_ja(sent)
        tf = collections.Counter(words)
        sent_tf_list.append(tf)

    return sent_tf_list


def main(text):
    sentences = list(tools.sent_splitter_ja(text))  # Separate documents by new line.
    return word_count(sentences)


if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        text = f.read()

    print(main(text))
