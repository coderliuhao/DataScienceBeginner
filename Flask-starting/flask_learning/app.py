from flask import Flask
#import config

app = Flask(__name__)#__name__当前模块的名字
#app.debug = True
app.config.update(DEBUG = True)
#app.config.from_object(config)
#app.config.from_pyfile('config.py')
@app.route('/1')
@app.route('/2')#装饰器，绑定视图函数路径
#@app.route('/post',methods = ['post'])
#@app.route('/',methods = ['POST'])
def hello_world1(): #视图函数
    return 'Hello World 1'

#@app.route('/')
# @app.route('/',methods = ['GET'])
# def Hello_world2():
# 	return "Hello world 2"
#
# @app.route('/')
# def Hello_world3():
# 	return "Hello world 3"

if __name__ == '__main__':
    print(app.url_map) #打印整个flask的路由信息
    #app.run(debug = True)#运行本地服务器测试flask程序
    app.run()