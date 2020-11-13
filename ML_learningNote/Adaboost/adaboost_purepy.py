# -*- coding: utf-8 -*- 
# @Time : 2020/8/19 14:25 
# @Version: 3.6.5
# @Author : liu hao 
# @File : adaboost_purepy.py

import numpy as np
import matplotlib.pyplot as plt

"""单层决策树数据集"""


def load_data():
    data = np.mat([[1., 2.1],
                   [1.5, 1.6],
                   [1.3, 1],
                   [1.0, 1.0],
                   [2.0, 1.0]
                   ])
    labels = [1.0, 1.0, -1.0, -1.0, 1.0]
    return data, labels


def plot_data(data, labels):
    data_p, data_n = [], []
    for i in range(len(data)):
        if labels[i] > 0:
            data_p.append(data[i])
        else:
            data_n.append(data[i])
    data_p_arr, data_n_arr = np.array(data_p), np.array(data_n)
    x = np.transpose(data_p_arr)
    y = np.transpose(data_n_arr)
    plt.scatter(x[0], x[1])
    plt.scatter(y[0], y[1])
    plt.show()


"""单层决策树分类函数"""


def sl_tree_classify(data, dim, threshval, threshnote):
    res_arr = np.ones((np.shape(data)[0], 1))
    if threshnote == "lt":
        res_arr[data[:, dim] <= threshval] = -1.0
    else:
        res_arr[data[:, dim] > threshval] = -1.0
    return res_arr


"""寻找最优单层决策树"""


def best_sl_tree(data, labels, D):
    data_mat = np.mat(data)
    labels_mat = np.mat(labels).transpose()
    r, c = np.shape(data_mat)
    steps = 10.0
    best_tree = {}
    best_classify_res = np.mat(np.zeros((r, 1)))
    min_err = float("inf")
    for i in range(c):
        range_min = data_mat[:, i].min()
        range_max = data_mat[:, i].max()
        step_size = (range_max - range_min) / steps
        for j in range(-1, int(steps) + 1):
            for in_equal in ["lt", "gt"]:
                threshval = (range_min + float(j) * step_size)
                predict = sl_tree_classify(data_mat, i, threshval, in_equal)
                err_arr = np.mat(np.ones((r, 1)))
                err_arr[predict == labels_mat] = 0
                weighted_err = D.T * err_arr

                if weighted_err < min_err:
                    min_err = weighted_err
                    best_classify_res = predict.copy()
                    best_tree["dim"] = i
                    best_tree["thresh"] = threshval
                    best_tree["in_eq"] = in_equal
    return best_tree, min_err, best_classify_res


"""使用adaboost提升弱分类器性能"""


def Adaboost_train(data, labels, num_iter=40):
    weak_classifier = []
    r = np.shape(data)[0]
    D = np.mat(np.ones((r, 1)) / r)
    agg_label_esti = np.mat(np.zeros((r, 1)))
    for i in range(num_iter):
        best_tree, err, label_esti = best_sl_tree(data, labels, D)
        print("D:", D.T)
        alpha = float(0.5 * np.log((1 - err) / max(err, 1e-16)))
        best_tree["alpha"] = alpha
        weak_classifier.append(best_tree)
        print("label estimate:", label_esti.T)
        expon = np.multiply(-1 * alpha * np.mat(labels).T, label_esti)
        D = np.multiply(D, np.exp(expon))
        D = D / D.sum()

        agg_label_esti += alpha * label_esti
        agg_err = np.multiply(np.sign(agg_label_esti) != np.mat(labels).T, np.ones((r, 1)))
        err_rate = agg_err.sum() / r
        if err_rate == 0.0:
            break
    return weak_classifier, agg_label_esti


"""使用adaboost进行分类"""


def ada_classify(test_mat, classifier):
    test_X = np.mat(test_mat)
    r = np.shape(test_X)[0]
    agg_label_esti = np.mat(np.zeros((r, 1)))
    for i in range(len(classifier)):
        label_esti = sl_tree_classify(test_X, classifier[i]["dim"], classifier[i]["thresh"],
                                      classifier[i]["in_eq"])
        agg_label_esti += classifier[i]["alpha"] * label_esti
        print(agg_label_esti)
    return np.sign(agg_label_esti)


if __name__ == "__main__":
    data, labels = load_data()
    plot_data(data, labels)
    weakclassifier, agg_label_esti = Adaboost_train(data, labels)
    print(ada_classify([[0, 0], [5, 5]], weakclassifier))
    print(weakclassifier)
