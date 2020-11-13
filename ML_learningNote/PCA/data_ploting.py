# -*- coding: utf-8 -*- 
# @Time : 2020/8/27 17:01 
# @Version: 3.6.5
# @Author : liu hao 
# @File : data_ploting.py

import matplotlib.pyplot as plt
from numpy import *

n=1000
x0,x1,y0,y1=[],[],[],[]
markers,colors=[],[]

fw=open("testSet.txt","w")
for i in range(n):
    [r0,r1]=random.standard_normal(2)
    f_c=r0+9.0
    tats=1.0*r1+f_c+0
    x0.append(f_c)
    y0.append(tats)
    fw.write("%f\t%f\n"%(f_c,tats))

fw.close()
fig=plt.figure()
ax=fig.add_subplot(111)
ax.scatter(x0,y0,marker="^",s=90)
plt.xlabel("hours of direct sunlight")
plt.ylabel("liters of water")
plt.show()