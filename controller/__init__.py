# -*- coding: utf-8 -*-
from flask import Flask
from config.appconfig import Config
from flask import session
import hashlib
import json


app = Flask(__name__)
app.config.from_object(Config)
app.template_folder = app.config['TEMPLATE_FOLDER']
app.static_folder = app.config['STATIC_PATH']
__all__ = ['index', 'admin']


def is_login():
    if not session.get('uid') or not session.get('logged'):
        return False
    else:
        uid = session.get('uid')
        logged = session.get('logged')
        if uid == hashlib.md5(app.config['ADMIN_USER']).hexdigest() and logged == 1:
            return True
        else:
            return False


def do_signin(username, password):
    if username != '' and username == app.config['ADMIN_USER']:
        if password != '' and password == app.config['ADMIN_PWD']:
            return json.dumps({'status': True, 'msg': '登录成功'})
        else:
            return json.dumps({'status': False, 'msg': '密码错误'})
    else:
        return json.dumps({'status': False, 'msg': '用户名错误!'})


def check_param(param):
    # 初始化
    paper_num = param.get('paper_num')
    pid = param.get('pid')
    limit = app.config['PAPER_LIMIT']
    prev = 1
    next = 2
    current_id = 1
    if not paper_num or not paper_num.isdigit():
        paper_num = None
    if param.get('limit') and param.get('limit').isdigit():
        limit = param.get('limit')
    if pid and pid.isdigit():
        current_id = int(pid)
        prev = current_id - 1
        next = current_id + 1
    return {'prev': prev, 'next': next, 'current_id': current_id, 'limit': limit, 'paper_num': paper_num}







