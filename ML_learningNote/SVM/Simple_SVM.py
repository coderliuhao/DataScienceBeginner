# -*- coding: utf-8 -*- 
# @Time : 2020/8/17 11:25 
# @Version: 3.6.5
# @Author : liu hao 
# @File : Simple_SVM.py

import matplotlib.pyplot as plt
import numpy as np
import random


def load_data(filename):
    data = []
    labels = []
    fr = open(filename)
    for line in fr.readlines():
        line_arr = line.strip().split("\t")
        data.append([float(line_arr[0]), float(line_arr[1])])
        labels.append(float(line_arr[-1]))
    return data, labels


"""随机选择alpha"""


def rand_alpha(i, m):#随机选择一个不等于i的j
    j = i
    while j == i:
        j = int(random.uniform(0, m))
    return j


"""alpha剪枝"""


def clip_alpha(a_j, sup, inf):#将高于上确界alpha和低于下确界的alpha约束贼上确界和下确界上
    if a_j > sup:
        a_j = sup
    if inf > a_j:
        a_j = inf
    return a_j


"""数据可视化"""


def plot_data(data, labels):
    data_p = []
    data_n = []
    for i in range(len(data)):
        if labels[i] > 0:
            data_p.append(data[i])
        else:
            data_n.append(data[i])
    data_p_arr = np.array(data_p)
    data_n_arr = np.array(data_n)
    plt.scatter(np.transpose(data_p_arr)[0], np.transpose(data_p_arr)[1])
    plt.scatter(np.transpose(data_n_arr)[0], np.transpose(data_n_arr)[1])
    plt.show()


"""简化的SMO算法"""


def simple_smo(data, labels, C, toler, max_iter):
    data_mat = np.mat(data)
    label_mat = np.mat(labels).transpose()
    b = 0
    r, c = np.shape(data_mat)
    alphas = np.mat(np.zeros((r, 1)))
    num_iter = 0
    while num_iter < max_iter:
        alpha_pair_changed = 0
        for i in range(r):
            f_xi = float(np.multiply(alphas, label_mat).T * (data_mat * data_mat[i, :].T)) + b#支持向量机的分类决策函数
            err_i = f_xi - float(label_mat[i])#分类误差

            if ((label_mat[i] * err_i < -toler) and (alphas[i] < C)) or (  #可优化条件   0《=alpha<=C
                    (label_mat[i] * err_i > toler) and (alphas[i] > 0)):
                j = rand_alpha(i, r)

                f_xj = float(np.multiply(alphas, label_mat).T * (data_mat * data_mat[j, :].T)) + b #np.multiply为矩阵对应元素相乘
                err_j = f_xj - float(label_mat[j])                                                 #矩阵的*为矩阵乘积
                alpha_iold = alphas[i].copy()
                alpha_jold = alphas[j].copy()

                if label_mat[i] != label_mat[j]:
                    inf = max(0, alphas[j] - alphas[i])
                    sup = min(C, C + alphas[j] - alphas[i])
                else:
                    inf = max(0, alphas[j] - alphas[i] - C)
                    sup = min(C, alphas[j] + alphas[i])
                if sup == inf:
                    print("sup=inf")
                    continue

                eta = 2.0 * data_mat[i, :] * data_mat[j, :].T - data_mat[i, :] * data_mat[i, :].T - data_mat[j,
                                                                                                    :] * data_mat[j,
                                                                                                         :].T
                if eta >= 0:
                    print("eta>=0")
                    continue

                alphas[j] -= label_mat[j] * (err_i - err_j) / eta
                alphas[j] = clip_alpha(alphas[j], sup, inf)
                if abs(alphas[j] - alpha_jold) < 0.00001:
                    print("alpha_j变化太小")
                    continue
                alphas[i] += label_mat[j] * label_mat[i] * (alpha_jold - alphas[j])
                b1 = b - err_i - label_mat[i] * (alphas[i] - alpha_iold) * data_mat[i, :] * data_mat[i, :].T - \
                     label_mat[j] * (alphas[j] - alpha_jold) * data_mat[i, :] * data_mat[j, :].T
                b2 = b - err_j - label_mat[i] * (alphas[i] - alpha_iold) * data_mat[i, :] * data_mat[j, :].T - \
                     label_mat[j] * (alphas[j] - alpha_jold) * data_mat[j, :] * data_mat[j, :].T

                if 0 < alphas[i] and C > alphas[i]:
                    b = b1
                elif 0 < alphas[j] and C > alphas[j]:
                    b = b2
                else:
                    b = (b1 + b2) / 2.0

                alpha_pair_changed += 1

                print("第%d次迭代:样本%d,alpha优化次数:%d" % (num_iter, i, alpha_pair_changed))

        if alpha_pair_changed == 0:
            num_iter += 1
        else:
            num_iter = 0
        print("迭代次数:%d" % num_iter)

    return b, alphas


"""分类结果可视化"""


def show_classify_res(data, labels, w, b, alphas):
    data_p, data_n = [], []
    for i in range(len(data)):
        if labels[i] > 0:
            data_p.append(data[i])
        else:
            data_n.append(data[i])
    data_p_arr = np.array(data_p)
    data_n_arr = np.array(data_n)
    plt.scatter(np.transpose(data_p_arr)[0], np.transpose(data_p_arr)[1], s=30, alpha=0.5)
    plt.scatter(np.transpose(data_n_arr)[0], np.transpose(data_n_arr)[1], s=30, alpha=0.5)

    x1 = max(data)[0]
    x2 = min(data)[0]
    a1, a2 = w
    b = float(b)
    a1 = float(a1[0])
    a2 = float(a2[0])
    y1, y2 = (-b - a1 * x1) / a2, (-b - a1 * x2) / a2
    plt.plot([x1, x2], [y1, y2])

    for i, alpha in enumerate(alphas):
        if abs(alpha) > 0:
            x, y = data[i]
            plt.scatter([x], [y], s=150, c="none", alpha=0.7, linewidths=1.5, edgecolor="red")

    plt.show()


"""计算w"""


def cal_w(data, labels, alphas):
    alphas, data, labels = np.array(alphas), np.array(data), np.array(labels)
    W = np.dot((np.tile(labels.reshape(1, -1).T, (1, 2)) * data).T, alphas)#对于array来说，*为对应元素乘积，np.dot为矩阵乘法
    return W.tolist()


if __name__ == "__main__":
    data, labels = load_data("testSet.txt")
    b, alphas = simple_smo(data, labels, 0.6, 0.001, 40)
    w = cal_w(data, labels, alphas)
    print(w)
    print(alphas)
    show_classify_res(data, labels, w, b, alphas)
    plot_data(data,labels)
