from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate,MigrateCommand
from flask_script import Shell,Manager

app = Flask(__name__)
manager = Manager(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:liuhao123@127.0.0.1:3306/flask_test"
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)


#第一个参数是Flask的实例，第二个参数是SQLAlchemy数据库的实例
migrate = Migrate(app,db)

manager.add_command("db",MigrateCommand)

class Role(db.Model):
    __tablename__ = "roles"

    idx = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(64),unique =True)
    def __repr__(self):
        return "Role :  %s" % self.name

class User(db.Model):
    __tablename__ =  "users"

    idx = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(64),unique = True,index = True)
    def __repr__(self):
        return "User : %s" % self.name

if __name__ == "__main__":
    manager.run()
