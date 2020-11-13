#!/usr/bin/python3
# -*- coding: utf-8 -*- 
# @Time : 2020/9/3 下午5:56 
# @Author : liu hao 
# @File : json_parser.py

"""use json module to encode/decode  JSON data,include two funcs:
1 json.dumps() python form encode to JSON data
2 json.loads() decode JSON data to python form"""

"""
python  encode(dumps) to JSON

pyton           JSON

dict            object
list,tuple      array
str             string
int(float..)    number
True            true
False           false
None            null   
"""


"""
JSON  decode(loads) to python

JSON             python

object           dict
string           str
array            list
number(real)     float
number(int)      int
true             True
false            False
null             None
"""

import json
#python dict trans to JSON obj

data={"NO":1,
      "Name":"liuhao",
      "url":"www.bing.com"}

json_str=json.dumps(data)
print("data:",repr(data))
print("JSON obj:",json_str)

#JSON obj convert to dict

data_=json.loads(json_str)
print("data_['Name']:",data_["Name"])
print("data_['url']:",data_["url"])

with open("data.json","w") as f:
    json.dump(data,f)

with open("data.json","r") as f:
    data=json.load(f)
