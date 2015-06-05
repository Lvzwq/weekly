#!/usr/bin/python
# coding:utf-8
from ConfigParser import ConfigParser
import os

web_root = os.path.abspath(".")
config_path = os.path.join(web_root, "config")
cp = ConfigParser()
cp.read(os.path.join(config_path, "db.conf"))
mysql = dict(cp.items("mysql_db"))

cp.read(os.path.join(config_path, "app.conf"))
appconfig = dict(web_root=web_root, config_path=config_path)
appconfig.update(dict(cp.items("app")))
