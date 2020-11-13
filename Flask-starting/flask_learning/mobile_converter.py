#!/usr/bin/python3
# -*- coding: utf-8 -*- 
# @Time : 2020/11/5 下午11:20 
# @Author : liu hao 
# @File : mobile_converter.py

from flask import Flask,redirect,url_for
from werkzeug.routing import BaseConverter

app = Flask(__name__)
# 为方便理解，直接创建电话号码转换器
class MobileConverter(BaseConverter):
    def __init__(self, url_map):
        super(MobileConverter, self).__init__(url_map)
        self.regex = r'1[345678]\d{9}'

    def to_python(self,value):
#        return value
        return "123456"


    def to_url(self, value):
        return "654321"

app.url_map.converters["mobile"] = MobileConverter


@app.route("/send/<mobile:mobile_num>")
def send_sms(mobile_num):
    return "send_sms : %s" % mobile_num

@app.route("/index")
def index():
    url = url_for("send_sms",mobile_num="13456789012")
    return redirect(url)

if __name__ == "__main__":
    app.run(debug = True)