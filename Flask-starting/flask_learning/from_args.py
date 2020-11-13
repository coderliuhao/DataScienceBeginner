#!/usr/bin/python3
# -*- coding: utf-8 -*- 
# @Time : 2020/11/6 下午11:30 
# @Author : liu hao 
# @File : from_args.py

from flask import Flask,request

app = Flask(__name__)

@app.route("/post",methods=["GET","POST"])
def post():
    city = request.args.get("city")
    print(request.data)
    return "hello city = %s"%(city)

if __name__ == '__main__':
    app.run(debug = True)