# coding:utf-8
# 命令行参数传递，例如输入: python <文件名>.py -help
# 这个结果就会打印help
# sys.argv[0]代表"文件名",第一个参数是sys.argv[1]
import sys
import json


def load_json(json_file):
    with open(json_file, "r")as load_f:
        data = json.load(load_f)
        return data


def store(data, outfile):
    with open(outfile, 'w') as json_file:
        json_file.write(json.dumps(data))


def summary(string):
    all_set = set()
    for i in range(7):
        file = "word_" + string + str(i) + ".txt"
        with open(file, "r", encoding="utf-8")as inp:
            words = inp.read().strip().split()
            all_set |= set(words)
    with open("word_all_" + string + ".txt", "wb", 0) as outp:
        for i in all_set:
            outp.write((i + "\n").encode("utf-8"))


if __name__ == "__main__":
    '''
    argument = sys.argv[1]  # 智能是fail 或者 success
    if argument == "fail" or argument == "success":
        summary(argument)
    else:
        pass
    '''
    all_set, all_fail_set, all_success_set = set(), set(), set()
    all_set = set(load_json("set2.json"))
    print(len(all_set))
    with open("word_all_fail.txt", "r", encoding="utf-8")as inp:
        all_fail_set = set(inp.read().strip().split())
        if "" in all_fail_set:
            all_fail_set.remove("")
        print(len(all_fail_set))
    with open("word_all_success.txt", "r", encoding="utf-8")as inp:
        all_success_set = set(inp.read().strip().split())
        if "" in all_success_set:
            all_success_set.remove("")
        print(len(all_success_set))
    rest_word = all_set - all_success_set - all_fail_set
    print(len(rest_word))
    if len(rest_word) > 0:
        with open("word_rest.txt", "wb")as outp:
            for i in rest_word:
                outp.write((i + "\n").encode("utf-8"))
