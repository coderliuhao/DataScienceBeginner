# -*- coding: utf-8 -*- 
# @Time : 2020/8/28 16:41 
# @Version: 3.6.5
# @Author : liu hao 
# @File : SVD.py


from numpy import *
from numpy import linalg as la

def load_example1():
    return[[0, 0, 0, 2, 2],
           [0, 0, 0, 3, 3],
           [0, 0, 0, 1, 1],
           [1, 1, 1, 0, 0],
           [2, 2, 2, 0, 0],
           [5, 5, 5, 0, 0],
           [1, 1, 1, 0, 0]]



"""数据集说明：
行:代表人
列:菜肴名
值:代表人对菜肴的评分"""
def load_example2():
    return[[0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 5],
           [0, 0, 0, 3, 0, 4, 0, 0, 0, 0, 3],
           [0, 0, 0, 0, 4, 0, 0, 1, 0, 4, 0],
           [3, 3, 4, 0, 0, 0, 0, 2, 2, 0, 0],
           [5, 4, 5, 0, 0, 0, 0, 5, 5, 0, 0],
           [0, 0, 0, 0, 5, 0, 1, 0, 0, 5, 0],
           [4, 3, 4, 0, 0, 0, 0, 5, 5, 0, 1],
           [0, 0, 0, 4, 0, 4, 0, 0, 0, 0, 4],
           [0, 0, 0, 2, 0, 2, 5, 0, 0, 1, 2],
           [0, 0, 0, 0, 5, 0, 0, 0, 0, 4, 0],
           [1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0]]
"""计算欧氏距离相似度"""
def eclu_similarity(ds1,ds2):
    return 1.0/(1.0+la.norm(ds1-ds2))
"""皮尔逊相关系数"""
def pearsonr_similarity(ds1,ds2):
    if len(ds1)<3:
        return 1.0
    return 0.5+0.5*corrcoef(ds1,ds2,rowvar=0)[0][1]
"""余弦相似度"""
def cosin_similarity(ds1,ds2):
    num=float(ds1.T*ds2)
    denorm=la.norm(ds1)*la.norm(ds2)
    return 0.5+0.5*(num/denorm)



"""基于物品相似度估计的推荐"""
"""参数说明:
data:训练数据
user:用户编号
similar_method:相似度计算方法
item:未被评分的物品编号"""
def similar_based_estim(data,user,similar_method,item):
    c=shape(data)[1]  #计算物品数量
    similar_total=0.0         #初始化两个评分为0
    rating_similar_total=0.0
    for j in range(c): #遍历每个物品，对用户评过分的物品进行遍历，并将它与其他物品进行比较
        user_rating=data[user,j] #获得该用户对j物品的评分
        if user_rating==0: #如果评分为0，跳过该物品
            continue
        #寻找两个都被所有用户评分的物品，overlap表示两个物品中已经被评分的元素的索引，

        overlap=nonzero(logical_and(data[:,item].A>0,data[:,j].A>0))[0]
        #如果overlap长度为0，说明没有重合元素，置相似度为0，终止循环
        if len(overlap)==0:
            similarity=0
        else:#如果存在重合的物品，则基于这些物品计算相似度
            similarity=similar_method(data[overlap,item],data[overlap,j])
        #相似度不断累加
        similar_total+=similarity
        #累加相似度与用户评分的乘积
        rating_similar_total+=similarity*user_rating
    if similar_total==0:
        return 0
    else: #除以所有评分和，归一化分数，使评分落在0`5之间，作为对预测值排序的依据
        return rating_similar_total/similar_total

"""基于svd评分估计"""
"""参数说明
data:训练数据集
user:用户编号
similar_method:相似度计算方法"""

