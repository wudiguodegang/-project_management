#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Desc  :调用百度接口实现关键词的提取

import json
import requests

APIKey='hwewdeSUssNFRebqsNr6mryk'
SecretKey='0SmVhYPgusraUZspMrg662DV8TqVVln5'

#创建请求url
def get_url():
    url=0
    #通过API Key和Secret Key获取access_token
    AccessToken_url='https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(APIKey,SecretKey)
    res = requests.post(AccessToken_url)#推荐使用post
    json_data = json.loads(res.text)
    #print(json.dumps(json_data, indent=4, ensure_ascii=False))
    if not json_data or 'access_token' not in json_data:
        print("获取AccessToken的json数据失败")
    else:
        accessToken=json_data['access_token']
        #将得到的access_token加到请求url中
        url='https://aip.baidubce.com/rpc/2.0/nlp/v1/keyword?charset=UTF-8&access_token={}'.format(accessToken)
    return url

#创建请求，获取数据
def get_tag(url,title,content):
    tag=''#存储得到的关键词
    #创建Body请求
    body={
        "title": title,
        "content":content
    }
    body2 = json.dumps(body)#将字典形式的数据转化为字符串,否则报错
    #创建Header请求
    header={
        'content-type': 'application/json'
    }
    res = requests.post(url,headers=header,data=body2)# 推荐使用post
    json_data = json.loads(res.text)
    if not json_data or 'error_code' in json_data:
        #print(json.dumps(json_data, indent=4, ensure_ascii=False))
        print("获取关键词的Json数据失败")
    else:
        #print(json.dumps(json_data, indent=4, ensure_ascii=False))
        for item in json_data['items']:
            tag=tag+item['tag']+' '
        tags=tag.strip()#去除前后空格
        print(tags)
        return tags

if __name__ == '__main__':
    title='提取客户的需求信息'
    content = "呃你好，就是我想我这个手机不是办了那个宽带业务，吧我想把它打开一下宽带业务。它这个怎么会要200块钱这个开户？啊以前我们都没有。啊意思就是说一个月200，后面的话再加100。它是从话费里面扣还是什么呢？噢那目前不开了。"
    url=get_url()
    get_tag(url, title,content)
