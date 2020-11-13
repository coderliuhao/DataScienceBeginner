# -*- coding: utf-8 -*- 
# @Time : 2020/8/16 18:15 
# @Version: 3.6.5
# @Author : liu hao 
# @File : horse_life_prediction.py

from sklearn.linear_model import LogisticRegression
import numpy as np
import random

"""x是一个非常小的负数时，exp(-x)会过大，导致溢出，因此对sigmoid优化"""
def sigmoid(input_x):
    if input_x>0:
        return 1.0/(1+np.exp(-input_x))
    else:
        return np.exp(input_x)/(1+np.exp(input_x))

"""改进的随机梯度上升算法"""
def stoch_grad_ascent(data,labels,num_iters=500):
    r,c=np.shape(data)#获取数据行列数
    weights=np.ones(c)#初始化权重向量
    sw=np.shape(weights)#一维数组shape(21,)只返回元素个数
    for j in range(num_iters): #迭代步数
        data_idx=list(range(r))
        for i in range(r): #对每行样本操作
            alpha=4/(1.0+i+j)+0.1#设定梯度的上升步长
            rand_idx=int(random.uniform(0,len(data_idx)))#随机选一个样本
            h=sigmoid(sum(data[rand_idx]*weights))
            sri=np.shape(data[rand_idx])
            sh=np.shape(data[rand_idx]*weights)
            error=labels[rand_idx]-h
            weights=weights+alpha*error*data[rand_idx]
            del data_idx[rand_idx]
    return weights

"""梯度上升算法"""
def grad_ascent(data,labels):
    data_mat=np.mat(data)
    labels_mat=np.mat(labels).transpose()
    r,c=np.shape(data_mat)
    alpha=0.01
    max_iters=500
    weights=np.ones((c,1))
    for k in range(max_iters):
        h=sigmoid(data_mat*weights)
        error=labels_mat-h
        weights=weights+alpha*data_mat.transpose()*error
    return weights.getA()



"""使用python实现logistic分类器做预测"""

def horse_life_test():
    f_train=open("horseColicTraining.txt")
    f_test=open("horseColicTest.txt")
    train_X=[]
    train_labels=[]
    for line in f_train.readlines():
        cur_line=line.strip().split("\t")
        line_arr=[]
        for i in range(len(cur_line)-1):
            line_arr.append(float(cur_line[i]))
        train_X.append(line_arr)
        train_labels.append(float(cur_line[-1]))
    train_weights=stoch_grad_ascent(np.array(train_X),train_labels,500)
    error_stats=0
    test_length=0
    for line in f_test.readlines():
        test_length+=1
        cur_line=line.strip().split("\t")
        line_arr=[]
        for i in range(len(cur_line)-1):
            line_arr.append(float(cur_line[i]))
        if int(classify_pre(np.array(line_arr),train_weights)) !=int(cur_line[-1]):
            error_stats+=1
    error_rate=(float(error_stats)/test_length)*100
    print("测试集错误率为：%.2f%%"%error_rate)

"""分类函数"""
def classify_pre(data,weights):
    prob=sigmoid(sum(data*weights))
    if prob>0.5:
        return 1.0
    else:
        return 0.0

"""使用sklearn构建logistic回归 分类器"""
def classify_with_sk():
    f_train=open("horseColicTraining.txt")
    f_test=open("horseColicTest.txt")
    train_X=[]
    train_labels=[]
    test_X=[]
    test_labels=[]

    for line in f_train.readlines():
        cur_line=line.strip().split("\t")
        line_arr=[]
        for i in range(len(cur_line)-1):
            line_arr.append(float(cur_line[i]))
        train_X.append(line_arr)
        train_labels.append(float(cur_line[-1]))
    for line in f_test.readlines():
        cur_line=line.strip().split("\t")
        line_arr=[]
        for i in range(len(cur_line)-1):
            line_arr.append(float(cur_line[i]))
        test_X.append(line_arr)
        test_labels.append(float(cur_line[-1]))
    classifier=LogisticRegression(solver="sag",max_iter=5000).fit(train_X,train_labels)
    test_acc=classifier.score(test_X,test_labels)*100
    print("分类正确率：%.2f%%"%test_acc)

if __name__=="__main__":
    horse_life_test()
    classify_with_sk()

