from flask import Flask

app = Flask()

@app.route("/")
def index():
    return "index"

@app.route("/list")
def list1():
    return "list1"

@app.route("/detail")
def detail():
    return detail

@app.route("/")
def admin_home():
    return "admin home"

@app.route("/new"):
def new():
    return new

@app.route("/edit")
def edit():
    return "edit"

