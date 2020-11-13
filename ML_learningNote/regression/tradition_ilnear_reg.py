# -*- coding: utf-8 -*- 
# @Time : 2020/8/21 23:41 
# @Version: 3.6.5
# @Author : liu hao 
# @File : tradition_ilnear_reg.py

from numpy import *

def load_data(filename):
    num_col=len(open(filename).readline().split("\t"))-1
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

"""标准回归方程求解-最小二乘法求解得到-容易欠拟合  LR有参数学习方法
   在训练完所有数据之后得到一系列训练参数，然后根据训练参数来预测样本
   的值这时不再依赖之前的训练数据，参数是确定的"""
def standard_regression(X,y):
    X_mat=mat(X)
    y_mat=mat(y).T
    xTx=X_mat.T*X_mat
    if linalg.det(xTx)==0.0:
        print("This matrix is singular,cannot do inverse")
        return
    ws=xTx.I*(X_mat.T*y_mat)
    return ws

"""局部加权线性回归模型-解决线性回归中存在的欠拟合问题    LWLR非参数学习方法
   在预测新样本值时每次都会重新训练新的参数，也就是每次预测新的样本值都会依赖训练数据集合，
所以每次的参数是不确定的.
   对每个点做预测时都必须使用整个数据集，因此当训练容量过大时，非参数学习算法需要占用更多的存储容量，
计算速度较慢.
   对于样本的预测，其实就是对每个点的预测（或者说拟合）m样本点有m个点，则预测出来的也是m个点，
而这m个点不在一条直线上，而是离散的点,因此最终拟合的'线性'（实为非线性）
曲线则是m个点的（m-1条线段）组成的估计曲线"""

def local_weighted_lr(test_p,X,y,k=1.0):
    X_mat=mat(X)
    y_mat=mat(y)
    r=shape(X_mat)[0]
    weights=mat(eye((r)))
    for j in range(r):
        diff_X=test_p-X_mat[j,:]
        weights[j,j]=exp(diff_X*diff_X.T/(-2.0*k**2))
    xTx=X_mat.T*(weights*X_mat)
    if linalg.det(xTx)==0.0:
        print("This matrix is singular,cannot do inverse")
        return
    ws=xTx.I*(X_mat.T*(weights*y_mat))
    return test_p*ws

def local_weighted_test(test_X,X,y,k=1.0):
    r=shape(test_X)[0]
    y_hat=zeros(r)
    for i in range(r):
        y_hat[i]=local_weighted_lr(test_X[i],X,y,k)
    return y_hat

def lw_test_plot(X,y,k=1.0):
    y_hat=zeros(shape(y))
    X_cp=mat(X)
    y_cp=mat(y)
    X_cp.sort()
    for i in range(shape(X)[0]):
        y_hat[i]=local_weighted_lr(X_cp[i],X,y,k)
    return y_hat,X_cp

def RSS(y,y_hat):
    return ((y-y_hat)**2).sum()

"""岭回归-解决过拟合问题
# 在增加约束时，普通的最小二乘法回归会得到与岭回归的一样的公式，
也就是说在增加约束情况下，最少二乘法可以转化为岭回归"""
def ridge_reg(X,y,lam=0.2):
    xTx=X.T*X
    denom=xTx+eye(shape(X)[1])*lam
    if linalg.det(denom)==0.0:
        print("This matrix is singular,cnnot do inverse")
        return
    ws=denom.I*(X.T*y)
    return ws

def ridge_test(X,y):
    X_mat=mat(X)
    y_mat=mat(y)
    y_mean=mean(y_mat,0)
    y_mat=y_mat-y_mean
    X_mean=mean(X_mat,0)
    X_var=var(X_mat,0)
    X_mat=(X_mat-X_mean)/X_var
    num_test_points=30
    weights_mat=zeros((num_test_points,shape(X_mat)[1]))
    for i in range(num_test_points):
        ws=ridge_reg(X_mat,y_mat,exp(i-10))
        weights_mat[i,:]=ws.T
    return weights_mat

def regularize(X):
    x_in=X.coopy()
    mean_in=mean(x_in,0)
    var_in=var(x_in,0)
    x_in=(x_in-mean_in)/var_in
    return x_in

