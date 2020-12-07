#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
这是主要的demo
流程是：
音频->讯飞语音识别API->文本
文本再作两种处理：
    文本->百度情绪识别API->情绪识别的响应
    文本->讯飞关键词提取API->关键词提取的响应
"""
import sys
import json
import Get_text_result

# 硬编码选定需要离线分析的音频
# 以下是一些测试--------------------------
# SOURCE_PATH = 'input/test.mp3'
# SOURCE_PATH = 'input/test.pcm'
# SOURCE_PATH = 'input/test.m4a'
# SOURCE_PATH = 'input/test.wav'
# 以上是一些测试--------------------------
# 或者，通过命令行参数选定需要离线分析的音频
# 如：python demo.py test.wav

#SOURCE_PATH = 'input/' + sys.argv[1]

# STEP 1: 调用讯飞语音识别 API
# 获取讯飞识别出来的响应
def save_file(data, destin):
    """
    数据持久化函数
    :param data: 数据
    :param destin: 目标路径
    :return: None
    """
    data = str(data)
    if data:
        with open(destin, "w", encoding='utf-8') as f:
            f.write(data)

def seperate_method(TEXT_RESULT):
    """
    将音频文本作区分地提取（区分两个人的对话）
    :return: None
    """
    data_list = json.loads(TEXT_RESULT['data'])
    # text 用于拼接
    text_result = ''
    text_result1 = ''
    text_result2 = ''

    #得到整段话
    for data in data_list:
        text_result += data['onebest']
    print('text_result:', text_result)
    print('text_result completed')

    # 假设有两个人，把文本分别做整合
    for data in data_list:
        # print(data)
        if data['speaker'] == '1':
            text_result1 += data['onebest']
        else:
            text_result2 += data['onebest']
    print('客服： ', text_result1)
    print('客户： ', text_result2)
    print('text_result1 text_result2 completed')
    save_file(text_result1, 'output/text_result1.txt')
    save_file(text_result2, 'output/text_result2.txt')
    return text_result,text_result1,text_result2

if __name__ == '__main__':
    TEXT_RESULT = Get_text_result.get_text_result("F:\\pycharm\\新建文件夹\\语音质检\\data\\110.wav")
    seperate_method(TEXT_RESULT)