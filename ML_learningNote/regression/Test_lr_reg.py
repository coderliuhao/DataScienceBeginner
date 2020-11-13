# -*- coding: utf-8 -*- 
# @Time : 2020/8/22 23:52 
# @Version: 3.6.5
# @Author : liu hao 
# @File : Test_lr_reg.py

from numpy  import *

def load_data(filename):
    num_col=len(open(filename).readline().split("\t"))-1
    data,labels=[],[]
    fr=open(filename)
    for line in fr.readlines():
        line_arr=[]
        cur_line=line.strip().split("\t")
        for i in range(num_col):
            line_arr.append(float(cur_line[i]))
        data.append(line_arr)
        labels.append(float(cur_line[-1]))
    return data,labels

"""标准回归方程求解-最小二乘法求解得到-容易欠拟合  LR有参数学习方法
   在训练完所有数据之后得到一系列训练参数，然后根据训练参数来预测样本
   的值这时不再依赖之前的训练数据，参数是确定的"""
"""标准线性回归"""
def stand_lr_regres(x,y):
    x_mat=mat(x)
    y_mat=mat(y).T
    xTx=x_mat.T * x_mat
    if linalg.det(xTx)==0.0:
        print("This matrix is singular,cannot do inverse")
        return
    ws=xTx.I*(x_mat.T*y_mat)
    return ws

"""局部加权线性回归模型-解决线性回归中存在的欠拟合问题    LWLR非参数学习方法
   在预测新样本值时每次都会重新训练新的参数，也就是每次预测新的样本值都会依赖训练数据集合，
所以每次的参数是不确定的.
   对每个点做预测时都必须使用整个数据集，因此当训练容量过大时，非参数学习算法需要占用更多的存储容量，
计算速度较慢.
   对于样本的预测，其实就是对每个点的预测（或者说拟合）m样本点有m个点，则预测出来的也是m个点，
而这m个点不在一条直线上，而是离散的点,因此最终拟合的'线性'（实为非线性）
曲线则是m个点的（m-1条线段）组成的估计曲线"""

"""局部加权线性回归"""
def lw_lr_reg(test_p,x,y,k=0.1):
    x_mat=mat(x)
    y_mat=mat(y).T
    r=shape(x_mat)[0]
    weights=mat(eye((r)))
    for j in range(r):
        diff_x=test_p-x_mat[j,:]
        weights[j,j]=exp(diff_x*diff_x.T/(-2.0*k**2))
    xTx=x_mat.T*(weights*x_mat)
    if linalg.det(xTx)==0.0:
        print("This matrix is singular,cannot do inverse")
        return
    ws=xTx.I*(x_mat.T*(weights*y_mat))
    return test_p*ws

"""测试局部加权线性回归"""
def test_lw_lr(test_x,x,y,k=1.0):
    r=shape(test_x)[0]
    y_hat=zeros(r)
    for i in range(r):
        y_hat[i]=lw_lr_reg(test_x[i],x,y,k)
    return y_hat

"""局部加权线性回归作图"""
def plot_lw_lr(x,y,k=0.1):
    from matplotlib import pyplot as plt
    y_hat=zeros(shape(y))
    x_cp=mat(x)
    x_cp.sort(0)
    for i in range(shape(x)[0]):
        y_hat[i]=lw_lr_reg(x_cp[i],x,y,k)
    return y_hat,x_cp

"""计算RSS"""
def RSS(y,y_hat):
    return ((y-y_hat)**2).sum()

"""岭回归-解决过拟合问题
在增加约束时，普通的最小二乘法回归会得到与岭回归的一样的公式，
也就是说在增加约束情况下，最少二乘法可以转化为岭回归"""
"""岭回归"""
def ridge_reg(x,y,lam=0.2):
    xTx=x.T*x
    deno=xTx+eye(shape(x)[1])*lam
    if linalg.det(deno)==0.0:
        print("This matrix is singular,cannot do invese")
        return
    ws=deno.I*(x.T*y)
    return ws

"""测试岭回归"""
def test_ridge(x,y):
    x_mat=mat(x)
    y_mat=mat(y).T
    y_mean=mean(y_mat,0)
    y_mat=y_mat-y_mean
    x_mean=mean(x_mat,0)
    x_var =var(x_mat,0)
    x_mat=(x_mat-x_mean)/x_var
    num_test_p=30
    weights_mat=zeros((num_test_p,shape(x_mat)[1]))
    for i in range(num_test_p):
        ws=ridge_reg(x_mat,y_mat,exp(i-10))
        weights_mat[i,:]=ws.T
    return weights_mat

"""正则化"""
def regularized_trans(x):
    x_mat=x.copy()
    x_mean=mean(x_mat,0)
    x_var=var(x_mat,0)
    x_mat=(x_mat-x_mean)/x_var
    return x_mat

