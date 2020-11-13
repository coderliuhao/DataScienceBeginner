# -*- coding: utf-8 -*- 
# @Time : 2020/8/18 16:31 
# @Version: 3.6.5
# @Author : liu hao 
# @File : SVC.py

import numpy as np
import operator
from os import listdir
from sklearn.svm import  SVC

def img2vec(filename):
    vec=np.zeros((1,1024))
    fr=open(filename)
    for i in range(32):
        line_arr=fr.readline()
        for j in range(32):
            vec[0,32*i+j]=int(line_arr[j])
    return vec

def handwritingtest():
    labels=[]
    train_files=listdir("trainingDigits")
    r=len(train_files)
    train_X=np.zeros((r,1024))
    for i in range(r):
        filename=train_files[i]
        label_i=int(filename.split("_")[0])
        labels.append(label_i)
        train_X[i,:]=img2vec("trainingDigits/%s"%(filename))
    clf=SVC(C=200,kernel='rbf')
    clf.fit(train_X,labels)

    test_files=listdir("testDigits")
    err_stat=0.0
    num_test=len(test_files)
    for i in range(num_test):
        filename=test_files[i]
        label_i=int(filename.split("_")[0])
        test_X=img2vec("testDigits/%s"%(filename))
        res=clf.predict(test_X)

        print("分类结果:%d\t真实结果:%d"%(res,label_i))
        if res!=label_i:
            err_stat+=1.0
    print("分类错误样本数:%d\n错误率:%f%%"%(err_stat,err_stat/num_test*100))

if __name__=="__main__":
    handwritingtest()

