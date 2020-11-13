# -*- coding: utf-8 -*- 
# @Time : 2020/8/18 17:43 
# @Version: 3.6.5
# @Author : liu hao 
# @File : kernel_svm.py

import matplotlib.pyplot as plt
import numpy as np
import random

"""参数含义
data:数据矩阵
labels:数据标签
C:惩罚参数
toler:容错率
kt:核函数信息元组,第一项存放核函数类型，第二项存放核函数参数"""
class Opt:
    def __init__(self,data,labels,C,toler,kt):
        self.X=data
        self.labels=labels
        self.C=C
        self.tol=toler
        self.r=np.shape(data)[0]
        self.alphas=np.mat(np.zeros((self.r,1)))
        self.b=0
        self.err_cache=np.mat(np.zeros((self.r,2)))#误差缓存：第一列为是否有效的标志位，第二列为实际误差之
        self.K=np.mat(np.zeros((self.r,self.r)))
        for i in range(self.r):
            self.K[:,i]=kernel_trans(self.X,self.X[i,:],kt)

def kernel_trans(X,A,kt):
    r,c=np.shape(X)
    K=np.mat(np.zeros((r,1)))
    if kt[0]=="linear":
        K=X*A.T
    elif kt[0]=="rbf":
        for j in range(r):
            row_dist=X[j,:]-A
            K[j]=row_dist*row_dist.T
        K=np.exp(K/(-1*kt[1]**2))
    else:
        raise NameError("和函数无法识别")
    return K

def load_data(filename):
    data,labels=[],[]
    fr=open(filename)
    for line in fr.readlines():
        line_arr=line.strip().split("\t")
        data.append([float(line_arr[0]),float(line_arr[1])])
        labels.append(float(line_arr[-1]))
    return data,labels

"""计算标号为k的数据的误差"""
def cal_errk(ds,k):
    f_xk=float(np.multiply(ds.alphas,ds.labels).T*ds.K[:,k]+ds.b)
    errk=f_xk-float(ds.labels[k])
    return errk

"""随机选择alpha_j的索引"""
def rand_alpha_j(i,r):
    j=i
    while j==i:
        j=int(random.uniform(0,r))
    return j

"""内循环启发式寻找j并计算标号j的数据误差err_j"""
def heur_select_j(i,ds,err_i):
    max_K=-1
    max_err_changed=0
    err_j=0
    ds.err_cache[i]=[1,err_i]
    valid_err_cache=np.nonzero(ds.err_cache[:,0].A)[0]
    if len(valid_err_cache)>1:
        for k in valid_err_cache:
            if k==i:
                continue
            err_k=cal_errk(ds,k)
            err_change=abs(err_i-err_k)
            if err_change>max_err_changed:
                max_K=k
                max_err_changed=err_change
                err_j=err_k
        return max_K,err_j
    else:
        j=rand_alpha_j(i,ds.r)
        err_j=cal_errk(ds,j)
    return j,err_j

"""计算err_k并更新误差缓存"""
def update_errk(ds,k):
    err_k=cal_errk(ds,k)
    ds.err_cache[k]=[1,err_k]

"""修建alpha的值，超过上界时修剪为上界，低于下界时修剪成下界"""
def clip_alpha(aj,sup,inf):
    if aj>sup:
        aj=sup
    if aj<inf:
        aj=inf
    return aj

"""优化的SMO算法"""
"""标志位介绍：1:有任一一对alpha的值发生变化 
            0:没有任意一对alpha值发生变化
            
"""
def modified_smo(i,ds):
    err_i=cal_errk(ds,i)
    if ((ds.labels[i]*err_i<-ds.tol) and (ds.alphas[i]<ds.C)) or ((ds.labels[i]*err_i>ds.tol) and (ds.alphas[i]>0)):
        j,err_j=heur_select_j(i,ds,err_i)
        alpha_i_old=ds.alphas[i].copy()
        alpha_j_old=ds.alphas[j].copy()

        if ds.labels[i]!=ds.labels[j]:
            sup=min(ds.C,ds.C+ds.alphas[j]-ds.alphas[i])
            inf=max(0,ds.alphas[j]-ds.alphas[i])
        else:
            sup=min(ds.C,ds.alphas[j]+ds.alphas[i])
            inf=max(0,ds.alphas[j]+ds.alphas[i]-ds.C)
        if sup==inf:
            print("sup=inf")
            return 0

        eta=2.0*ds.K[i,j]-ds.K[i,i]-ds.K[j,j]
        if eta>=0:
            print("eta>=0")
            return 0

        ds.alphas[j]-=ds.labels[j]*(err_i-err_j)/eta
        ds.alphas[j]=clip_alpha(ds.alphas[j],sup,inf)

        update_errk(ds,j)
        if abs(ds.alphas[j]-alpha_j_old)<0.00001:
            print("alpha_j变化太小")
            return 0

        ds.alphas[i]+=ds.labels[j]*ds.labels[i]*(alpha_j_old-ds.alphas[j])
        update_errk(ds,i)

        b1=ds.b-err_i-ds.labels[i]*(ds.alphas[i]-alpha_i_old)*ds.K[i,i]-ds.labels[j]*(ds.alphas[j]-alpha_j_old)*ds.K[i,j]
        b2=ds.b-err_j-ds.labels[i]*(ds.alphas[i]-alpha_i_old)*ds.K[i,j]-ds.labels[j]*(ds.alphas[j]-alpha_j_old)*ds.K[j,j]

        if ds.alphas[i]>0 and ds.C>ds.alphas[i]:
            ds.b=b1
        elif ds.alphas[j]>0 and ds.C>ds.alphas[j]:
            ds.b=b2
        else:
            ds.b=(b1+b2)/2.0
        return 1
    else:
        return 0

