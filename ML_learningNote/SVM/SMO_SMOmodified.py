# -*- coding: utf-8 -*- 
# @Time : 2020/8/18 0:34 
# @Version: 3.6.5
# @Author : liu hao 
# @File : SMO_SMOmodified.py

import matplotlib.pyplot as plt
import numpy as np
import random


class Opt:
    def __init__(self, data, labels, C, toler):
        self.X = data
        self.labels = labels
        self.C = C
        self.tol = toler
        self.r = np.shape(data)[0]
        self.alphas = np.mat(np.zeros((self.r, 1)))
        self.b = 0
        self.err_cache = np.mat(np.zeros((self.r, 2)))

def load_data(filename):
    fr=open(filename)
    data,labels=[],[]
    for line in fr.readlines():
        line_arr=line.strip().split("\t")
        data.append([float(line_arr[0]),float(line_arr[1])])
        labels.append(float(line_arr[-1]))
    return data,labels

def cal_err(ds,k):
    f_xk=float(np.multiply(ds.alphas,ds.labels).T*(ds.X*ds.X[k,:].T)+ds.b)
    err_k=f_xk-float(ds.labels[k])
    return err_k

def select_alphaj_idx(i,r):
    j=i
    while j==i:
        j=int(random.uniform(0,r))
    return j

def select_j(i,ds,err_i):

    max_K=-1
    max_err_changed=0
    err_j=0
    ds.err_cache[i]=[i,err_i]
    valid_err_cache=np.nonzero(ds.err_cache[:,0].A)[0]
    if len(valid_err_cache)>1:
        for k in valid_err_cache:
            if k==i:
                continue
            err_k=cal_err(ds,k)
            err_changed=abs(err_i-err_k)
            if err_changed>max_err_changed:
                max_K=k
                max_err_changed=err_changed
                err_j=err_k
        return max_K,err_j
    else:
        j=select_alphaj_idx(i,ds.r)
        err_j=cal_err(ds,j)
    return j,err_j

def update_errk(ds,k):
    err_k=cal_err(ds,k)
    ds.err_cache[k]=[1,err_k]

def clip_alpha(aj,sup,inf):
    if aj>sup:
        aj=sup
    if aj<inf:
        aj=inf
    return aj


"""优化的SMO算法"""
def modified_smo(ds,i):
    err_i=cal_err(ds,i)
    if ((ds.labels[i]*err_i<-ds.tol) and (ds.alphas[i]<ds.C)) or ((ds.labels[i]*err_i>ds.tol) and (ds.alphas[i]>0)):
        j,err_j=select_j(i,ds,err_i)
        alpha_i_old=ds.alphas[i].copy()
        alpha_j_old=ds.alphas[j].copy()
        if ds.labels[i]!=ds.labels[j]:
            inf=max(0,ds.alphas[j]-ds.alphas[i])
            sup=min(ds.C,ds.C+ds.alphas[j]-ds.alphas[i])
        else:
            inf=max(0,ds.alphas[j]+ds.alphas[i]-ds.C)
            sup=max(ds.C,ds.alphas[j]+ds.alphas[i])
        if sup==inf:
            print("sup=inf")
            return 0

        eta=2.0*ds.X[i,:]*ds.X[j,:].T-ds.X[i,:]*ds.X[i,:].T-ds.X[j,:]*ds.X[j,:].T
        if eta>=0:
            print("eta>=0")
            return 0

        ds.alphas[j]-=ds.labels[j]*(err_i-err_j)/eta

        ds.alphas[j]=clip_alpha(ds.alphas[j],sup,inf)

        update_errk(ds,j)
        if abs(ds.alphas[j]-alpha_j_old)<0.000001:
            print("alpha_j变化太小")
            return 0
        ds.alphas[i]+=ds.labels[j]*ds.labels[i]*(alpha_j_old-ds.alphas[j])
        update_errk(ds,i)
        b1=ds.b-err_i-ds.labels[i]*(ds.alphas[i]-alpha_i_old)*ds.X[i,:]*ds.X[i,:].T-ds.labels[j]*(ds.alphas[j]-alpha_j_old)*ds.X[i,:]*ds.X[j,:].T
        b2=ds.b-err_j-ds.labels[i]*(ds.alphas[i]-alpha_i_old)*ds.X[i,:]*ds.X[j,:].T-ds.labels[j]*(ds.alphas[j]-alpha_j_old)*ds.X[j,:]*ds.X[j,:].T

        if (ds.alphas[i]>0) and(ds.C>ds.alphas[i]):
            ds.b=b1
        elif (ds.alphas[j]>0) and (ds.C>ds.alphas[j]):
            ds.b=b2
        else:
            ds.b=(b1-b2)/2.0
        return 1
    else:
        return 0

"""完整的SMO算法"""
def linear_SMO_algo(data,labels,C,toler,max_iter):
    ds=Opt(np.mat(data),np.mat(labels).transpose(),C,toler)
    iter=0
    all_data=True
    alpha_pair_changed=0
    while (iter<max_iter) and ((alpha_pair_changed>0) or (all_data)):
        alpha_pair_changed=0
        if all_data:
            for i in range(ds.r):
                alpha_pair_changed+=modified_smo(ds,i)
                print("全样本遍历:第%d次迭代 样本:%d,alpha优化次数:%d" %(iter,i,alpha_pair_changed))
            iter+=1
        else:
            non_bound_i=np.nonzero((ds.alphas.A>0)*(ds.alphas.A<C))[0]
            for i in non_bound_i:
                alpha_pair_changed+=modified_smo(ds,i)
                print("非边界遍历:第%d次迭代 样本:%d,alpha优化次数:%d"%(iter,i,alpha_pair_changed))
            iter+=1
        if all_data:
            all_data=False
        elif alpha_pair_changed==0:
            all_data=True
        print("迭代次数:%d"%iter)
    return ds.b,ds.alphas

def show_classified_res(data,labels,w,b,alphas):
    data_p=[]
    data_n=[]
    for i in range(len(data)):
        if labels[i]>0:
            data_p.append(data[i])
        else :
            data_n.append(data[i])
    data_p_arr=np.array(data_p)
    data_n_arr=np.array(data_n)

    plt.scatter(np.transpose(data_p_arr)[0],np.transpose(data_p_arr)[1],s=30,c="red",alpha=0.7)
    plt.scatter(np.transpose(data_n_arr)[0],np.transpose(data_n_arr)[1],s=30,c="blue",alpha=0.7)

    x1=max(data)[0]
    x2=min(data)[0]
    a1,a2=w
    b=float(b)
    a1=float(a1[0])
    a2=float(a2[0])
    y1,y2=(-b-a1*x1)/a2,(-b-a1*x2)/a2
    plt.plot([x1,x2],[y1,y2])
    for i,alpha in enumerate(alphas):
        if abs(alpha)>0:
            x,y=data[i]
            plt.scatter([x],[y],s=150,c="none",alpha=0.7,linewidths=1.5,edgecolor="red")
    plt.show()

def cal_w(alphas,data,labels):
    X=np.mat(data)
    labels=np.mat(labels).transpose()
    r,c=np.shape(X)
    w=np.zeros((c,1))
    for i in range(r):
        w+=np.multiply(alphas[i]*labels[i],X[i,:].T)
    return w

if __name__=="__main__":
    data,labels=load_data("testSet.txt")
    b,alphas=linear_SMO_algo(data,labels,0.6,0.001,40)
    w=cal_w(alphas,data,labels)
    show_classified_res(data,labels,w,b,alphas)





