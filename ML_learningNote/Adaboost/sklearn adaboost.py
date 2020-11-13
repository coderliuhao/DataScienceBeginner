# -*- coding: utf-8 -*- 
# @Time : 2020/8/21 16:57 
# @Version: 3.6.5
# @Author : liu hao 
# @File : sklearn adaboost.py

import numpy as np
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier

def load_data(filename):
    num_col=len(open(filename).readline().split("\t"))
    data=[]
    labels=[]
    fr=open(filename)
    for line in fr.readlines():
        line_arr=[]
        cur_line=line.strip().split("\t")
        for i in range(num_col-1):
            line_arr.append(float(cur_line[i]))
        data.append(line_arr)
        labels.append(float(cur_line[-1]))
    return data,labels

if __name__ == '__main__':
    data,labels=load_data("horseColicTraining2.txt")
    test_X,test_labels=load_data("horseColicTest2.txt")
    ada=AdaBoostClassifier(DecisionTreeClassifier(max_depth=2),algorithm="SAMME",n_estimators=10)
    ada.fit(data,labels)
    predictions=ada.predict(data)
    err_arr=np.mat(np.ones((len(data),1)))
    print("训练集错误率: %.3f%%"%float(err_arr[predictions!=labels].sum()/len(data)*100))
    predictions=ada.predict(test_X)
    err_arr=np.mat(np.ones((len(test_X),1)))
    print("测试集错误率: %.3f%%"%float(err_arr[predictions!=test_labels].sum()/len(test_X)*100))

