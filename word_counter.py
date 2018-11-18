# coding: utf-8

import collections
from misc import tools
from misc.mecab_segmenter import word_segmenter_ja
import sys


def word_count(sentences, is_doc_or_docs):
    words_list = []
    sent_tf_list = []

    # sentences to TF
    for sent in sentences: 
        words = word_segmenter_ja(sent)

        # For a doc.
        if is_doc_or_docs: 
            words_list.extend(words)
        # For docs.
        else:
            words_list.append(words)
            sent_tf_list.append(collections.Counter(words))

    if is_doc_or_docs: 
        sent_tf_list = collections.Counter(words_list)

    return words_list, sent_tf_list


def main(text, is_doc_or_docs = True):
    # Separate documents by new line. 
    sentences = list(tools.sent_splitter_ja(text))
    return word_count(sentences, is_doc_or_docs)


if __name__ == "__main__":
    with open(sys.argv[1], "r") as f:
        text = f.read()

    print(main(text))