"""前向逐步线性回归-使用贪心算法来达到L1正则化的效果，本质上也是
缩减系数，有很多随机性"""
"""前向逐步回归"""
def step_wise_reg(x,y,eps=0.01,num_iter=100):
    x_mat=mat(x)
    y_mat=mat(y).T
    y_mean=mean(y_mat,0)
    y_mat=y_mat-y_mean

    x_mat=regularized_trans(x_mat)
    r,c=shape(x_mat)
    res_mat=zeros((num_iter,c))
    ws=zeros((c,1))
    ws_max=ws.copy()
    for i in range(num_iter):
        print(ws.T)
        min_err=inf
        for j in range(c):
            for sign in [-1,1]:
                ws_test=ws.copy()
                ws_test[j] += eps*sign
                y_test=x_mat*ws_test
                rss=RSS(y_mat.A,y_test.A)
                if rss<min_err:
                    min_err=rss
                    ws_max=ws_test
        ws=ws_max.copy()
        res_mat[i,:]=ws.T
    return res_mat

if __name__ == '__main__':
    x1,y1=load_data("ex1.txt")
    ws=stand_lr_regres(x1,y1)
    x1_mat=mat(x1)
    y1_mat=mat(y1)
    y_hat1=x1_mat*ws
    print("普通最小二乘预测值:",y_hat1)

    x2,y2=load_data("ex0.txt")
    #print("局部加权最小二乘回归:",lw_lr_reg(x2[0],x2,y2,1.0))
    print("局部加权最小二乘预测值:",test_lw_lr(x2,x2,y2,0.001))

    x3,y3=load_data("abalone.txt")
    print("岭回归预测结果:",test_ridge(x3,y3))

    x4,y4=load_data("abalone.txt")
    print("前向逐步回归预测结果:",step_wise_reg(x4,y4,0.01,200))





# from time import sleep
# import json
# import urllib
#
# def search_dataset(x_out,y_out,num,yr,num_pce,origprc):
#     sleep(10)
#     my_api_str="AIzaSyD2cR2KFyx12hXu6PFU-wrWot3NXvko8vY"
#     url="https://www.googleapis.com/shopping/search/v1/public/products?key=%s&country=US&q=lego+%d&alt=json"%(my_api_str,num)
#     pg=urllib.urlopen(url)
#     res_dict=json.loads(pg.read())
#     for i in range(len(res_dict["items"])):
#         try:
#             cur_item=res_dict["item"][i]
#             if cur_item['product']["condition"]=="new":
#                 new_flag=1
#             else:
#                 new_flag=0
#             list_of_inv=cur_item["product"]["inventories"]
#             for item in list_of_inv:
#                 sell_price=item["price"]
#                 if sell_price>origprc*0.5:
#                     print("%d\t%d\t%d\t%f\t%f" %(yr,num_pce,new_flag,origprc,sell_price))
#                     x_out.append([yr,num_pce,new_flag,origprc])
#                     y_out.append(sell_price)
#
#         except:
#             print("problem with item %d"%i)
#
# #def setDataCollect(retX, retY):
#     search_dataset(retX, retY, 8288, 2006, 800, 49.99)
#     search_dataset(retX, retY, 10030, 2002, 3096, 269.99)
#     search_dataset(retX, retY, 10179, 2007, 5195, 499.99)
#     search_dataset(retX, retY, 10181, 2007, 3428, 199.99)
#     search_dataset(retX, retY, 10189, 2008, 5922, 299.99)
#     search_dataset(retX, retY, 10196, 2009, 3263, 249.99)
#
#
# #def cross_validation(x,y,num_val=10):
#     r=len(y)
#     idx_list=range(r)
#     err_mat=zeros((num_val,30))
#     for i in range(num_val):
#         train_x,train_y,test_x,test_y=[],[],[],[]
#         random.shuffle(idx_list)
#         for j in range(r):
#             if j<r*0.9:
#                 train_x.append(x[idx_list[j]])
#                 train_y.append(y[idx_list[j]])
#             else:
#                 test_x.append(x[idx_list[j]])
#                 test_y.append(y[idx_list[j]])
#         ws=test_ridge(train_x,train_y)
#         for k in range(30):
#             test_mx=mat(test_x)
#             train_mx=mat(train_x)
#             train_meanx=mean(train_mx,0)
#             train_var=var(train_x,0)
#             test_mx=(test_mx-train_meanx)/train_var
#             y_est=test_mx*mat(ws[k,:]).T+mean(train_y)
#             err_mat[i,k]=RSS(y_est,array(y))
#     mean_err=mean(err_mat)
#     min_mean=float(min(mean_err))
#     best_ws=ws[nonzero(mean_err==min_mean)]
#
#     x_m=mat(x)
#     y_m=mat(y).T
#     mean_x=mean(x_m,0)
#     var_x=var(x_m,0)
#     unreg=best_ws/var_x
#     print("the best model from Ridge Regression is:\n", unreg)
#     print("with constant term: ", -1 * sum(multiply(mean_x, unreg)) + mean(y_m))











