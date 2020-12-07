#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
讯飞关键词提取接口
"""
import time
import urllib.request
import urllib.parse
import json
import hashlib
import base64
import numpy as np
import jieba
import jieba.analyse

# 接口地址
url = "http://ltpapi.xfyun.cn/v1/ke"
# 开放平台应用ID
x_appid = "5fb4e665"
# 开放平台应用接口秘钥
api_key = "8a218e9409e139f4749a72eaa6288828"
# 语言文本
TEXT = "呃你好，就是我想我这个手机不是办了那个宽带业务，吧我想把它打开一下宽带业务。它这个怎么会要200块钱这个开户？啊以前我们都没有。啊意思就是说一个月200，后面的话再加100。它是从话费里面扣还是什么呢？噢那目前不开了。"


def get_keyword_xunfei(text):
    """
    这是讯飞官方文档给出的示例
    :param text: 输入文本
    :return response: 返回对象
    """
    if text == '':
        return ''
    body = urllib.parse.urlencode({'text': text}).encode('utf-8')
    param = {"type": "dependent"}
    x_param = base64.b64encode(json.dumps(param).replace(' ', '').encode('utf-8'))
    x_time = str(int(time.time()))
    x_checksum = hashlib.md5(api_key.encode('utf-8') +
                             str(x_time).encode('utf-8') +
                             x_param).hexdigest()
    x_header = {'X-Appid': x_appid,
                'X-CurTime': x_time,
                'X-Param': x_param,
                'X-CheckSum': x_checksum}
    req = urllib.request.Request(url, body, x_header)
    result = urllib.request.urlopen(req)
    result = result.read()
    return result.decode('utf-8')

def save_file(data, destin):
    """
    数据持久化函数
    :param data: 数据
    :param destin: 目标路径
    :return: None
    """
    data = str(data)
    if data:
        with open(destin, "a", encoding='utf-8') as f:
            f.write(data)
            f.write("\n")

def get_keyword_jieba(TEXT):
    #第一步：分词，这里使用结巴分词全模式
    jieba.load_userdict("data\keyword.txt")
    fenci_text = jieba.cut(TEXT)
    #第二步：去停用词
    #这里是有一个文件存放要改的文章，一个文件存放停用表，然后和停用表里的词比较，一样的就删掉，最后把结果存放在一个文件中
    stopwords = {}.fromkeys([ line.rstrip() for line in open('data/stopwords.txt',encoding='UTF-8') ])
    final = ""
    for word in fenci_text:
        if word not in stopwords:
            if (word != "。" and word != "，") :
                final = final + " " + word
    #第三步：提取关键词
    b=jieba.analyse.extract_tags(TEXT, topK = 10,   allowPOS = ())
    return b

def get_key(TEXT):
    keyword_result = get_keyword_xunfei(TEXT)
    xunfei_a = json.loads(keyword_result)
    xunfei_b = [i["word"] for i in xunfei_a["data"]["ke"]]
    jieba_b = get_keyword_jieba(TEXT)
    result_b = list(set(jieba_b).intersection(set(xunfei_b)))
    return result_b

#print(get_key(TEXT))