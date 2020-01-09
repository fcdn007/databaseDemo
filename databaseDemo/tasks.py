#!usr/bin/env python
# -*- coding:utf-8 -*-
from celery import task
from django.conf import settings
from django.core.mail import send_mail

from .settings import SERVER_HOST


@task
def send_register_active_email(to_email, username, token):
    """发送激活邮件"""
    # 组织邮件信息
    subject = '甲基化早筛项目数据库管理系统Demo'
    message = ''
    sender = settings.EMAIL_PROM  # 发送人
    receiver = [to_email]
    html_message = '<h1>%s, 欢迎您成为甲基化早筛项目数据库管理系统Demo注册成员</h1>请点击下面链接激活您的账户<br/>' \
                   '<a href="http://%s:8000/active/%s">http://%s:8000/active/%s</a>' % \
                   (SERVER_HOST, SERVER_HOST, username, token, token)

    send_mail(subject, message, sender, receiver, html_message=html_message)
    return True
    # time.sleep(5)
