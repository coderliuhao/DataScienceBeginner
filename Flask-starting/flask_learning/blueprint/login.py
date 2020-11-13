from flask import Blueprint,render_template

#创建首页
logins = Blueprint("login",__name__)

@logins.route("/login")
def login():
    return render_template("login.html")