from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "hello world"

#第一次请求之前执行
#连接数据库操作
@app.before_first_request
def before_first_request():
    print("before first request")


#每次请求都会执行
#权限校验
@app.before_request
def before_request():
    print("before request")


#请求之后运行
@app.after_request
def after_request(response):
    #response是前面请求处理完毕之后，返回的响应数据
    #如需对响应额外处理，可以在这里编写处理逻辑
    #json.dumps配置请求钩子
    #response.headers["Content_Type"] = "application/json"
    print("after requets")
    return response


#每次请求之后调用,传入错误信息
@app.teardown_request
def teardown_request(err_msg):
    #数据库扩展，可以实现自动提交数据库
    print("teardown request: error %s" % err_msg)





if __name__ == "__main__":
    app.run()
