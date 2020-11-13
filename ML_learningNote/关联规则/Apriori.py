# -*- coding: utf-8 -*- 
# @Time : 2020/8/26 23:22 
# @Version: 3.6.5
# @Author : liu hao 
# @File : Apriori.py


from numpy import *

def load_data():
    return [[1,3,4],[2,3,5],[1,2,3,5],[2,5]]

def creat_c1(dataset):
    c1=[]
    for transaction in dataset:
        for item in transaction:
            if not  [item] in c1:
                c1.append([item])

    c1.sort()
    return list(map(frozenset,c1))

def scan_data(data,ck,min_support):
    ss_cnt={}
    for tid in data:
        for can in ck:
            if can.issubset(tid):
                if not can in ss_cnt:

                    ss_cnt[can]=1
                else:
                    ss_cnt[can]+=1
    num_items=float(len(data))
    res_list=[]
    support_data={}
    for key in ss_cnt:
        support=ss_cnt[key]/num_items
        if support>=min_support:
            res_list.insert(0,key)
        support_data[key]=support
    return res_list,support_data


"""频繁项集，项集元素个数k"""
def apriori_generator(fs,k):
    res_list=[]
    len_fs=len(fs)
    for i in range(len_fs):
        for j in range(i+1,len_fs):
            f1=list(fs[i])[:k-2]
            f2=list(fs[j])[:k-2]
            f1.sort()
            f2.sort()
            if f1==f2:
                res_list.append(fs[i]|fs[j])
    return res_list

"""核心程序"""
def apriori(data,min_support=0.5):
    c1=creat_c1(data)
    d=list(map(set,data))
    f1,support_data=scan_data(d,c1,min_support)
    fs=[f1]
    k=2
    while len(fs[k-2])>0:
        ck=apriori_generator(fs[k-2],k)
        fk,supk=scan_data(d,ck,min_support)
        support_data.update(supk)
        fs.append(fk)
        k+=1

    return fs,support_data


"""关联规则生成"""
def rule_generator(fs,suppport_data,min_conf=0.7):
    strong_rule_list=[]

    for i in range(1,len(fs)):
        for freq_set in fs[i]:
            h1=[frozenset([item]) for item in freq_set]
            if i>1:
                rules_from_conseq(freq_set,h1,suppport_data,strong_rule_list,min_conf)
            else:
                cal_conf(freq_set,h1,suppport_data,strong_rule_list,min_conf)
    return strong_rule_list


"""计算可信度"""
def cal_conf(freq_set,h,support_data,brl,min_conf=0.7):

    prune_conf=[]
    for conseq in h:
        conf=support_data[freq_set]/support_data[freq_set-conseq]
        if conf>=min_conf:
            print(freq_set-conseq,"-->",conseq,"conf:",conf)
            brl.append((freq_set-conseq,conseq,conf))
            prune_conf.append(conseq)
    return prune_conf


def rules_from_conseq(freq_set,h,support_data,brl,min_conf=0.7):
    m=len(h[0])
    if len(freq_set)>(m+1) :
        hmp1=apriori_generator(h,m+1)
        hmp1=cal_conf(freq_set,hmp1,support_data,brl,min_conf)

        if len(hmp1)>1:
            rules_from_conseq(freq_set,hmp1,support_data,brl,min_conf)

def print_rules(rule_list,item_mean):
    for rule in rule_list:
        for item in rule[0]:
            print(item_mean[item])
        print("          -------->")
        for item in rule[1]:
            print(item_mean[item])
        print("confidences :%f"%rule[2])

if __name__ == '__main__':
    dataset=load_data()
    fs,support_data=apriori(dataset)
    print("频繁项集 ：",fs,"\n支持度",support_data)


    rules=rule_generator(fs,support_data,min_conf=0.5)
    print("关联规则为:",rules)