from tkinter import *
import Get_text_result
import numpy as np
import jieba as jb
import joblib
import VoiceTransformToText
from gensim.models.word2vec import Word2Vec
import Keywords

class core():
    def __init__(self,str):
        self.string=str

    def build_vector(self,text,size,wv):
        #创建一个指定大小的数据空间
        vec = np.zeros(size).reshape((1,size))
        #count是统计有多少词向量
        count = 0
        #循环所有的词向量进行求和
        for w in text:
            try:
                vec +=  wv[w].reshape((1,size))
                count +=1
            except:
                continue
        #循环完成后求均值
        if count!=0:
            vec/=count
        return vec
    def get_predict_vecs(self,words):
        # 加载模型
        wv = Word2Vec.load("data/model3.pkl")
        #将新的词转换为向量
        train_vecs = self.build_vector(words,300,wv)
        return train_vecs
    def svm_predict(self,string):
        # 对语句进行分词
        words = jb.cut(string)
        # 将分词结果转换为词向量
        word_vecs = self.get_predict_vecs(words)
        #加载模型
        cls = joblib.load("data/svcmodel.pkl")
        #预测得到结果
        result = cls.predict(word_vecs)
        #输出结果
        if result[0]==1:
            return "良好"
        else:
            return "较差"
    def main(self):
        s=self.svm_predict(self.string)
        return s
def solve_start(filename):
    TEXT_RESULT = Get_text_result.get_text_result(filename)
    a,b,c = VoiceTransformToText.seperate_method(TEXT_RESULT)
    key = Keywords.get_key(c)
    key = ",".join(key)
    p=core(b)
    sentiment =p.main()
    return sentiment,key
if __name__ == '__main__':
    print(solve_start("F:\项目\语音质检\data\好感.wav"))