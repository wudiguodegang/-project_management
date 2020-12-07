#coding:utf-8
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd
import jieba as jb
import joblib
from sklearn.svm import SVC
from gensim.models.word2vec import Word2Vec


def load_file_and_preprocessing():
    neg =pd.read_excel("data/neg_fixed.xlsx",header=None,index=None)
    pos =pd.read_excel("data/pos_fixed.xlsx",header=None,index=None)
    # 这是两类数据都是x值
    pos['words'] = pos[0].apply(lambda x:list(jb.cut(x)))
    neg['words'] = neg[0].apply(lambda x:list(jb.cut(x)))
    #需要y值  0 代表neg 1代表是pos
    y = np.concatenate((np.ones(len(pos)),np.zeros(len(neg))))
    X = np.concatenate((pos['words'],neg['words']))
    # 切分训练集和测试集
    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=3)
    #保存数据
    np.save("data/y_train.npy",y_train)
    np.save("data/y_test.npy",y_test)
    return X_train,X_test

def build_vector(text,size,wv):
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

def get_train_vecs(x_train,x_test):
    #初始化模型和词表
    wv = Word2Vec(size=300,min_count=10)
    wv.build_vocab(x_train)
    # 训练并建模
    wv.train(x_train,total_examples=1, epochs=1)
    #获取train_vecs
    train_vecs = np.concatenate([ build_vector(z,300,wv) for z in x_train])
    #保存处理后的词向量
    np.save('data/train_vecs.npy',train_vecs)
    #保存模型
    wv.save("data/model3.pkl")

    wv.train(x_test,total_examples=1, epochs=1)
    test_vecs = np.concatenate([build_vector(z,300,wv) for z in x_test])
    np.save('data/test_vecs.npy',test_vecs)



def get_data():
    train_vecs = np.load("data/train_vecs.npy")
    y_train = np.load("data/y_train.npy")
    test_vecs = np.load("data/test_vecs.npy")
    y_test = np.load("data/y_test.npy")
    return train_vecs,y_train,test_vecs,y_test

def suc_train(train_vecs,y_train,test_vecs,y_test):
    #创建SVC模型
    cls = SVC(kernel="rbf",verbose=True)
    #训练模型
    cls.fit(train_vecs,y_train)
    #保存模型
    joblib.dump(cls,"data/svcmodel.pkl")
    #输出评分
    print(cls.score(test_vecs,y_test))

def get_predict_vecs(words):
    # 加载模型
    wv = Word2Vec.load("data/model3.pkl")
    #将新的词转换为向量
    train_vecs = build_vector(words,300,wv)
    return train_vecs

def svm_predict(string):
    # 对语句进行分词
    words = jb.cut(string)
    # 将分词结果转换为词向量
    word_vecs = get_predict_vecs(words)
    #加载模型
    cls = joblib.load("data/svcmodel.pkl")
    #预测得到结果
    result = cls.predict(word_vecs)
    #输出结果
    if result[0]==1:
        print("pos")
    else:
        print("neg")

def train():
    x_train,x_test = load_file_and_preprocessing()
    get_train_vecs(x_train,x_test)
    train_vecs,y_train,test_vecs,y_test = get_data()
    suc_train(train_vecs,y_train,test_vecs,y_test)

train()

#string = "您好，很高兴为您服务。那可以的先生，办理宽带业务需要产生200块钱开户，后面每个月在套餐基础上加18块钱，您确定办理吗？都要产生啊都要产生。从19年6月份开始都要产生的。是吧博士先生？第一个月200，后面每个月在套餐基础上加18块钱电视服务费就可以。从话费里面扣取。现在需要办理，请您告诉我地址在什么地方，马上给您办理，明天是不是上门给您安装就可以了。对对对对对。那您看还起来可以帮你吗？没有。好担心了。"

#svm_predict(string)

