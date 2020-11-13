# -*- coding: utf-8 -*- 
# @Time : 2020/8/27 16:32 
# @Version: 3.6.5
# @Author : liu hao 
# @File : PCA.py



from numpy import *


def load_data(filename,delim="\t"):
    fr=open(filename)
    string_arr=[line.strip().split(delim) for line in fr.readlines()]
    data_arr=[list(map(float,line)) for line in string_arr]
    return mat(data_arr)

"""pca核心算法"""
def pca(data,topK_feat=9999999):
    avg_val=mean(data,axis=0)#计算均值
    avg_remove=data-avg_val#去除均值
    cov_mat=cov(avg_remove,rowvar=0)#对去均值后的数据计算协方差矩阵
    eig_val,eig_vec=linalg.eig(mat(cov_mat))#对协方差矩阵计算特征值和特征向量
    eig_val_sort=argsort(eig_val) #根据特征索引对特征值对特征大小排序，默认从小到大
    eig_val_sort=eig_val_sort[:-(topK_feat+1):-1]#倒序取特征值前K个特征
    reorganize_eig_vec=eig_vec[:,eig_val_sort]#重新组织特征向量
    trans_to_low_dim=avg_remove*reorganize_eig_vec #数据转换到新空间
    recon_mat=(trans_to_low_dim*reorganize_eig_vec.T)+avg_val#降维重构的数据矩阵
    return trans_to_low_dim,recon_mat


def replace_nan_with_mean():
    data=load_data("secom.data"," ")
    num_feat=shape(data)[1]
    for i in range(num_feat):
        avg_val=mean(data[nonzero(~isnan(data[:,i].A))[0],i])

        data[nonzero(isnan(data[:,i].A))[0],i]=avg_val
    return data



