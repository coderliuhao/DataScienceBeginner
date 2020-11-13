# -*- coding: utf-8 -*- 
# @Time : 2020/8/15 12:44 
# @Version: 3.6.5
# @Author : liu hao 
# @File : logistic reg.py

import matplotlib.pyplot as plt
import numpy as np

"""测试梯度上升算法
例子：求f(x)=-x^2+4x的极大值"""


def gradient_asent_test():
    def ff_prime(x_old):
        return -2 * x_old + 4

    x_old = -1
    x_new = 0
    alpha = 0.01
    presision = 0.00000001
    while abs(x_new - x_old) > presision:
        x_old = x_new
        x_new = x_old + alpha * ff_prime(x_old)
    print(x_new)


def load_dataset():
    data_matrix = []
    labels = []
    fr = open("testSet.txt")
    for line in fr.readlines():
        line_arr = line.strip().split()
        data_matrix.append([1.0, float(line_arr[0]), float(line_arr[1])])
        labels.append(int(line_arr[2]))
        fr.close()
    return data_matrix, labels


"""定义sigmoid函数"""


def sigmoid(input_x):
    return 1.0 / (1 + np.exp(-input_x))


"""梯度上升算法"""


def grad_asent(data, label):
    # pre_label=np.mat(label)
    datamatrix = np.mat(data)#(100,3)
    label = np.mat(label).transpose()#shape(100,1)
    # sl=np.shape(label)
    r, c = np.shape(datamatrix)
    alpha = 0.01
    max_iters = 500
    weights = np.ones((c, 1))#shape(3,1)
    for k in range(max_iters):
        h = sigmoid(datamatrix * weights)
        error = label - h#shape(100,1)
        # se=np.shape(error)          #shape(c,r)=(3,100)*(100,1)
        weights = weights + alpha * datamatrix.transpose() * error
        # sw=np.shape(weights)
    return weights.getA()#将numpy的matrix转换为数组



"""绘制数据集"""


def plot_data():
    data, label = load_dataset()
    data_arr = np.array(data)
    r = np.shape(data)[0]
    x_p = [] #正例数据
    y_p = [] #正例标签
    x_n = [] #负例数据
    y_n = [] #负例标签
    for i in range(r):
        if int(label[i]) == 1:
            x_p.append(data_arr[i, 1]) #特征列
            y_p.append(data_arr[i, 2])#标签列
        else:
            x_n.append(data_arr[i, 1])
            y_n.append(data_arr[i, 2])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(x_p, y_p, s=20, c="red", marker="s", alpha=0.5)
    ax.scatter(x_n, y_n, s=20, c="green", alpha=0.5)
    plt.title("dataset")
    plt.xlabel("X1")
    plt.ylabel("X2")
    plt.show()


"""绘制带最优拟合线的数据"""


def plot_data_with_bestfit(weights):
    data, label = load_dataset()
    data_arr = np.array(data)
    r = np.shape(data)[0]
    x_n, x_p, y_n, y_p = [], [], [], []
    for i in range(r):
        if int(label[i]) == 1:
            x_p.append(data_arr[i, 1])
            y_p.append(data_arr[i, 2])
        else:
            x_n.append(data_arr[i, 1])
            y_n.append(data_arr[i, 2])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(x_p, y_p, s=20, c="red", marker="s", alpha=.5)
    ax.scatter(x_n, y_n, s=20, c="green", alpha=.5)

    x = np.arange(-3.0, 3.0, 0.1)
    y = (-weights[0] - weights[1] * x) / weights[2]
    ax.plot(x, y)
    plt.title("bestfit")
    plt.xlabel("X1")
    plt.ylabel("X2")
    plt.show()

if __name__=="__main__":
    data,label=load_dataset()
    #print(label)
    # print(type(label))
    # print(np.shape(label))
    plot_data()
    weights=grad_asent(data,label)
    # print(weights)
    # print(np.shape(weights))
    # print(type(weights))
    plot_data_with_bestfit(weights)
