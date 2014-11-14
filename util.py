# -*- coding: utf-8 -*-
from config.appconfig import ADMIN_USER, ADMIN_PWD
import json


def format_week(week):
    weekly = ['日', '一', '二', '三', '四', '五', '六', '日']
    return weekly[week]


def check_login(username, password):
    if username != '' and username == ADMIN_USER:
        if password != '' and password == ADMIN_PWD:
            return json.dumps({'status': True, 'msg': '登录成功'})
        else:
            return json.dumps({'status': False, 'msg': '密码错误'})
    else:
        return json.dumps({'status': False, 'msg': '用户名错误!'})

def check_param(params):
    pass