def svd_based_estim(data,user,similar_method,item):
    c=shape(data)[1]   #物品数量
    similar_total=0.0    #舒适化相似度和，评分与相似度乘积和
    rating_similar_total=0.0
     #在SVD分解之后，我们只利用包含90 % 能量值的奇异值sigma，这些奇异值会以Numpy数组形式得以保存
    U,sigma,VT=la.svd(data)
    sig=mat(eye(4)*sigma[:4])#用奇异值构建对角阵，方便后续矩阵运算
    trans_item=data.T*U[:,:4]*sig.I  #U矩阵将物品转换到低维空间，用物品的4个特征构建转换后的物品矩阵
    for j in range(c):
        user_rating=data[user,j] #遍历某用户对每个物品的评分值
        if user_rating==0 or j==item: #用户评分为0则跳过
            continue
        #对用户都评分的两个物品按照similar_method参数计算相似度
        similarity=similar_method(trans_item[item,:].T,trans_item[j,:].T)#
        print("the %d and %d similarity is: %.f"%(item,j,similarity))
        similar_total+=similarity
        rating_similar_total+=similarity*user_rating
    if similar_total==0:
        return 0
    else:
        return rating_similar_total/similar_total

"""推荐引擎"""
"""参数说明:
data:训练数据
user:指定用户编号
N:产生N个推荐结果
similar_method:相似度计算方法
esti_method:推荐引擎方法"""
def recommend_proc(data,user,N=3,similar_method=cosin_similarity,esti_method=similar_based_estim):
    #寻找未评级的物品，对指定用户建立未评分物品列表
    unrated_item=nonzero(data[user,:].A==0)[1]
    #若物品均评分，则函数终止
    if len(unrated_item)==0:
        return "you rated everything"
    #建立列表存储物品编号和评分值
    item_scores=[]
    for item in unrated_item:#遍历所有未评分的物品，通过esti_method预测前N个未评级物品的评分
        estim_score=esti_method(data,user,similar_method,item)
        item_scores.append((item,estim_score))
    return sorted(item_scores,key=lambda r:r[1],reverse=True)[:N]#按照评分值对前N个未评分的物品编号降序排列

"""图像压缩"""
def analyse_data(Sigma, loopNum=20):
    # 总方差的集合（总能量值）
    Sig2 = Sigma ** 2
    SigmaSum = sum(Sig2)
    for i in range(loopNum):
        # 根据自己的业务情况，进行处理，设置对应的Sigma次数
        # 通常保留矩阵80%~90%的能量，就可以得到重要的特征并去除噪声
        SigmaI = sum(Sig2[:i+1])
        print('主成分：%s, 方差占比: %s%%' % (format(i+1, '2.0f'), format(SigmaI / SigmaSum * 100, '4.2f')))


def print_mat(mat_in,thresh=0.8):
    for i in range(32):
        for k in range(32):
            if float(mat_in[i,k])>thresh:
                print(1,end=" ")
            else:
                print(0,end=" ")
        print("")

def img_compress(num_sv=3,thresh=0.8):
    myl=[]
    for line in open("0_5.txt").readlines():
        new_row=[]
        for i in range(32):
            new_row.append(int(line[i]))
        myl.append(new_row)
    mymat=mat(myl)
    print("=====original matrix=======")
    print_mat(mymat,thresh)
    U,sigma,VT=la.svd(mymat)
    analyse_data(sigma,20)
    sig_recon=mat(eye(num_sv)*sigma[:num_sv])
    reconmat=U[:,:num_sv]*sig_recon*VT[:num_sv,:]
    #sig_reconst=mat(zeros((num_sv,num_sv)))
    #for k in range(num_sv):
       # sig_reconst[k,k]=sigma[k]
    # reconmat=U[:,:num_sv]*sig_reconst*VT[:num_sv,:]
    print("======reconstructed matrix using %d singular values========"%num_sv)
    print_mat(reconmat,thresh)

if __name__ == '__main__':
    img_compress(num_sv=3,thresh=0.8)
    #data1=mat(load_example1())
    #data2=mat(load_example2())
    #recommend_proc(data2,1,esti_method=svd_based_estim)
    #print("=================================")
    #a=recommend_proc(data2,1,similar_method=pearsonr_similarity,esti_method=svd_based_estim)
    #print(a)





