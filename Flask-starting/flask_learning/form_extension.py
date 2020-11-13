from flask import Flask,render_template,redirect,url_for,session,request,flash

from flask_wtf import FlaskForm #导入wtf扩展的表单类

#导入自定义表单需要的字段
from wtforms import SubmitField,StringField,PasswordField

#导入wtf扩展提供的表单验证器
from wtforms.validators import DataRequired,EqualTo
app = Flask(__name__)
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        print(username,password)
        return "Success"
    else:
        return render_template("login.html")


app.config["SECRET_KEY"] = "123"

#创建自定义表单类，文本字段，密码字段，提交按钮

class Login(FlaskForm):
    username = StringField(label=u"用户",validators = [DataRequired()])
    password = PasswordField(label=u"密码",validators=[DataRequired(),EqualTo("password1","err")])
    password1 = PasswordField(label = u"确认密码",validators = [DataRequired()])
    submit = SubmitField(u"提交")


#定义根路由视图函数，生成表单对象，获取表单数据，进行表单数据验证

@app.route("/",methods = ["GET","POST"])
def index():
    #初始化登录的表单对象
    form = Login()
    if form.validate_on_submit():
        #调用login中的属性获取数据
        name = form.username.data
        pw = form.password.data
        pw1 = form.password1.data
        print(name,pw,pw1)
        #重定向到login的装饰器
        return redirect(url_for("login"))
    else:
        if request.method == "POST":
            flash(u"信息有误，请重新输入 ：")
    
    return render_template('index.html',form = form)

if __name__ == "__main__":
    app.run(debug = True)