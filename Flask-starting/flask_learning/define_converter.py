#!/usr/bin/python3
# -*- coding: utf-8 -*- 
# @Time : 2020/11/5 上午12:45 
# @Author : liu hao 
# @File : define_converter.py

from flask import Flask
from werkzeug.routing import BaseConverter

app = Flask(__name__)


class RegexConverter(BaseConverter):
    def __init__(self, url_map, regex):
        super(RegexConverter, self).__init__(url_map)  # 调用父类初始化方法
        self.regex = regex


app.url_map.converters["re"] = RegexConverter  # 将自定义的转换器添加到flask应用中


@app.route("/send/<re(r'1[345678]\d{9}'):mobile>")
def send_sms(mobile):
    return "send_sms : %s" % mobile


if __name__ == "__main__":
    app.run(debug=True)