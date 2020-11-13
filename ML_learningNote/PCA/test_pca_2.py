# -*- coding: utf-8 -*- 
# @Time : 2020/8/27 17:28 
# @Version: 3.6.5
# @Author : liu hao 
# @File : test_pca_2.py


from numpy import *
import matplotlib.pyplot as plt
import PCA

n=1000
x0,x1,x2,y0,y1,y2=[],[],[],[],[],[]
markers,colors=[],[]
fw=open("testSet3.txt","w")
for i in range(n):
    group_num=int(3*random.uniform())
    [r0,r1]=random.standard_normal(2)
    if group_num==0:
        x=r0+16.0
        y=1.0*r1+x
        x0.append(x)
        y0.append(y)
    elif group_num==1:
        x=r0+8.0
        y=1.0*r1+x
        x1.append(x)
        y1.append(y)
    elif group_num==2:
        x=r0+0.0
        y=1.0*r1+x
        x2.append(x)
        y2.append(y)
    fw.write("%f\t%f\t%d\n"%(x,y,group_num))
fw.close()
fig=plt.figure()
ax=fig.add_subplot(211)
ax.scatter(x0,y0,marker="^",s=90)
ax.scatter(x1,y1,marker="o",s=50,c="red")
ax.scatter(x2,y2,marker="v",s=50,c="yellow")

ax=fig.add_subplot(212)
dat=PCA.load_data("testSet3.txt")
low_dim_dat,recon_dat=PCA.pca(dat[:,0:2],1)
label0=low_dim_dat[nonzero(dat[:,2]==0)[0],:2][0]
label1=low_dim_dat[nonzero(dat[:,2]==1)[0],:2][0]
label2=low_dim_dat[nonzero(dat[:,2]==2)[0],:2][0]

ax.scatter(label0[:,0].tolist(),zeros(shape(label0)[0]),marker="^",s=90)
ax.scatter(label1[:,0].tolist(),zeros(shape(label1)[0]),marker="o",s=50,c="red")
ax.scatter(label2[:,0].tolist(),zeros(shape(label2)[0]),marker="v",s=50,c="yellow")
plt.show()
