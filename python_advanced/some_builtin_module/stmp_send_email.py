
#创建SMTP对象：smtp_obj=smtplib.SMTP([host[,port[,local_hostname]]])
#host:SMTP服务器主机，可以指定主机的ip地址或者域名，是可选参数
#port:如果提供了host参数，需要指定SMTP服务器使用的端口号，一般情况下SMTP的端口号为25
#local_hostname:如果SMTP在本机上，只需要指定服务器地址为localhost即可
#python SMTP使用sendmail方法发送邮件：
# SMTP.sendmail(from_add,to_add,msg[,msg_options,rcpt_options])
"""参数分别为：发送者地址，发送的目标地址，发送的信息。其中，msg是字符串，表示邮件，邮件包含：标题、发信人、收件人、邮件内容、附件等等，发送时需要注意msg格式。该格式就是smtp协议中定义的格式"""
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

#ygisamlmrxlebfjd

#XDJGPERLTDZCJGQP


sender="liuhao1995@126.com"  
password="XDJGPERLTDZCJGQP"
reciever="630439975@qq.com"

reciever1="liuhao1995@126.com"  
password1="ygisamlmrxlebfjd"
sender1="630439975@qq.com"

def mail():
    ret=True
    try:
        msg=MIMEText("python SMTP发送邮件","plain","utf-8")
        msg["From"]=formataddr(["From@刘浩126",sender])
        msg["To"]=formataddr(["刘浩qq",reciever])
        msg["Subject"]="从126邮箱向QQ邮箱发送邮件测试"
        server=smtplib.SMTP_SSL("smtp.126.com",)
        server.login(sender,password)
        server.sendmail(sender,[reciever,],msg.as_string())
        server.quit()
    except:
        ret=False
    return ret

def mail1():
    ret=True
    try:
        msg=MIMEText("python SMTP发送邮件","plain","utf-8")
        msg["From"]=formataddr(["From@刘浩qq",sender1])
        msg["To"]=formataddr(["刘浩126",reciever1])
        msg["Subject"]="从qq邮箱向126邮箱发送邮件测试"
        server=smtplib.SMTP_SSL("smtp.qq.com",)
        server.login(sender1,password1)
        server.sendmail(sender1,[reciever1,],msg.as_string())
        server.quit()
    except:
        ret=False
    return ret

def html_type_email():
    ret=True
    try:
        email_msg = """<h1>126发往qq的测试文件...</h1>,
         <p>python测试...</p>"""
        msg=MIMEText(email_msg,"html","utf-8")
        msg["From"]=formataddr(["来自126",sender])
        msg["To"]=formataddr(["to_qq",reciever])
        subject="126发往qq的测试邮件"
        msg["Subject"]=Header(subject,"utf-8")

        # 登录邮箱发送邮件
        server=smtplib.SMTP_SSL("smtp.126.com")
        server.login(sender,password)
        server.sendmail(sender,[reciever,],msg.as_string())
        server.quit()
    
    except Exception:
        ret=False
    return ret

def email_with_attach():
    ret=True
    try:
        msg=MIMEMultipart()
        msg["From"]=Header("126发邮件","utf-8")
        msg["To"]=Header("qq收件","utf-8")
        subject="126发往qq的测试邮件"
        msg["Subject"]=Header(subject,"utf-8")
        
        msg.attach(MIMEText("python smtp 邮件带附件测试","plain","utf-8"))
        
        att_file="uu.txt"
        txtfile=MIMEApplication(open(att_file,"rb").read())
        txtfile.add_header('Content-Disposition','attachment',filename=att_file)
        msg.attach(txtfile)
        
        pfile = '推荐指南.pdf'
        pdffile = MIMEApplication(open(pfile,'rb').read())
        pdffile.add_header('Content-Disposition','attachment',filename=pfile)
        msg.attach(pdffile)
        
        server=smtplib.SMTP("smtp.126.com")
        server.login(sender,password)
        server.sendmail(sender,reciever,msg.as_string())
        server.quit()
    except Exception:
        ret=False
    return ret
        
    


    

if __name__=="__main__":
    #ret=mail()
    #ret=mail1()
    #ret=html_type_email()
    ret=email_with_attach()
    if ret:
        print("邮件发送成功")
    else:
        print("邮件发送失败")

