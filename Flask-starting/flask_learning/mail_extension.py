from flask import Flask
from flask_mail import Mail,Message

app = Flask(__name__)

#配置邮件
app.config.update(DEBUG = True,
    MAIL_SERVER = "smtp.163.com", #smtp服务器地址
    MAIL_PORT = 25, #服务端口
    MAIL_USE_TLS = True,#传输层安全协议
    MAIL_USERNAME = "liuhao1995abc@163.com",#邮箱名
    MAIL_PASSWORD = "JUBMSUDZGUVSHKYF",#smtp授权码
    )

mail = Mail(app)
@app.route("/")
def index():
    #邮件抬头，收信人recipients列表，发信人sender
    msg = Message("来自flask mail的测试邮件",sender = "liuhao1995abc@163.com",
    recipients=["630439975@qq.com","liuhao1995@126.com","liuhao1995abc@163.com"])

    #邮件内容
    msg.body = "Flask test mail"
    mail.send(msg)
    print("Mail sent")
    return "Sent Sucessful"

if __name__ == "__main__":
    app.run()
