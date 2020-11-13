# -*- coding: utf-8 -*- 
# @Time : 2020/8/15 23:42 
# @Version: 3.6.5
# @Author : liu hao 
# @File : modified_logistic_regression.py

import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

def load_data():
    data_matrix=[]
    labels=[]
    fr=open("testSet.txt")
    for line in fr.readlines():
        line_arr=line.strip().split()
        data_matrix.append([1.0,float(line_arr[0]),float(line_arr[1])])
        labels.append(int(line_arr[2]))
    fr.close()
    return data_matrix,labels

def sigmoid(input_x):
    return 1.0/(1+np.exp(-input_x))

"""梯度提升算法"""
def grad_ascent(data,label):
    data_matrix=np.mat(data)
    labels=np.mat(label).transpose()
    r,c=np.shape(data_matrix)
    alpha=0.01
    max_iters=500
    weights=np.ones((c,1))
    weights_arr=np.array([])
    for k in range(max_iters):
        h=sigmoid(data_matrix*weights)
        error=labels-h
        weights=weights+alpha*data_matrix.transpose()*error
        weights_arr=np.append(weights_arr,weights)
    weights_arr=weights_arr.reshape(max_iters,c)
    return weights.getA(),weights_arr

"""改进的梯度提升"""


def stoch_grad_ascent(data, labels, num_iters=150):
    r, c = np.shape(data)
    weights = np.ones(c)
    # sw = np.shape(weights)
    weights_arr = np.array([])
    for j in range(num_iters):
        data_idx = list(range(r))
        for i in range(r):
            alpha = 4 / (1.0 + j + i) + 0.01
            rand_idx = int(random.uniform(0, len(data_idx)))
            h = sigmoid(sum(data[rand_idx] * weights))
            # sh = np.shape(h)
            error = labels[rand_idx] - h
            # se = np.shape(error)
            weights = weights + alpha * error * data[rand_idx]
            # sww = np.shape(weights)
            weights_arr = np.append(weights_arr, weights, axis=0)
            del (data_idx[rand_idx])
    weights_arr = weights_arr.reshape(num_iters * r, c)
    # swr = np.shape(weights_arr)
    return weights, weights_arr

def plot_data(weights):
    data,labels=load_data()
    data_arr=np.array(data)
    r=np.shape(data)[0]
    x_p,x_n,y_p,y_n=[],[],[],[]
    for i in range(r):
        if int(labels[i])==1:
            x_p.append(data_arr[i,1])
            y_p.append(data_arr[i,-1])
        else:
            x_n.append(data_arr[i,1])
            y_n.append(data_arr[i,-1])
    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax.scatter(x_p,y_p,s=20,c="red",marker="s",alpha=0.5)
    ax.scatter(x_n,y_n,s=20,c="green",alpha=0.5)
    x=np.arange(-3.0,3.0,0.1)
    y=(-weights[0]-weights[1]*x)/weights[2]
    ax.plot(x,y)
    plt.title("bestfit")
    plt.xlabel("X1")
    plt.ylabel("X2")
    plt.show()

"""绘制回归系数与迭代次数的关系"""
def plot_weights(weights_arr1,weights_arr2):
    font=FontProperties(fname=r"c:\windows\fonts\simsun.ttc",size=14)

    fig,axs=plt.subplots(3,2,sharex=False,sharey=False,figsize=(20,10))
    x1=np.arange(0,len(weights_arr1),1)

    axs[0][0].plot(x1,weights_arr1[:,0])
    axs[0][0].set_title(u"改进的梯度提升算法：回归系数与迭代次数的关系",FontProperties=font)
    axs[0][0].set_ylabel(u"W0",FontProperties=font)

    axs[1][0].plot(x1, weights_arr1[:, 1])
    axs[1][0].set_ylabel(u"W1", FontProperties=font)

    axs[2][0].plot(x1, weights_arr1[:, 2])
    axs[2][0].set_xlabel(u"迭代次数",FontProperties=font)
    axs[2][0].set_ylabel(u"W2", FontProperties=font)

    x2=np.arange(0,len(weights_arr2),1)
    axs[0][1].plot(x2,weights_arr2[:,0])
    axs[0][1].set_title(u"梯度提升算法：回归系数与迭代次数的关系",FontProperties=font)
    axs[0][1].set_ylabel(u"W0",FontProperties=font)

    axs[1][1].plot(x2,weights_arr2[:,1])
    axs[1][1].set_ylabel(u"W1",FontProperties=font)

    axs[2][1].plot(x2,weights_arr2[:,2])
    axs[2][1].set_xlabel(u"迭代次数",FontProperties=font)
    axs[2][1].set_ylabel(u"W2",FontProperties=font)

    plt.show()

if __name__=="__main__":
    data,labels=load_data()
    weights1,weights_arr1=stoch_grad_ascent(np.array(data),labels)
    print(np.shape(weights1))
    print(np.shape(weights_arr1))
    weights2,weights_arr2=grad_ascent(data,labels)
    print(np.shape(weights_arr2))
    print(np.shape(weights2))
    plot_weights(weights_arr1,weights_arr2)
    plot_data(weights1)
    plot_data(weights2)
