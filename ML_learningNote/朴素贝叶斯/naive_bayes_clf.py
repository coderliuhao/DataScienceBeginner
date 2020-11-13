# -*- coding: utf-8 -*- 
# @Time : 2020/8/13 23:01 
# @Author : liu hao 
# @File : naive_bayes_clf.py

from sklearn.naive_bayes import MultinomialNB
import matplotlib.pyplot as plt
import os
import random
import jieba

"""文本处理函数"""
def text_preprocessing(folder_path, test_size=0.2):
    folder_list = os.listdir(folder_path)
    dataset = []
    labels = []
    for folder in folder_list:
        new_folder_path = os.path.join(folder_path, folder)
        files = os.listdir(new_folder_path)

        j = 1
        for file in files:
            if j > 100:
                break
            with open(os.path.join(new_folder_path, file), "r", encoding="utf-8") as f:
                raw = f.read()
            word_cut = jieba.cut(raw, cut_all=False)
            word_list = list(word_cut)

            dataset.append(word_list)
            labels.append(folder)

            j += 1

    data_with_label=list(zip(dataset,labels))
    random.shuffle(data_with_label)
    index=int(len(data_with_label)*test_size)+1
    train_ds=data_with_label[index:]
    test_ds=data_with_label[:index]

    train_data,train_labels=zip(*train_ds)
    test_data,test_labels=zip(*test_ds)

    word_freq={}
    for word_list in train_data:
        for word in word_list:
            if word in word_freq.keys():
                word_freq[word]+=1
            else:
                word_freq[word]=1

    freq_sort=sorted(word_freq.items(),key=lambda f:f[1],reverse=True)
    all_words,word_count=zip(*freq_sort)
    all_words=list(all_words)
    return all_words,train_data,test_data,train_labels,test_labels

"""读取文件内容并去重（提取停用词）"""
def word_set(words_file):
    words_set=set()
    with open(words_file,"r",encoding="utf-8") as f:
        for line in f.readlines():
            word=line.strip()
            if len(word)>0:
                words_set.add(word)
    return words_set

"""根据feature_words将文本向量化
   提取特征向量"""
def text_features(train_data,test_data,feature_words):
    def text_feature_extract(text,feature_words):
        text_words=set(text)
        features=[1 if word in text_words else 0 for word in feature_words]
        return features
    train_feat=[text_feature_extract(text,feature_words) for text in train_data]
    test_feat=[text_feature_extract(text,feature_words) for text in test_data]
    return train_feat,test_feat

"""文本特征选取（提取特征词）"""
def feat_word_extract(all_words,deleteN,stop_words_set=set()):
    feature_words=[]
    n=1
    for t in range(deleteN,len(all_words),1):
        if n>1000:
            break
        if not all_words[t].isdigit() and all_words[t] not in stop_words_set and 1<len(all_words[t])<5:
            feature_words.append(all_words[t])
        n+=1
    return feature_words

"""新闻分类器"""
"""分类：MultinomialNB。多项式NB主要用于离散特征，高斯NB主要用于特征满足高斯分布,通常用于连续变量，
   通过估计均值和方差确定概率密度离散化"""
def text_classifier(train_feat,test_feat,train_labels,test_labels):
    clf=MultinomialNB().fit(train_feat,train_labels)
    test_acc=clf.score(test_feat,test_labels)
    return test_acc

"""新浪新闻分类实例"""
if __name__=="__main__":

    folder_path="./SogouC/Sample"
    all_words,train_data,test_data,train_labels,test_labels=text_preprocessing(folder_path,test_size=0.2)

    stop_words_file="./stopwords_cn.txt"
    stop_word_set=word_set(stop_words_file)

    test_accuracy_ls=[]
    deleteN_=range(0,1000,20)
    for deleteN in deleteN_:
        feature_words=feat_word_extract(all_words,deleteN,stop_word_set)
        train_feat,test_feat=text_features(train_data,test_data,feature_words)
        test_accuracy=text_classifier(train_feat,test_feat,train_labels,test_labels)
        test_accuracy_ls.append(test_accuracy)

    ave=lambda c:sum(c)/len(c)
    print(ave(test_accuracy_ls))

    plt.figure()
    plt.plot(deleteN_,test_accuracy_ls)
    plt.title("Relationship between deleteNs and test_acc")
    plt.xlabel("deleteNs")
    plt.ylabel("test_acc")
    plt.show()


