from flask import Blueprint,render_template

users = Blueprint("user",__name__)

@users.route("/user")
def user():
    return render_template("form.html")

