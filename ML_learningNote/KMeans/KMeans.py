# -*- coding: utf-8 -*- 
# @Time : 2020/8/23 18:20 
# @Version: 3.6.5
# @Author : liu hao 
# @File : KMeans.py

from numpy import *

"""读取数据"""
def load_data(filename):
    data=[]
    fr=open(filename)
    for line in fr.readlines():
        curline=line.strip().split("\t")
        filtline=list(map(float,curline))
        data.append(filtline)
    return data

"""计算欧氏距离"""
def dist_eclud(vec1,vec2):
    return sqrt(sum(power(vec1-vec2,2)))

"""随机选取聚类中心"""
def random_center(data,k):
    c=shape(data)[1]
    centroids=mat(zeros((k,c)))
    for j in range(c):
        min_j=min(data[:,j])# 计算列最小值
        range_j=float(max(data[:,j])-min_j)#计算极差
        centroids[:,j]=mat(min_j+range_j*random.rand(k,1))#对每列获取一个在极差范围内的均匀分布随机数
    return centroids

def kmeans(data,k,dist=dist_eclud,creat_cent=random_center):
    r=shape(data)[0] #获取行数
    in_cluster_dist=mat(zeros((r,2))) #初始化储存结果的矩阵包含每个样本点的簇标签和样本点到该簇质心的距离
    centroids=creat_cent(data,k)#随机获取质心
    cluster_changed=True#while循环的标志位

    while cluster_changed:#当各个样本的簇不发生改变时推出循环
        cluster_changed=False
        for i in range(r):#遍历所有样本点
            min_dist=inf #用于贪心算法求最小距离
            min_index=-1 #初始化所在的簇索引
            for j in range(k):#遍历所有的簇
                dist_ij=dist(centroids[j,:],data[i,:])#计算当前簇质心到第i个样本的距离
                if dist_ij<min_dist:#贪心算法，寻找距离样本i最小距离的那个簇及编号
                    min_dist=dist_ij
                    min_index=j
            if in_cluster_dist[i,0]!=min_index:#标志位判断，如果第i个样本点的簇编号不等于当前寻找的距离i样本最小距离的簇编号，则反转标志位用于继续循环
                cluster_changed=True
            in_cluster_dist[i,:]=min_index,min_dist**2#记录当前样本i的簇和到簇中心的距离信息
        print("------循环一次-------")
        print(centroids)
        for cent in range(k):
            in_cluster_data=data[nonzero(in_cluster_dist[:,0].A==cent)[0]]#获取每个簇下的所有数据
            if len(in_cluster_data) != 0:
                centroids[cent,:]=mean(in_cluster_data,0)#将各个簇的质心更新为各个簇数据的列均值
    return centroids,in_cluster_dist

"""二分KMeans算法"""
def binary_kmeans(data,k,dist=dist_eclud):
    r=shape(data)[0]
    in_cluster_dist=mat(zeros((r,2)))
    centroid_base=mean(data,0)#初始化质心为列均值

    centroid_list=[centroid_base]

    for j in range(r):
        in_cluster_dist[j,1]=dist(mat(centroid_base),data[j,:])**2
    while len(centroid_list)<k:
        min_err=inf
        for i in range(len(centroid_list)):
            in_cluster_data=data[nonzero(in_cluster_dist[:,0].A==i)[0],:]
            centroid_mat,split_data=kmeans(in_cluster_data,2,dist)

            sse_split=sum(split_data[:,1])

            sse_not_in_i=sum(in_cluster_dist[nonzero(in_cluster_dist[:,0].A!=i)[0],1])

            print("sse_split:",sse_split)
            print("sse_not_split:",sse_not_in_i)

            if (sse_split+sse_not_in_i)<min_err:
                min_err=sse_split+sse_not_in_i
                best_cent_to_split=i
                best_new_cent=centroid_mat
                best_clust=split_data.copy()

        best_clust[nonzero(best_clust[:,0].A==1)[0],0]=len(centroid_list)
        best_clust[nonzero(best_clust[:,0].A==0)[0],0]=best_cent_to_split

        print("the best center to split is:",best_cent_to_split)
        print("the length of best_clust is :",len(best_clust))

        centroid_list[best_cent_to_split]=best_new_cent[0,:].tolist()[0]
        centroid_list.append(best_new_cent[1,:].tolist()[0])

        in_cluster_dist[nonzero(in_cluster_dist[:,0].A==best_cent_to_split)[0],:]=best_clust
    return mat(centroid_list),in_cluster_dist

if __name__ == '__main__':
    "test1: Kmeans"
    data=mat(load_data("testSet.txt"))
    center,cluster_res=kmeans(data,4)

    """test2 binary_kmeans"""
    center,cluster_res=binary_kmeans(data,3)











