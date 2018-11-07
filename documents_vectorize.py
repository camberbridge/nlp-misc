# coding: utf-8

from gensim import corpora, models, similarities
from word_counter import main
import sys

def document_vectorize(text):
    """
    - For a doc.
    - text: Separated by every lines for a doc (Input is one file.
    """

    with open(text, "r") as f:
        sentences = f.read()
        return main(sentences)

def documents_vectorize(text):
    """
    - For docs.
    - text: Separated by every doc for docs (Input is one file).
    """

    with open(text, "r") as f:
        sentences = f.read()
        splitted_document_WAKATIlist, _ = main(sentences, aggregate_flag = False, is_doc_or_docs = False)
        return splitted_document_WAKATIlist

if __name__ == "__main__":
    print(documents_vectorize(sys.argv[1]))