"""前向逐步回归"""
"""前向逐步线性回归-使用贪心算法来达到L1正则化的效果，本质上也是
缩减系数，有很多随机性"""
def stage_wise(X,y,eps=0.01,num_iter=100):
    X_mat=mat(X)
    y_mat=mat(y).T
    y_mean=mean(y,0)
    y_mat=y_mat-y_mean
    X_mat=regularize(X_mat)

    r,c=shape(X_mat)
    res_mat=zeros((num_iter,c))
    ws=zeros((c,1))
    ws_test=ws.copy()
    ws_max=ws.copy()
    for i in range(num_iter):
        min_err=inf
        for j in range(c):
            for sign in [-1,1]:

                ws_test=ws.copy()
                ws_test[j]+=eps*sign
                y_test=X_mat*ws_test
                rss=RSS(y_mat.A,y_test.A)
                if rss<min_err:
                    min_err=rss
                    ws_max=ws_test
        ws=ws_max.copy()
        res_mat[i,:] = ws.T
    return res_mat

def scrapy_webpage(file_in,file_out,yr,num__pce,orig_prc):
    from bs4 import BeautifulSoup

    fr=open(file_in)
    fw=open(file_out,"a")
    soup=BeautifulSoup(fr.read())
    i=1
    cur_row=soup.findAll("table",r="%d"%i)
    while len(cur_row)!=0:
        cur_row=soup.findAll("table",r="%d"%i)
        title=cur_row[0].findAll("a")[1].text
        lower_title=title.lower()
        if (lower_title.find("new")>-1) or (lower_title.find("nisb")>-1):
            new_flag=1.0
        else:
            new_flag=0.0
        sold_unicde=cur_row[0].findAll("td")[3].findAll("span")

        if len(sold_unicde)==0:
            print("item #%d did not sell"%i)
        else:
            sold_price=cur_row[0].findAll("td")[4]
            price_str=sold_price.text
            price_str=price_str.replace("$","")
            price_str=price_str.replace(",","")
            if len(sold_price)>1:
                price_str=price_str.replace("Free shipping","")
            print("%s\t%d\t%d\t%f\t%s\n"%(price_str,new_flag,title))
            fw.write("%d\t%d\t%d\t%f\t%s\n"%(yr,num__pce,new_flag,orig_prc,price_str))
        i+=1
        cur_row=soup.findAll("table",r="%d"%i)
    fw.close()

def set_dataset():
    scrapy_webpage("setHtml/lego8288.html","out.txt",2006,800,49.99)
    scrapy_webpage("setHtml/lego10030.html","out.txt",2002,3096,269.99)
    scrapy_webpage("setHtml/lego10179.html","out.txt",2007,5195,499.99)
    scrapy_webpage("setHtml/lego10181.html","out.txt",2007,3428,199.99)
    scrapy_webpage("setHtml/lego10189.html","out.txt",2008,5922,299.99)
    scrapy_webpage("setHtml/lego10196.html","out.txt",2009,3263,249.99)

def cross_validation(X,y,num_fold=10):
    r=len(y)
    idx_lst=range(r)
    err_mat=zeros((num_fold,30))
    for i in range(num_fold):
        train_X,train_y,test_X,test_y=[],[],[],[]
        random.shuffle(idx_lst)
        for j in range(r):
            if j< r*.9:
                train_X.append(X[idx_lst[j]])
                train_y.append(y[idx_lst[j]])
            else:
                test_X.append(X[idx_lst[j]])
                test_y.append(y[idx_lst[j]])
        weights=ridge_test(train_X,train_y)
        for k in range(30):
            test_mat=mat(test_X)
            train_mat=mat(train_X)
            mean_train=mean(train_mat,0)
            var_train=mean(train_mat,0)
            test_mat=(test_mat-mean_train)/var_train
            y_pre=test_mat*mat(weights[k,:]).T+mean(train_y)
            err_mat[i,k]=RSS(array(test_y),y_pre.T.A)
    mean_err=mean(err_mat,0)
    min_mean=float(min(mean_err))
    best_weights=weights[nonzero(mean_err==min_mean)]

    X_mat=mat(X)
    y_mat=mat(y).T
    mean_X=mean(X_mat,0)
    var_X=var(X_mat,0)
    unregularized=best_weights/var_X
    print("the best model from ridge regression is \n",unregularized)
    print("with constant term:",-1*sum(multiply(mean_X,unregularized))+mean(y_mat))



