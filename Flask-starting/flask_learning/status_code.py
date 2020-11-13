from flask import Flask,abort,Response

app = Flask(__name__)

@app.route("/login")
def login():
    #传递http标准状态码信息
    name = ""
    pwd = ""

    if name != "liuhao" and pwd != "123456":
        resp = Response("login failed")
        abort(resp)
    
    return "login success"

if __name__ == "__main__":
    app.run(debug = True)