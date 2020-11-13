#!/usr/bin/python3
# -*- coding: utf-8 -*- 
# @Time : 2020/11/5 上午12:12 
# @Author : liu hao 
# @File : usage_transformer.py

from flask import Flask

app = Flask(__name__)

@app.route('/goods/<goods_id>')
#@app.route('/goods/<int:goods_id>')
def goods(goods_id):
    return 'goods_id : %s' % goods_id


if __name__ == "__main__":
    app.run(debug = True)