from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
#设置连接数据库的URI
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:liuhao123@127.0.0.1:3306/flask_test"
#设置每次请求结束后会自动提交数据库的改动
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
#查询时会显示原始SQL语句
app.config["SQLALCHEMY_ECHO"] = True


db = SQLAlchemy(app)


#定义两个模型,类似于django中的模型类，定义各个字段的类型,相当于数据库的两张表
class Role(db.Model):
    __tablename__ = "roles"

    idx = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(64),unique = True)
    users = db.relationship("User",backref = "role")
    #repr方法显示一个可读字符串
    def __repr__(self):
        return "Role : %s"% self.name

class User(db.Model):
    __tablename__ = "users"

    idx = db.Column(db.Integer,primary_key= True)
    name = db.Column(db.String(64),unique = True,index = True)
    email = db.Column(db.String(64),unique = True)
    password = db.Column(db.String(64))
    role_id = db.Column(db.Integer,db.ForeignKey("roles.idx"))

    def __repr__(self):
        return "User: %s" % self.name


if __name__ == "__main__":
    db.drop_all()#首次创建表时使用
    db.create_all()#根据模型类创建表

    role1 = Role(name = "admin")
    role2 = Role(name = "user")
    db.session.add_all([role1,role2]) #一次插入两条数据
    db.session.commit()

    user1 = User(name = "liu",email = "liu@163.com",password = "123456",role_id = role1.idx)
    user2 = User(name = "shen",email = "shen@qq.com",password = "654321",role_id = role2.idx)
    user3 = User(name = "ni",email = "ni@126.com",password = "123789",role_id = role2.idx)
    user4 = User(name = "wei",email = "wei@163.com",password = "666666",role_id = role1.idx)
    db.session.add_all([user1,user2,user3,user4])
    db.session.commit()

     
    user = User.query.first()
    user.name = "liuhao"
    db.session.commit()
    user.query.first()

    app.run(debug = True)
   