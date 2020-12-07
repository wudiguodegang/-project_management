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

# 接口地址
url = "http://ltpapi.xfyun.cn/v1/ke"
# 开放平台应用ID
x_appid = "5fb4e665"
# 开放平台应用接口秘钥
api_key = "8a218e9409e139f4749a72eaa6288828"
# 语言文本
TEXT = "呃你好，就是我想我这个手机不是办了那个宽带业务，吧我想把它打开一下宽带业务。它这个怎么会要200块钱这个开户？啊以前我们都没有。啊意思就是说一个月200，后面的话再加100。它是从话费里面扣还是什么呢？噢那目前不开了。"


def get_keyword_result(text):
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

if __name__ == '__main__':
    keyword_result = get_keyword_result(TEXT)
    a = json.loads(keyword_result)
    b = [i["word"] for i in a["data"]["ke"]]
    b = ",".join(b)
    print(b)
    save_file(b, 'output/keyword_result.txt')

