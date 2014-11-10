# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
import mysql
app = Flask(__name__)


@app.route('/')
def index():
    sess = mysql.init_db()
    paper_list = mysql.get_all_paper(sess)
    for i in paper_list:
        print i
    mysql.close_session(sess)


    return render_template("index.html")



if __name__ == '__main__':
    app.run(host = '127.0.0.1', port = 8082)
