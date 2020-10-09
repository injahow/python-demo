#!/usr/bin/python
# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
 
my_sender = '***@**.com'
my_pass = '***'
my_user = '***@**.com'


def mail(message):
    ret = True
    try:
        msg = MIMEText(message, 'plain', 'utf-8')
        msg['From'] = formataddr(['noreply', my_sender])
        msg['To'] = formataddr(['someone', my_user])
        msg['Subject'] = '***'

        server = smtplib.SMTP_SSL('smtp.qq.com', 465)
        server.login(my_sender, my_pass)
        server.sendmail(my_sender, [my_user,], msg.as_string())
        server.quit()
    except Exception:
        ret = False
    return ret

message = 'message'
ret=mail(message)

if ret:
    print('邮件发送成功')
else:
    print('邮件发送失败')