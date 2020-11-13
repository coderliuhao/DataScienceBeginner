# -*- coding: utf-8 -*- 
# @Time : 2020/8/15 1:02 
# @Version: 3.6.5
# @Author : liu hao 
# @File : bayes_modify.py

import numpy as np
import random
import re

"""加载数据"""
def load_dataset():
    sentences_split=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                   ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                   ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                   ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                   ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                   ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    labels=[0,1,0,1,0,1]#0为积极1为消极
    return sentences_split,labels
#创建词汇列表
def vocab_list(dataset):
    vocab_set=set([])
    for sentence in dataset:
        vocab_set=vocab_set|set(sentence)
    return list(vocab_set)

"""定义词集"""
def set_of_word2vec(vocab_list,input_sentence):
    word_vec=[0]*len(vocab_list)
    for word in input_sentence:
        if word in vocab_list:
            word_vec[vocab_list.index(word)]=1
        else:
            print("The word %s is not in my vocabulary"%word)
    return word_vec

"""定义词袋"""
def bag_of_word2vec(vocab_list,inpput_sentence):
    word_vec=[0]*len(vocab_list)
    for word in inpput_sentence:
        if word in vocab_list:
            word_vec[vocab_list.index(word)]+=1
    return word_vec

"""训练朴素贝叶斯分类器函数"""
def NBclassifier(train_X,train_labels):
    num_sentences=len(train_X)
    num_words=len(train_X[0])
    p_neg=sum(train_labels)/float(num_sentences)
    num_p0=np.ones(num_words)
    num_p1=np.ones(num_words)

    p0_init=2.0
    p1_init=2.0

    for i in range(num_sentences):
        if train_labels[i]==1:
            num_p1+=train_X[i]
            p1_init+=sum(train_X[i])
        else:
            num_p0+=train_X[i]
            p0_init+=sum(train_X[i])
    p1_vec=np.log(num_p1/p1_init)
    p0_vec=np.log(num_p0/p0_init)
    return p0_vec,p1_vec,p_neg

"""使用朴素贝叶斯分类"""
def NBclassify(test_X,p0_vec,p1_vec,p_neg):
    p1=sum(test_X*p1_vec)+np.log(p_neg)
    p0=sum(test_X*p0_vec)+np.log(1-p_neg)
    if p1>p0:
        return 1
    else:
        return 0

"""文本解析函数"""
def text_parse(longstr):
    token_list=re.split(r"\W*",longstr)
    return [token.lower() for token in token_list if len(token)>2]


"""垃圾邮件过滤"""
def email_filter():
    sentences=[]
    label_list=[]
    all_text=[]
    for i in range(1,26):
        word_list=text_parse(open("email/spam/%d.txt"%i,"r").read())
        sentences.append(word_list)
        all_text.append(word_list)
        label_list.append(1)
        word_list=text_parse(open("email/ham/%d.txt"%i,"r").read())
        sentences.append(word_list)
        all_text.append(word_list)
        label_list.append(0)

    vocablist=vocab_list(sentences)
    train_set=list(range(50))
    test_set=[]
    for i in range(10):
        rand_index=int(random.uniform(0,len(train_set)))
        test_set.append(train_set[rand_index])
        del (train_set[rand_index])

    train_X=[]
    train_labels=[]
    for sent_index in train_set:
        train_X.append(set_of_word2vec(vocablist,sentences[sent_index]))
        train_labels.append(label_list[sent_index])

    p0_vec,p1_vec,p_neg=NBclassifier(np.array(train_X),np.array(train_labels))
    error_stats=0
    for sent_index in test_set:
        word_vec=set_of_word2vec(vocablist,sentences[sent_index])
        if  NBclassify(np.array(word_vec),p0_vec,p1_vec,p_neg) !=label_list[sent_index]:
            error_stats+=1
            print("分类错误的测试数据；",sentences[sent_index])
    print("错误率：%.2f%%"%(float(error_stats)/len(test_set)*100))

"""文本情感分析实例"""
def emotion_analyse():
    sentences_split,labels=load_dataset()
    vocablist=vocab_list(sentences_split)
    train_X=[]
    for sentences in sentences_split:
        train_X.append(set_of_word2vec(vocablist,sentences))
    p0_vec,p1_vec,p_neg=NBclassifier(train_X,labels)
    test_sentence=["love","my","dalmation"]
    test_vec=np.array(set_of_word2vec(vocablist,test_sentence))
    if NBclassify(test_vec,p0_vec,p1_vec,p_neg):
        print(test_sentence,"属于侮辱类")
    else:
        print(test_sentence,"属于非侮辱类")

    test_sentence1=["stupid","garbage"]
    test_vec1=np.array(set_of_word2vec(vocablist,test_sentence1))
    if NBclassify(test_vec1,p0_vec,p1_vec,p_neg):
        print(test_sentence1,"属于侮辱类")
    else:
        print(test_sentence1,"属于非侮辱类")

if __name__ =="__main__":
    email_filter()
    emotion_analyse()






