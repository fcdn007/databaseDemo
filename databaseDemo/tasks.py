#!usr/bin/env python
# -*- coding:utf-8 -*-
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from .celerys import app
from .settings import SERVER_HOST
from .utils import make_new_merge_df, check_new_merge_df


@app.task
def send_register_active_email(to_email, username, token):
    """发送激活邮件"""
    # 组织邮件信息
    subject = '甲基化早筛项目数据库管理系统Demo'
    message = ''
    sender = settings.EMAIL_PROM  # 发送人
    receiver = [to_email]
    html_message = '<h1>%s, 欢迎您成为甲基化早筛项目数据库管理系统Demo注册成员</h1>请点击下面链接激活您的账户<br/>' \
                   '<a href="http://%s:8000/active/%s">http://%s:8000/active/%s</a>' % \
                   (username, SERVER_HOST, token, SERVER_HOST, token)

    send_mail(subject, message, sender, receiver, html_message=html_message)
    return True
    # time.sleep(5)


@app.task
def make_new_merge_df_by_celery(json_files_tmp, time2):
    make_new_merge_df(json_files_tmp, time2)
    return True


@shared_task
def keep_merge_df_newest_by_celery():
    flag_update, json_files, time2, _ = check_new_merge_df()
    if flag_update:
        make_new_merge_df(json_files, time2)
    return True
