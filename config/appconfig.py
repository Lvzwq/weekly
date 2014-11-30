# -*- coding: utf-8 -*-

class Config(object):
    SECRET_KEY = 'hello world bingyan'
    HOST = 'http://images.hustnews.com'
    PAPER_LIMIT = 20
    ALLOWED_MIMETYPES = {'image/jpeg', 'image/png', 'image/gif', 'image/bmp', 'image/jpg'}
    UPLOAD_FOLDER = 'static/upload'
    ADMIN_USER = 'hustnews'
    ADMIN_PWD = '87542701'
    TEMPLATE_FOLDER = '../templates'
    STATIC_PATH = '../static'
    UPLOAD_FOLDER = 'static/upload'