#! /usr/bin/env python3
# -*- coding: UTF-8 -*-
import datetime
import logging
import smtplib
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dataCollecter.store import *

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s [dataCollector.mailSender][line:%(lineno)d] %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='mailSender.log',
                    filemode='a')
logging.info('aaaa')
head = '<html>\n<body>\n'
tail = '</body>\n</html>'
tag_a = '<a href=\"%s\">%s</a>\n<br/>\n'

json = list(Email.find())
datas = list(lastest_data.find())
print(str(json))
context = ''
for data in datas:
    context += tag_a % (data['url'], '[' + data['spider'] + '] ' +
                        '[' + data['date'] + '] ' + data['title'])
context = head + context + tail
mailto_list = [i['address'] for i in json]  # 收件人(列表)
# mailto_list.append("scau_DCS@163.com")
# mailto_list.reverse()
mail_host = "smtp.163.com"  # 使用的邮箱的smtp服务器地址，这里是163的smtp地址
mail_user = "scau_DCS@163.com"  # 用户名
mail_pass = "dcs123456"  # 密码
mail_postfix = "163.com"  # 邮箱的后缀，网易就是163.com


def send_mail(to_list, sub, context):
    me = "DataCollectionSystem" + "<" + mail_user + "@" + mail_postfix + ">"
    msg = MIMEMultipart('alternative')
    msg['Subject'] = Header(sub, 'utf-8')
    html = MIMEText(context, 'html', 'utf-8')
    msg.attach(html)
    msg['From'] = me
    msg['To'] = ";".join(to_list)  # 将收件人列表以‘；’分隔
    server = smtplib.SMTP(host=mail_host,port=25)
    server.login(mail_user, mail_pass)  # 登录操作
    server.sendmail(me, to_list, msg.as_string())
    server.close()
    return True


if True:
    for i in range(1):  # 发送1封，上面的列表是几个人，这个就填几
        if send_mail(mailto_list, str(datetime.date.today()) + "更新列表", context):  # 邮件主题和邮件内容
            # 这是最好写点中文，如果随便写，可能会被网易当做垃圾邮件退信
            lastest_data.drop()
            print("done!")
        else:
            print("failed!")
else:
    print('no new data')
