import unittest
from unittest_case import app

import json


class LoginTest(unittest.TestCase):

    #构造单元测试

    def setUP(self):
        #开启flask的测试模式
        app.testing = True


    def test_user_isempty(self):
        #测试用户和密码是否完整

        #创建web请求客户端,由flask提供
        client = app.test_client()
        #利用client客户端模拟发送请求
        resp  = client.post("/login",data={})#用户名密码都为空

        #resp是视图返回的响应对象，data属性是响应体数据
        resp_data = resp.data
        #解析json,把json转换成python字典
        resp_data = json.loads(resp_data)

        #断言
        self.assertIn("code",resp_data)
        self.assertEqual(resp_data["code"],1)

    def test_user_pass_isright(self):
        client = app.test_client()
        resp = client.post("/login",data={"username":"liuhao","password":"123789"})
        resp_data = resp.data
        resp_data = json.loads(resp_data)

        #断言
        self.assertIn("code",resp_data)
        self.assertEqual(resp_data["code"],2)


    def test_user_pass_isallright(self):
        client = app.test_client()
        resp = client.post("/login",data={"username":"liuhao","password" : "123456"})
        
        resp_data = json.loads(resp.data)
        
        #断言
        self.assertIn("code",resp_data)
        self.assertEqual(resp_data["code"],0)


if __name__ == "__main__":
    unittest.main()

