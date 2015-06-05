#!/usr/bin/python
# coding:utf-8
from flask import redirect, url_for
from flask import session
from config import appconfig
from functools import wraps
import hashlib


def md5(text):
    if text is not None:
        return hashlib.md5(text).hexdigest()
    return hashlib.md5("").hexdigest()


def login_required(func):
    @wraps(func)
    def _login_required(*args, **kwargs):
        if is_login():
            return func(*args, **kwargs)
        else:
            return redirect(url_for("admin.login"))
    return _login_required


def is_login():
    if not session.get('uid') or not session.get('logged'):
        return False
    else:
        uid = session.get('uid')
        logged = session.get('logged')
        if uid == md5(appconfig['admin_user']) and logged == 1:
            return True
        else:
            return False


def destroy_session():
    session.clear()


def do_signin(username, password):
    if username != '' and username == appconfig['admin_user']:
        if password != '' and password == appconfig['admin_password']:
            return dict(status=True, msg='登录成功')
        else:
            return dict(status=False, msg="密码错误")
    else:
        return dict(status=False, msg='用户名错误')


def set_login(username):
    session.permanent = True
    session['uid'] = md5(username)
    session['logged'] = 1
