from flask import Flask,make_response

app = Flask(__name__)

@app.route("/set_cookie")
def setting_cookie():
    resp = make_response("success")
    resp.set_cookie("name","liuhao",max_age = 3600)
    resp.set_cookie("age","25")
    return resp

if __name__ == "__main__":
    app.run(debug = True)