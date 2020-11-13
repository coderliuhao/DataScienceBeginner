# -*- coding: utf-8 -*- 
# @Time : 2020/8/27 17:43 
# @Version: 3.6.5
# @Author : liu hao 
# @File : test_pca_3.py

from numpy import *
import matplotlib.pyplot as plt
import PCA

data=PCA.replace_nan_with_mean()

mean_val=mean(data,axis=0)
mean_removed=data-mean_val
cov_mat=cov(mean_removed,rowvar=0)
eig_val,eig_vec=linalg.eig(mat(cov_mat))
eig_val_idx=argsort(eig_val)
eig_val_idx=eig_val_idx[::-1]
sorted_eig_val=eig_val[eig_val_idx]
total=sum(sorted_eig_val)
var_percent=sorted_eig_val/total*100

fig=plt.figure()
ax=fig.add_subplot(111)
ax.plot(range(1,21),var_percent[:20].tolist(),marker="^")
plt.xlabel('Principal Compoent Number')
plt.ylabel("Percentage of Variance")
plt.show()
