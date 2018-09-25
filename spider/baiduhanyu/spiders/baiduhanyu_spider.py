# -*- coding: utf-8 -*-
import scrapy
from urllib import parse
import json
from scrapy.http import Request
import re
import time

num = 2
regular_success = "百科释义|基本释义|详细释义"  # 日常词匹配
pattern_success = re.compile(regular_success)

regular_fail = "<title>页面不存在_百度搜索</title>"  # 被反扒
pattern_fail = re.compile(regular_fail)


def tell_class(str, pattern_success=pattern_success, pattern_fail=pattern_fail):
    res = re.search(pattern_fail, str)
    if res != None:
        return -1  # 被反扒
    res = re.search(pattern_success, str)
    if res != None:
        return 1  # 成功搜索，并找到
    return 0  # 成功搜索，但是没有找到


def get_url(word):
    url = 'https://hanyu.baidu.com/s?'
    dict1 = {
        "wd": word,
        "device": "pc",
        "from": "home"
    }
    return url + parse.urlencode(dict1)


def load_json(json_file):
    with open(json_file, "r")as load_f:
        data = json.load(load_f)
        return data


def store(data, outfile):
    with open(outfile, 'w') as json_file:
        json_file.write(json.dumps(data))

'''
word_list = load_json("word" + str(num) + ".json")
try:
    with open("word_fail" + str(num) + ".txt", "r", encoding="utf-8")as inp1:
        word_fail = set(inp1.read().split())
except FileNotFoundError:
    word_fail = set()
try:
    with open("word_success" + str(num) + ".txt", "r", encoding="utf-8")as inp2:
        word_success = set(inp2.read().split())
except FileNotFoundError:
    word_success = set()
word_list = set(word_list) - word_fail - word_success
file_success = open("word_success" + str(num) + ".txt", "ab", 0)
file_fail = open("word_fail" + str(num) + ".txt", "ab", 0)
'''

with open("word_rest.txt","r",encoding="utf-8")as inp:
    word_rest=set(inp.read().strip().split())
    if "" in word_rest:
        word_rest.remove("")
    word_list=list(word_rest)
file_success = open("word_success6.txt", "ab", 0)
file_fail = open("word_fail6.txt", "ab", 0)

class BaiduhanyuSpider(scrapy.Spider):
    name = 'baiduhanyu'
    allowed_domains = ['baidu.com']

    def start_requests(self):
        for word in word_list:
            url = get_url(word)
            yield Request(url=url, callback=self.parse)
            # yield Request(url, callback=lambda response, word=word: self.parse_type(response, word))

    def parse(self, response):
        url = response.url
        word = url.split("&")[0].split("=")[-1]
        word = parse.unquote(word)
        html = response.body.decode("utf-8", "ignore")
        state = tell_class(html)
        if state == 1:
            # 查询成功，词存在
            file_success.write((word + "\n").encode("utf-8"))
        elif state == 0:
            # 查询失败，词不存在
            file_fail.write((word + "\n").encode("utf-8"))
        else:
            # 被反爬
            print("被反爬了！")
