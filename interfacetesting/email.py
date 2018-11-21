import smtplib
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText

def send_mail(self):
    mail_host = "smtp.mxhichina.com"  # 设置服务器
    mail_user = "zhuxinyi@joinpay.cn"  # 用户名
    mail_pass = "Qdv1Bji3"

    sender = 'zhuxinyi@joinpay.cn'
    receiver = 'zhuxinyi@joinpay.cn'

    message = MIMEMultipart()
    message['From'] = formataddr(["zhuxinyi", sender])
    message['To'] = formataddr(["测试", receiver])
    message['Subject'] = "邮件测试"

    message.attach(
        MIMEText('本次共测试' + str(num_total) + '个用例，' \
                                            '通过率为' + '%.2f%%' % (pass_rate * 100) + ',' \
                                                                                    '耗时' + str(
            total_time) + '秒，详细请见附件。', 'plain', 'utf-8'))

    att1 = MIMEApplication(open("testReport.xlsx", 'rb').read())
    att1.add_header('Content-Disposition', 'attachment', filename=('gbk', '', "testReport.xlsx"))
    att1["Content-Disposition"] = 'attachment; filename="test.txt"'
    message.attach(att1)

    try:
        server = smtplib.SMTP_SSL(mail_host, 465)
        server.login(mail_user, mail_pass)
        server.sendmail(sender, receiver, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")