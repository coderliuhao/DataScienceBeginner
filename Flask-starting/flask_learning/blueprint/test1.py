from flask import Flask
from user import users
from login import logins

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "hello world"


#注册蓝图
app.register_blueprint(logins,url_prefix = "")
app.register_blueprint(users,url_prefix = "")


if __name__ == "__main__":
    app.run(debug = True)