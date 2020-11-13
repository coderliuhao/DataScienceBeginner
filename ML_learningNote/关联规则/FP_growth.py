# -*- coding: utf-8 -*- 
# @Time : 2020/8/27 12:41 
# @Version: 3.6.5
# @Author : liu hao 
# @File : FP_growth.py


class TreeNode:
    def __init__(self,name_value,num_occur,parent_node):
        self.name=name_value
        self.count=num_occur
        self.node_link=None
        self.parent=parent_node
        self.children={}

    def inc(self,num_occur):
        self.count+= num_occur

    def disp(self,ind=1):
        print("  "*ind,self.name,"  ",self.count)
        for child in self.children.values():
            child.disp(ind+1)


def create_tree(data,min_sup=1):
    header_table={}

    for trans in data:
        for item in trans:
            header_table[item]=header_table.get(item,0)+data[trans]
    for k in list(header_table.keys()):
        if header_table[k] < min_sup:
            del header_table[k]
    freq_item_set=set(header_table.keys())

    if len(freq_item_set)==0:
        return None,None

    for k in header_table:
        header_table[k]=[header_table[k],None]

    res_tree=TreeNode("Null Set",1,None)

    for transet,count in data.items():
        local_d={}
        for item in transet:
            if item in freq_item_set:
                local_d[item]=header_table[item][0]
            if len(local_d)>0:
                ordered_items=[v[0] for v in sorted(local_d.items(),key=lambda p:p[1],reverse=True)]
                update_tree(ordered_items,res_tree,header_table,count)

    return res_tree,header_table

def update_tree(items,tree,header_table,count):
    if items[0] in tree.children:
        tree.children[items[0]].inc(count)
    else:
        tree.children[items[0]]=TreeNode(items[0],count,tree)
        if header_table[items[0]][1]==None:
            header_table[items[0]][1]=tree.children[items[0]]
        else:
            update_header(header_table[items[0]][1],tree.children[items[0]])
    if len(items) >1:
        update_tree(items[1::],tree.children[items[0]],header_table,count)

def update_header(node_to_test,target_node):
    while node_to_test.node_link != None:
        node_to_test=node_to_test.node_link
    node_to_test.node_link=target_node

def ascent_tree(leafnode,prefix_path):
    if leafnode.parent !=None:
        prefix_path.append(leafnode.name)
        ascent_tree(leafnode.parent,prefix_path)

def find_prefix_path(bas,tree_node):
    cond_pats={}
    while tree_node !=None:
        prefix_path=[]
        ascent_tree(tree_node,prefix_path)
        if len(prefix_path)>1:
            cond_pats[frozenset(prefix_path[1:])]=tree_node.count
        tree_node=tree_node.node_link
    return cond_pats

def mine_tree(tree,header_table,min_sup,prefix,freq_item_list):
    large_l=[v[0] for v in sorted(header_table.items(),key=lambda p:p[1][0])]
    for base_pat in large_l:
        new_freq_set=prefix.copy()
        new_freq_set.add(base_pat)

        freq_item_list.append(new_freq_set)
        cond_patt_base=find_prefix_path(base_pat,header_table[base_pat][1])
        my_cond_tree,myhead=create_tree(cond_patt_base,min_sup)

        if myhead !=None:
             mine_tree(my_cond_tree,myhead,min_sup,new_freq_set,freq_item_list)

def load_simple_data():
    simple_data= [['r', 'z', 'h', 'j', 'p'],
               ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
               ['z'],
               ['r', 'x', 'n', 'o', 's'],
               ['y', 'r', 'x', 'z', 'q', 't', 'p'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
    return simple_data


def creat_init_set(dataset):
    res_dict={}
    for trans in dataset:
        res_dict[frozenset(trans)]=1
    return res_dict

if __name__ == '__main__':
    min_sup=3
    simple_data=load_simple_data()
    inie_set=creat_init_set(simple_data)
    my_FPtree,my_headertap=create_tree(inie_set,min_sup)
    my_FPtree.disp()
    myfreqlist=[]
    mine_tree(my_FPtree,my_headertap,min_sup,set([]),myfreqlist)


