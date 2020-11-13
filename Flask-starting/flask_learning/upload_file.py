#!/usr/bin/python3
# -*- coding: utf-8 -*- 
# @Time : 2020/11/6 下午10:20 
# @Author : liu hao 
# @File : upload_file.py

from flask import Flask,request

app = Flask(__name__)

@app.route("/upload",methods=["GET","POST"])
def upload():
    f = request.files.get("pic")
    if f is None:
        return "No files uploaded"

    f1 = open("/home/liuhao/Pictures/girl.jpg","wb")

    data = f.read()
    f1.write(data)
    f1.close()

    return "Upload successfully"

if __name__ == '__main__':
    app.run(debug = True)