#!/usr/bin/python3
# -*- coding: utf-8 -*- 
# @Time : 2020/11/6 下午11:07 
# @Author : liu hao 
# @File : get_form.py

from flask import Flask,request

app = Flask(__name__)

@app.route("/postt",methods = ["GET","POST"])
def postt():
    name = request.form.get("name")
    age = request.form.get("age")
    return "hello name = %s  age=%s"%(name,age)

if __name__ == '__main__':
    app.run(debug = True)