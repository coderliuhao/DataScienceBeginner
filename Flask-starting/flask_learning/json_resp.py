from flask import Flask,jsonify
import json

app = Flask(__name__)
@app.route("/index")
def index():
    data = {
        "name":"liuhao",
        "age":25
    }
    return jsonify(data) 
#把字典转成json格式，把响应头中的Content-Type设置为application/json

if __name__ == "__main__":
    app.run(debug = True)