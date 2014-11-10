# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from model import init_db, close_session, get_all_paper, get_article_list

app = Flask(__name__)


@app.route('/')
def index():
    sess = init_db()
    paper_list = get_all_paper(sess)
    for i in paper_list:
        print i
    close_session(sess)
    #return 'hello world'
    return render_template("index.html")




if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001)
