# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from model import Model
from datetime import datetime
from util import  format_week
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

app = Flask(__name__)


@app.route('/')
def index():
    model = Model()
    paper_list = model.get_all_paper()
    max_paper = model.get_max_paper()
    article_list = model.get_article_list(273)
    model.close_session()
    paper = []
    for p in paper_list:
        time = p.time.strftime('%Y年%m月%d日')
        paper.append({'id': p.id, 'num': p.num, 'time': time})
    data = {'now': datetime.now().strftime('%Y年%m月%d日')}
    week = datetime.now().isoweekday()
    data['week'] = format_week(week)

    print week
    return render_template("index.html", max_paper=max_paper, article_list=article_list, paper_list=paper, data=data)


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5000)
