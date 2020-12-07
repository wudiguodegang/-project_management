#-*-coding: utf-8-*-
import jieba
import jieba.analyse

#第一步：分词，这里使用结巴分词全模式
text = '''呃你好，就是我想我这个手机不是办了那个宽带业务，吧我想把它打开一下宽带业务。它这个怎么会要200块钱这个开户？啊以前我们都没有。啊意思就是说一个月200，后面的话再加100。它是从话费里面扣还是什么呢？噢那目前不开了。
'''
jieba.load_userdict("data\keyword.txt")
fenci_text = jieba.cut(text)
#print("/ ".join(fenci_text))

#第二步：去停用词
#这里是有一个文件存放要改的文章，一个文件存放停用表，然后和停用表里的词比较，一样的就删掉，最后把结果存放在一个文件中
stopwords = {}.fromkeys([ line.rstrip() for line in open('data/stopwords.txt',encoding='UTF-8') ])
final = ""
for word in fenci_text:
    if word not in stopwords:
        if (word != "。" and word != "，") :
            final = final + " " + word
print(final)

#第三步：提取关键词
a=jieba.analyse.extract_tags(text, topK = 5, withWeight = True, allowPOS = ())
b=jieba.analyse.extract_tags(text, topK = 10,   allowPOS = ())
print(a)
print(b)
#text 为待提取的文本
# topK:返回几个 TF/IDF 权重最大的关键词，默认值为20。
# withWeight:是否一并返回关键词权重值，默认值为False。
# allowPOS:仅包括指定词性的词，默认值为空，即不进行筛选。