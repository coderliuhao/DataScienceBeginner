from flask import Flask,request,jsonify

app = Flask(__name__)

@app.route("/login",methods=["GET","POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    #参数判断

    if not all([username,password]):
        resp = {
            "code":1,
            "message":"invalid params"
        }
        return jsonify(resp)

    if username == "liuhao" and password == "123456":
        resp = {
            "code":0,
            "message":"login success"
        }
        return jsonify(resp)

    else:
        resp = {
            "code":2,
            "message":"login failed"
        }
        return jsonify(resp)


if __name__ == "__main__":
    app.run(debug = True)