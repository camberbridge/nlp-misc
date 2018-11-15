# coding: utf-8

import os, glob


def listup_files():
    return glob.glob("./texts/*.txt")

def doc_gen():
    for p in listup_files():
        with open(str(p), "r") as f:
            #print(f.read().replace("\n", "."))
            with open("document_set.txt", "a") as ff:
                ff.write(f.read().replace("\n", ".") + "\n")

if __name__ == "__main__":
    doc_gen()
