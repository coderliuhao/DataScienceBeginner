# -*- coding: utf-8 -*- 
# @Time : 2020/8/21 17:10 
# @Version: 3.6.5
# @Author : liu hao 
# @File : ada_plot_ROC.py

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties


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

def sl_tree_classify(data,col,threshval,marker):
    res_arr=np.ones((np.shape(data)[0],1))
    if marker=="lt":
        res_arr[data[:,col]<=threshval] = -1.0
    else:
        res_arr[data[:,col]>threshval] = -1.0
    return res_arr

def sl_tree(data,labels,D):
    data_mat=np.mat(data)
    label_mat=np.mat(labels).T
    r,c=np.shape(data_mat)
    num_steps=10.0
    best_tree={}
    best_label_esti=np.mat(np.zeros((r,1)))
    min_err=float("inf")

    for i in range(c):
        upper=data_mat[:,i].max()
        lower=data_mat[:,i].min()
        step_size=(upper-lower)/num_steps
        for j in range(-1,int(num_steps)+1):
            for marker in ["lt","gt"]:
                threshval=lower+float(j)*step_size
                prediction=sl_tree_classify(data_mat,i,threshval,marker)
                err_arr=np.mat(np.ones((r,1)))
                err_arr[prediction==label_mat]=0
                weighted_err=D.T*err_arr

                if weighted_err<min_err:
                    min_err=weighted_err
                    best_label_esti=prediction.copy()
                    best_tree["col"]=i
                    best_tree["threshval"]=threshval
                    best_tree["marker"]=marker
    return best_tree,min_err,best_label_esti

def adaboost_train(data,labels,num_iter=40):
    weak_classifier=[]
    r=np.shape(np.mat(data))[0]
    D=np.mat(np.ones((r,1))/r)
    agg_label_esti=np.mat(np.zeros((r,1)))

    for i in range(num_iter):
        best_tree,err,label_esti=sl_tree(data,labels,D)
        alpha=float(0.5*np.log((1.0-err)/max(err,1e-16)))
        best_tree["alpha"]=alpha
        weak_classifier.append(best_tree)
        expon=np.multiply(-1*alpha*np.mat(labels).T,label_esti)

        D=np.multiply(D,np.exp(expon))
        D=D/D.sum()

        agg_label_esti +=alpha*label_esti
        agg_err=np.multiply(np.sign(agg_label_esti)!=np.mat(labels).T,np.ones((r,1)))
        err_rate=agg_err.sum()/r
        if err_rate==0.0:
            break
    return weak_classifier,agg_label_esti

def plot_roc(pred,labels):
    font=FontProperties(fname=r"c:\windows\fonts\simsun.ttc",size=14)
    cur=(1.0,1.0)
    y_sum=0.0
    num_p=np.sum(np.array(labels)==1.0)
    y_step=1/float(num_p)
    x_step=1/float(len(labels)-num_p)
    sorted_index=pred.argsort()
    fig=plt.figure()
    fig.clf()
    ax=plt.subplot(111)
    for idx in sorted_index.tolist()[0]:
        if labels[idx]==1.0:
            delx=0
            dely=y_step
        else:
            delx=x_step
            dely=0
            y_sum+=cur[1]
        ax.plot([cur[0],cur[0]-delx],[cur[1],cur[1]-dely],c="b")
        cur=(cur[0]-delx,cur[1]-dely)
    ax.plot([0,1],[0,1],"b--")
    plt.title("Adaboost马病检测系统的ROC曲线",FontProperties=font)
    plt.xlabel("假阳率",FontProperties=font)
    plt.ylabel("真阳率",FontProperties=font)
    ax.axis([0,1,0,1])
    print("AUC面积为:",y_sum*x_step)
    plt.show()

if __name__ == '__main__':
    data,labels=load_data("horseColicTraining2.txt")
    weak_classifier,agg_label_esti=adaboost_train(data,labels,50)
    plot_roc(agg_label_esti.T,labels)
    print(np.shape(agg_label_esti))







