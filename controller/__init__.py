# -*- coding: utf-8 -*-
from controller import index, admin
from flask import Flask, render_template
from config import appconfig, web_root
import os

app = Flask(__name__)
# app.default_config.update(appconfig)
app.template_folder = os.path.join(web_root, appconfig['template_folder'])
app.static_folder = os.path.join(web_root, appconfig['static_path'])
app.secret_key = appconfig['secret_key']
app.permanent_session_lifetime = 7200
app.register_blueprint(index.app)
app.register_blueprint(admin.app)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.template_filter("format_time")
def format_time(time_str):
    if time_str is None:
        return None
    return time_str.strftime("%Y-%m-%d")