"""完整的SMO算法"""
def SOM(data,labels,C,toler,max_iter,kt=("linear",0)):
    ds=Opt(np.mat(data),np.mat(labels).transpose(),C,toler,kt)
    iter=0
    all_data=True
    alpha_pair_changed=0
    while (iter<max_iter) and ((alpha_pair_changed>0) or (all_data)):
        alpha_pair_changed=0
        if all_data:
            for i in range(ds.r):
                alpha_pair_changed+=modified_smo(i,ds)
                print("全样本遍历:第%d次迭代 样本:%d,alpha优化次数:%d"%(iter,i,alpha_pair_changed))
            iter+=1
        else:
            nonbound=np.nonzero((ds.alphas.A>0)*(ds.alphas.A<C))[0]
            for i in nonbound:
                alpha_pair_changed+=modified_smo(i,ds)
                print("非边界遍历:第%d次迭代  样本:%d,alpha优化次数:%d"%(iter,i,alpha_pair_changed))
            iter+=1
        if all_data:
            all_data=False
        elif alpha_pair_changed==0:
            all_data=True
        print("迭代次数:%d"%iter)
    return ds.b,ds.alphas

"""测试RBF核函数    参数为到达率"""
def test_rbf(k1=1.3):
    data,labels=load_data("testSetRBF.txt")
    b,alphas=SOM(data,labels,200,0.0001,100,("rbf",k1))
    data_mat=np.mat(data)
    label_mat=np.mat(labels).transpose()
    spt_idx=np.nonzero(alphas.A>0)[0]
    spt_vec=data_mat[spt_idx]
    labels_sv=label_mat[spt_idx]
    print("支持向量的个数:%d"%np.shape(spt_vec)[0])

    r,c=np.shape(data_mat)
    err_stat=0.0
    for i in range(r):
        kernel_eval=kernel_trans(spt_vec,data_mat[i,:],("rbf",k1))
        predict=kernel_eval.T*np.multiply(labels_sv,alphas[spt_idx])+b
        if np.sign(predict)!=np.sign(labels[i]):
            err_stat+=1
    print("训练集错误率:%.2f%%"%((float(err_stat)/r)*100))

    test_X,test_label=load_data("testSetRBF2.txt")
    err_stat=0.0
    test_X_mat=np.mat(test_X)
    r,c=np.shape(test_X_mat)
    for i in range(r):
        kernel_eval=kernel_trans(spt_vec,test_X_mat[i,:],("rbf",k1))
        predict=kernel_eval.T*np.multiply(labels_sv,alphas[spt_idx])+b
        if np.sign(predict)!=np.sign(test_label[i]):
            err_stat+=1
    print("测试集错误率:%.2f%%"%(float(err_stat/r)*100))

"""可视化"""
def show_data(data,labels):

    data_p,data_n=[],[]
    for i in range(len(data)):
        if labels[i]>0:
            data_p.append(data[i])
        else:
            data_n.append(data[i])
    data_p_arr=np.array(data_p)
    data_n_arr=np.array(data_n)
    plt.scatter(np.transpose(data_p_arr)[0],np.transpose(data_p_arr)[1],s=30,c="blue",alpha=0.7)
    plt.scatter(np.transpose(data_n_arr)[0],np.transpose(data_n_arr)[1],s=30,c="red",alpha=0.7)
    plt.show()

if __name__=="__main__":
    test_rbf()
    data,labels=load_data("testSetRBF.txt")
    show_data(data,labels)



