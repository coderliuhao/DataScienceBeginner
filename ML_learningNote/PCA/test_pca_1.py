# -*- coding: utf-8 -*- 
# @Time : 2020/8/27 17:10 
# @Version: 3.6.5
# @Author : liu hao 
# @File : test_pca_1.py

import matplotlib.pyplot as plt
import PCA

data=PCA.load_data("testSet.txt")
low_dim_mat,recon_mat=PCA.pca(data,1)
fig=plt.figure()
ax=fig.add_subplot(111)
ax.scatter(data[:,0].tolist(),data[:,1].tolist(),marker="^",s=90)
ax.scatter(recon_mat[:,0].tolist(),recon_mat[:,1].tolist(),marker='o',s=50,c="red")
plt.show()
