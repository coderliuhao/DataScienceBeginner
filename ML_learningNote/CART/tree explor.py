# -*- coding: utf-8 -*- 
# @Time : 2020/8/12 16:55 
# @Author : liu hao 
# @File : tree explor.py

from tkinter import *
from numpy import *
from CART import regression_tree

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def re_draw(tol_error_decrease,min_split_samples):
    re_draw.f.clf()
    re_draw.a=re_draw.f.add_subplot(111)
    if check_button_var.get():
        if min_split_samples<2:
            min_split_samples=2
        tree=regression_tree.create_tree(re_draw.rawdata,regression_tree.model_leaf,\
                                         regression_tree.model_error,(tol_error_decrease,min_split_samples))
        y_hat=regression_tree.test_predict(tree,re_draw.test_data,\
                                           regression_tree.model_tree_eval)
    else:
        tree=regression_tree.create_tree(re_draw.rawdata,ops=(tol_error_decrease,min_split_samples))
        y_hat=regression_tree.test_predict(tree,re_draw.test_data)
    re_draw.a.scatter(re_draw.rawdata[:,0].tolist(),re_draw.rawdata[:,1].tolist(),s=5)
    re_draw.a.plot(re_draw.test_data,y_hat,linewidth=2.0)
    re_draw.canvas.draw()

def get_input():
    try:
        min_split_samples=int(tol_Nentry.get())
    except:
        min_split_samples=10
        print("Enter integer for tol_N")
        tol_Nentry.delete(0,END)
        tol_Nentry.insert(0,"10")
    try:
        tol_error_decrease=float(min_SS.get())
    except:
        tol_error_decrease = 1.0
        print("Enetr float for tol_ed")
        min_SS.delete(0,END)
        min_SS.insert(0,"1.0")
    return min_split_samples,tol_error_decrease

def draw_new_tree():
    min_split_samples,tol_error_decrease=get_input()
    re_draw(tol_error_decrease,min_split_samples)
if __name__=="__main__":
    root = Tk()
    re_draw.f = Figure(figsize=(5, 4), dpi=100)
    re_draw.canvas = FigureCanvasTkAgg(re_draw.f, master=root)
    re_draw.canvas.draw()
    re_draw.canvas.get_tk_widget().grid(row=0, columnspan=3)

    Label(root, text="min_split_samples").grid(row=1, column=0)
    tol_Nentry = Entry(root)
    tol_Nentry.grid(row=1, column=1)
    tol_Nentry.insert(0, "10")

    Label(root,text="tol_error_decrease").grid(row=2,column=0)
    min_SS = Entry(root)
    min_SS.grid(row=2, column=1)
    min_SS.insert(0, "1.0")


    Button(root,text="re draw",command=draw_new_tree).grid(row=1,column=2,rowspan=3)

    check_button_var=IntVar()
    check_button=Checkbutton(root,text="Model Tree",variable=check_button_var)
    check_button.grid(row=3,column=0,columnspan=2)

    re_draw.rawdata=mat(regression_tree.load_dataset("sine.txt"))
    re_draw.test_data=arange(min(re_draw.rawdata[:,0]),\
                             max(re_draw.rawdata[:,0]),0.01)
    re_draw(1.0,10)
    root.mainloop()



