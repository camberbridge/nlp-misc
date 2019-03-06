# coding: utf-8

import json, sys

class pycolor:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    END = '\033[0m'
    BOLD = '\038[1m'
    UNDERLINE = '\033[4m'
    INVISIBLE = '\033[08m'
    REVERCE = '\033[07m'

if __name__ == "__main__":
    program_id = sys.argv[1]

    with open("texts/tv_program.json", "r") as f:
        tv_program = json.load(f)

    result_list = []
    with open("files.txt", "r") as f:
        counter = 0
        for l in f:
            #print(counter, l.split()[8], tv_program[l.split()[8].replace(".txt", "")])
            result_list.append(tv_program[l.split()[8].replace(".txt", "")] + [l.split()[8]])
            counter += 1

    # 上位概念≒概略
    with open("./models/lda20_2_30per.json", "r") as f:
        tv_elem = json.load(f)
        print("\n")
        print(result_list[int(program_id)][3:])
        print(pycolor.RED + "=== includes =>>>" + pycolor.END)
        print("構成概略")
        print(tv_elem[program_id])
        
    # 下位概念≒詳細
    with open("./models/hdplda_2_30per.json", "r") as f:
        tv_elem = json.load(f)
        print("構成詳細")
        print(tv_elem[program_id])
        print("\n")
