import random
from email.mime.multipart import MIMEMultipart
import smtplib
from email.mime.text import MIMEText
from email.header import Header

import jwt
from django.conf import settings


def gen_verify_code(length=4):
    all_chars = '0123456789abcdefghijklmnopqrstuvwxyz'
    return ''.join(random.choices(all_chars, k=length))


def send_email_code(content, to_user):
    # 创建 SMTP 对象
    smtp = smtplib.SMTP()
    # 连接（connect）指定服务器
    html_msg = """
    <p>Python 邮件发送HTML格式文件测试...</p>
    <p>注册验证码<a>""" + content + """</a></p>
    """

    # 创建一个带附件的实例msg
    msg = MIMEMultipart()
    msg['From'] = Header('Flying fish')  # 发送者
    msg['To'] = Header('xxx')  # 接收者
    subject = 'Python SMTP 邮件测试'
    msg['Subject'] = Header(subject, 'utf-8')  # 邮件主题
    # 邮件正文内容
    msg.attach(MIMEText(html_msg, 'html', 'utf-8'))

    # # 构造附件1，传送当前目录下的 test1.txt 文件
    # att1 = MIMEText(open('test1.txt', 'rb').read(), 'base64', 'utf-8')
    # att1["Content-Type"] = 'application/octet-stream'
    # # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
    # att1["Content-Disposition"] = 'attachment; filename="test1.txt"'
    # msg.attach(att1)
    #
    # # 构造附件2，传送当前目录下的 test2.txt 文件
    # att2 = MIMEText(open('test2.txt', 'rb').read(), 'base64', 'utf-8')
    # att2["Content-Type"] = 'application/octet-stream'
    # att2["Content-Disposition"] = 'attachment; filename="test2.txt"'
    # msg.attach(att2)
    try:
        smtp.connect("smtp.126.com", port=25)
        # 登录，需要：登录邮箱和授权码
        smtp.login(user="feiyu2023@126.com", password="WPKGEGSYJWOLGFHD")
        smtp.sendmail(from_addr="feiyu2023@126.com", to_addrs="122943384@qq.com", msg=msg.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("无法发送邮件")
    finally:
        # 关闭服务器
        smtp.quit()


# 生成验证码
def rand_code(n=0, digit=4):
    list_res = ''
    for i in range(0, digit):
        if n == 0:  # 随机输出一个数字
            list_res += str(random.randint(0, 9))
        elif n == 1:  # 随机输出一个字母
            list_res += str(chr(random.randrange(65, 90)))
        elif n == 2:
            list_res += str(chr(random.randrange(97, 122)))
    return list_res


def getUsername(request):
    auth = request.META.get('HTTP_AUTHORIZATION').split(" ")
    dict = jwt.decode(auth[1], settings.SECRET_KEY, algorithms=['HS256'])
    username = dict.get('data').get('username')
    return username
