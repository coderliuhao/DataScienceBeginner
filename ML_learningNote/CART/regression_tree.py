# -*- coding: utf-8 -*-
from numpy import *

def load_dataset(filename):
    data_matrix=[]
    fr=open(filename)
    for line in fr.readlines():
        cur_line=line.strip().split("\t")
        line_filter=map(float,cur_line)
        data_matrix.append(list(line_filter))
    return data_matrix

#数据集二分
def split_dataset(dataset,feature,value):
    sub_dataset_1=dataset[nonzero(dataset[:,feature]>value),:][0]
    sub_dataset_2=dataset[nonzero(dataset[:,feature]<=value),:][0]
    return sub_dataset_1,sub_dataset_2

#CART回归树生成叶子节点函数
def reg_leaf(dataset):
    return mean(dataset[:,-1])

#最优特征划分依据
def reg_error(dataset):
    return var(dataset[:,-1])*shape(dataset)[0]

#模型树叶子节点生成函数
def linear_solve(dataset):
    r,c=shape(dataset)
    X=mat(ones((r,c)))
    Y=mat(ones((r,1)))
    X[:,1:c]=dataset[:,0:c-1]
    Y = dataset[:, -1]
    xTx=X.T*X
    if linalg.det(xTx)==0.0:
        raise NameError("This matrix is singular ,cannot do inverse,\n\
                        try increasing the second value of ops")
    weight=xTx.I*(X.T*Y)
    return weight,X,Y

def model_leaf(dataset):
    weight,X,Y=linear_solve(dataset)
    return weight

#模型树的误差计算
def model_error(dataset):
    weight,X,Y=linear_solve(dataset)
    y_hat=X*weight
    return sum(power(Y-y_hat,2))

#核心代码：选择最佳分裂特征和阈值
def find_best_split(dataset,leaf_type=reg_leaf,err_type=reg_error,ops=(1,4)):
    tol_error_decrease=ops[0]
    min_split_samples=ops[1]
    if len(set(dataset[:,-1].T.tolist()[0]))==1:
        return None,leaf_type(dataset)
    r,c=shape(dataset)

    error=err_type(dataset)
    best_error=inf
    best_idx=0
    best_val=0
    for feat_idx in range(c-1):
        for split_val in set(dataset[:,feat_idx].T.A.tolist()[0]):
            sub_dataset1,sub_dataset2=split_dataset(dataset,feat_idx,split_val)

            if shape(sub_dataset1)[0]<min_split_samples or shape(sub_dataset2)[0]<min_split_samples:
                continue
            new_error=err_type(sub_dataset1)+err_type(sub_dataset2)
            if new_error<best_error:
                best_idx=feat_idx
                best_val=split_val
                best_error=new_error

    if (error-best_error)<tol_error_decrease:
        return None,leaf_type(dataset)
    sub_dataset1,sub_dataset2=split_dataset(dataset,best_idx,best_val)
    if shape(sub_dataset1)[0]<min_split_samples or shape(sub_dataset2)[0]<min_split_samples:
        return None,leaf_type(dataset)
    return best_idx,best_val

def create_tree(dataset,leaf_type=reg_leaf,err_type=reg_error,ops=(1,4)):
    feature,value=find_best_split(dataset,leaf_type,err_type,ops)

    if feature==None:
        return value

    reg_tree={}
    reg_tree["split_idx"]=feature
    reg_tree["split_val"]=value
    l_ds,r_ds=split_dataset(dataset,feature,value)

    #开始递归
    reg_tree["left"]=create_tree(l_ds,leaf_type,err_type,ops)
    reg_tree['right']=create_tree(r_ds,leaf_type,err_type,ops)
    return reg_tree

#判断是否为子树
def is_tree(obj):
    return (type(obj).__name__=="dict")

#递归查找两个叶子节点
def get_leaf_node(tree):
    if is_tree(tree["right"]):
        tree["right"]=get_leaf_node(tree["right"])
    if is_tree(tree["left"]):
        tree["left"]=get_leaf_node(tree["left"])
    return (tree["left"]+tree["right"])/2.0

#后剪枝操作，参数为待剪枝树，剪枝所需测试数据（一般是验证集）
def prune(tree,test_ds):
    if shape(test_ds)[0]==0:
        return get_leaf_node(tree)
    if (is_tree(tree["right"]) or is_tree(tree["left"])):
        l_ds,r_ds=split_dataset(test_ds,tree["split_idx"],tree["split_val"])
    if is_tree(tree["left"]):
        tree["left"]=prune(tree['left'],l_ds)
    if is_tree(tree["right"]):
        tree["right"]=prune(tree["right"],r_ds)

    if not is_tree(tree["left"]) and not is_tree(tree["right"]):
        l_ds,r_ds=split_dataset(test_ds,tree["split_idx"],tree["split_val"])
        full_error=sum(power(l_ds[:,-1]-tree["left"],2))+\
                     sum(power(r_ds[:,-1]-tree["right"],2))
        error_mean=(tree["right"]+tree["left"])/2.0
        error_concat=sum(power(test_ds[:,-1]-error_mean,2))
        if error_concat<full_error:
            print("Concating....")
            return error_mean
        else:
            return tree
    else:
        return tree
#回归树评估函数
def tree_eval(model,data):
    return float(model)
#模型树评估函数
def model_tree_eval(model,data):
    c=shape(data)[1]
    X=mat(ones((1,c+1)))
    X[:,1:c+1]=data
    return float(X*model)

#回归树预测
def tree_predict(tree,data,model_eval=tree_eval):
    if not is_tree(tree):
        return model_eval(tree,data)
    if data[tree["split_idx"]]>tree["split_val"]:
        if is_tree(tree["left"]):
            return tree_predict(tree["left"],data,model_eval)
        else:
            return model_eval(tree["left"],data)
    else:
        if is_tree(tree["right"]):
            return tree_predict(tree["right"],data,model_eval)
        else:
            return model_eval(tree["right"],data)

#测试数据输入入口函数
def test_predict(tree,test_ds,model_eval=tree_eval):
    r=len(test_ds)
    y_hat=mat(zeros((r,1)))
    for i in range(r):
        y_hat[i,0]=tree_predict(tree,mat(test_ds[i]),model_eval)
    return y_hat

if __name__=="__main__":
    #模型比较
    #创建回归树
    train_matrix=mat(load_dataset("bikeSpeedVsIq_train.txt"))
    test_matrix=mat(load_dataset("bikeSpeedVsIq_test.txt"))
    reg_tree=create_tree(train_matrix,ops=(1,20))
    y_hat=test_predict(reg_tree,test_matrix[:,0])
    print("CART :",corrcoef(y_hat,test_matrix[:,1],rowvar=0)[0,1])

    #创建模型树
    model_tree=create_tree(train_matrix,model_leaf,model_error,ops=(1,20))
    y_hat=test_predict(model_tree,test_matrix[:,0],model_tree_eval)
    print("Model Tree:",corrcoef(y_hat,test_matrix[:,1],rowvar=0)[0,1])

    #创建线性回归模型
    weight,X,Y=linear_solve(train_matrix)
    for i in range(shape(test_matrix)[0]):
        y_hat[i]=test_matrix[i,0]*weight[1,0]+weight[0,0]
    print("Linear model:",corrcoef(y_hat,test_matrix[:,1],rowvar=0)[0,1])



