使用STMP服务发送邮件:

1、在邮箱官网登录账号，进入邮箱设置，开启STMP服务，获取模拟登陆的授权码(password)。

2、导入必要的依赖：import smtplib
                                     from email.mime.text import MIMEText
                                     from email.header import Header
                                     from email.utils import formataddr
                                     from email.mime.multipart import MIMEMultipart
                                     from email.mime.application import MIMEApplication

​     smtplib是关于smtp服务的库

​     MIMEText,构建邮件具体内容，格式，编码

​     Header和formataddr：完善标准smtp协议的邮件格式，包含三个部分：From、To、Subject.

​                                               分别对应了发送者邮箱，接受者邮箱以及邮件主题。

​    Header()中主要包含上述某一部分的具体内容和对应编码 。

​    formataddr():主要用来构建From,和To这两部分的信息.参数为列表形式，每个列表中包含两个

​    信息：  发送者/接受者的昵称，发送者/接受者的邮箱账户。举例：`msg["From"]=formataddr(["from_name",from_emai])`

 3、完成必要的信息组件之后，使用smtp.SMTP_SSL()生成服务器对象，括号中填写发送者邮箱的SMTP服务地址，一般为smtp.邮箱域名.com

4、使用发送者邮箱的账户和授权码模拟登陆邮箱，server.login(account,password)

5、服务器对象的sendmail方法用来发送邮件，传入参数有server.sendmail(from,[to,],msg.as_string())

6、server.quit()退出服务

7、将上述2,3,4,5步封装在函数中，添加标志位配合try...except Exception...语句异常处理，判断是否成  功发送邮件。







