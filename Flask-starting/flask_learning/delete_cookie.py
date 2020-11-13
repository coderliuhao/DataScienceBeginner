from flask import Flask,make_response

app = Flask(__name__)

@app.route("/del_cookie")
def deleting_cookie():
    resp = make_response("del success!")
    resp.delete_cookie("name")
    return resp

if __name__ == "__main__":
    app.run(debug = True)