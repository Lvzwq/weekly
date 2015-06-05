# -*- coding: utf-8 -*-
from controller import app
from controller import *
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

app.debug = True
app.run(host='127.0.0.1', port=5000)
