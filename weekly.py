# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from model import Model
from datetime import datetime
from util import format_week
from config.appconfig import HOST
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

app = Flask(__name__)


@app.route('/')
@app.route('/paper/<int:paper_id>')
@app.route('/page/<int:page_id>')
def index(paper_id=None, page_id=None):
    model = Model()
    paper_list = model.get_all_paper()
    max_paper = model.get_max_paper()
    article_list = model.get_article_list(273)

    if paper_id == None and page_id == None:
        paper_id = max_paper.id
        pic_info = model.get_pic_info(paper_id)
        page_id = pic_info.id
    elif paper_id != None:
        pic_info = model.get_pic_info(paper_id)
        page_id = pic_info.id
    else:
        pic_info = model.get_page_info(page_id)
    area_list = model.get_area_list(page_id)
    model.close_session()

    paper = []
    # 格式化日期时间
    for p in paper_list:
        time = p.time.strftime('%Y年%m月%d日')
        paper.append({'id': p.id, 'num': p.num, 'time': time})
    data = {'now': datetime.now().strftime('%Y年%m月%d日')}
    week = datetime.now().isoweekday()
    data['week'] = format_week(week)
    # 格式化大图片链接
    data['pic_url'] = HOST + "/Newspaper/paper" + pic_info.pic_url[3:]

    for i in range(len(area_list)):
        y = str(area_list[i].y)[:-2]
        height = str(area_list[i].height)[:-2]
        title_y = int(y) + int(height) + 7
        area_list[i].title_y = str(title_y) + 'px'
        area_list[i].article_title = model.get_article_info(area_list[i].article_id).title
    return render_template("paper_index.html", max_paper=max_paper.num, article_list=article_list, paper_list=paper,
                           data=data, area_list=area_list)


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5000)
