from flask import Flask,session

app = Flask(__name__)

app.config["SECRET_KEY"] = "123DFHJKJFGKJNGmvbshd"

@app.route("/login")
def login():
    session["name"] = "liuhao"
    session["phone"] = "13344445555"
    return "login success"

@app.route("/index")
def index():
    name = session.get("name")
    phone = session.get("phone")
    return "hello  %s ,phone: %s"%(name,phone)

if __name__ == "__main__":
    app.run(debug = True)