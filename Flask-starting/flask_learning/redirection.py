#!/usr/bin/python3
# -*- coding: utf-8 -*- 
# @Time : 2020/11/4 下午11:49 
# @Author : liu hao 
# @File : redirection.py

from flask import Flask,redirect,url_for

app = Flask(__name__)

@app.route('/hello')
def hello_world():
    return "hello world"


@app.route("/login")
def login():
   # url = "/hello"
    url = url_for('hello_world')
    return redirect(url)

if __name__ == '__main__':
    app.run(debug = True)