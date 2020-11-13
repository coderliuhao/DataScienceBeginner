# -*- coding: utf-8 -*- 
# @Time : 2020/8/20 23:42 
# @Version: 3.6.5
# @Author : liu hao 
# @File : horse_Death_classification.py

import numpy as np
import matplotlib.pyplot as plt

def load_data(filename):
    num_col=len((open(filename).readline().split("\t")))
    data,labels=[],[]
    fr=open(filename)
    for line in fr.readlines():
        line_arr=[]
        cur_line=line.strip().split("\t")
        for i in range(num_col-1):
            line_arr.append(float(cur_line[i]))
        data.append(line_arr)
        labels.append(float(cur_line[-1]))
    return data,labels

"""单层决策分类函数"""
def sl_dt_classify(data,col,threshval,thresh_marker):

    res_arr=np.ones((np.shape(data)[0],1))
    if thresh_marker=="lt":
        res_arr[data[:,col]<=threshval] = -1.0 #规定特征小于阈值部分为-1
    else:
        res_arr[data[:,col]>threshval]  = -1.0#规定特征大于阈值部分为-1
    return res_arr

"""寻找最优的单层决策树"""
def best_sl_tree(data,labels,D):
    data_mat=np.mat(data)
    label_mat=np.mat(labels).T
    r,c=np.shape(data_mat)
    num_steps=10.0
    best_tree={}
    best_label_esti=np.mat(np.zeros((r,1)))#初始化类别估计值
    min_err=float('inf')
    for i in range(c):#遍历所有特征
        upper_bound=data_mat[:,i].max()#计算特征上界
        lower_bound=data_mat[:,i].min()#计算特征下界
        step_size=(upper_bound-lower_bound)/num_steps#确定切分的步长
        for j in range(-1,int(num_steps)+1):#遍历特征所有可能的取值
            for marker in ['lq',"gt"]:
                threshval=lower_bound+float(j)*step_size ##当前切分点
                prediction=sl_dt_classify(data_mat,i,threshval,marker)#根据预测函数获得预测标签
                err_arr=np.mat(np.ones((r,1)))#初始化误差数组
                err_arr[prediction==label_mat]=0#如果预测和真实相同则置0
                weighted_err=D.T*err_arr

                if weighted_err<min_err: ##当前误差和初始化的误差关系
                    min_err=weighted_err#获得最小误差
                    best_label_esti=prediction.copy()#预测值作为最好的类别估计
                    best_tree["col"]=i#储存当前列
                    best_tree["threshval"]=threshval#储存阈值
                    best_tree["marker"]=marker#储存标志位
    return best_tree,min_err,best_label_esti

"""使用adaboost提升分类器性能"""
def adaboost_train(data,labels,num_iter=40):

    weak_classifier=[]#初始化弱分类器
    r=np.shape(data)[0]#取出行数
    D=np.mat(np.ones((r,1))/r) #初始化权重向量D，此时权重为1/r
    agg_label_esti=np.mat(np.zeros((r,1))) #初始化累积的类别估计
    for i in range(num_iter):#开始迭代
        best_tree,err,label_esti=best_sl_tree(data,labels,D) #根据权重D以及数据、标签获得最好的单层决策树，最小误差以及标签估计

        alpha=float(0.5*np.log((1-err)/max(err,1e-9))) #计算alpha值，alpha=1/2 *log(1-err/err)
        best_tree["alpha"]=alpha#储存alpha值
        weak_classifier.append(best_tree)#将弱分类器添加到列表
        expon=np.multiply(-1*alpha*np.mat(labels).T,label_esti) #计算e的指数部分，-alpha*y*label_esti
        D=np.multiply(D,np.exp(expon))#更新权重D
        D=D/D.sum()#归一化

        agg_label_esti+=alpha*label_esti#累加每一个弱分类器的类别估计值，alpah为弱分类器权重
        agg_err=np.multiply(np.sign(agg_label_esti)!=np.mat(labels).T,np.ones((r,1)))#如果累加的标签估计值不等于真实标签，置1，若相同则置0
        err_rate=agg_err.sum()/r#计算误差率
        if err_rate==0.0:#误差降为0时停止迭代
            break
    return weak_classifier,agg_label_esti

"""adaboost分类"""
def adaboost_classify(test_X,classifier):
    test_mat=np.mat(test_X)
    r=np.shape(test_mat)[0]
    agg_label_esti=np.mat(np.zeros((r,1)))#初始化累积预测值
    for i in range(len(classifier)):#遍历每个弱分类器的切分特征和划分阈值，以及标志位类型
        label_esti=sl_dt_classify(test_mat,classifier[i]["col"],
                                  classifier[i]["threshval"],
                                  classifier[i]["marker"])
        agg_label_esti+=classifier[i]["alpha"]*label_esti#将所有弱分类器的权重与标签估计值乘积求和，
    return np.sign(agg_label_esti)#符号函数获得最终的分类结果

if __name__=="__main__":
    data,labels=load_data("horseColicTraining2.txt")
    weak_classifier,agg_label_esti=adaboost_train(data,labels)
    test_X,test_labels=load_data("horseColicTest2.txt")
    print(weak_classifier)
    predictions=adaboost_classify(data,weak_classifier)
    err_arr=np.mat(np.ones((len(data),1)))
    print("训练集错误率: %.3f%%"%float(err_arr[predictions!=np.mat(labels).T].sum()/len(data)*100))
    predictions=adaboost_classify(test_X,weak_classifier)
    err_arr=np.mat(np.ones((len(test_X),1)))
    print("测试集错误率: %.3f%%"%float(err_arr[predictions!=np.mat(test_labels).T].sum()/len(test_X)*100))
