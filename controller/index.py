# -*- coding: utf-8 -*-
from datetime import datetime
from flask import render_template
from models.model import Model
from models.util import *


'''
with app.app_context():
    pass
'''


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/')
def index():
    model = Model()
    paper_list = model.get_all_paper()  # 获得所有期数列表
    max_paper = model.get_max_paper()
    paper_id = max_paper.id
    try:
        pic_info = model.get_pic_info(paper_id)
        print pic_info
        article_list = model.get_article_list(pic_info.id)
        page_id = pic_info.id
    except IndexError, e:
        return "so sad,the page has gone"
    area_list = model.get_area_list(page_id)
    column_list = model.get_column_list(max_paper.id)

    # 格式化日期时间
    for i in range(len(paper_list)):
        paper_list[i].pub_time = paper_list[i].time.strftime('%Y年%m月%d日')
    data = {'now': datetime.now().strftime('%Y年%m月%d日')}
    week = datetime.now().isoweekday()
    data['week'] = format_week(week)
    # 格式化大图片链接
    data['max_paper'] = max_paper.num
    data['pic_url'] = app.config['HOST'] + "/Newspaper/paper" + pic_info.pic_url[3:]
    data['current_num'] = max_paper.num  # 当前期数
    data['column_list'] = column_list
    data['current_page'] = column_list[0].id
    # 格式化报纸div
    for i in range(len(area_list)):
        y = str(area_list[i].y)[:-2]
        height = str(area_list[i].height)[:-2]
        title_y = int(y) + int(height) + 7
        area_list[i].title_y = str(title_y) + 'px'
        area_list[i].article_title = model.get_article_info(area_list[i].article_id).title
    column_list = model.get_column_list(max_paper.id)
    data['column_list'] = column_list
    model.close_session()
    return render_template("paper_index.html", article_list=article_list,
                           paper_list=paper_list,
                           data=data, area_list=area_list)


@app.route('/page/<int:page_id>')
def page(page_id):
    model = Model()
    print page
    paper_list = model.get_all_paper()
    max_paper = model.get_max_paper()
    try:
        pic_info = model.get_page_info(page_id)
        print pic_info
        article_list = model.get_article_list(pic_info.id)
    except IndexError, e:
        return "<h1>该页面不存在！<h1>"
    area_list = model.get_area_list(page_id)
    column_list = model.get_column_list(pic_info.paper_id)
    model.close_session()

    # 格式化日期时间
    for i in range(len(paper_list)):
        paper_list[i].pub_time = paper_list[i].time.strftime('%Y年%m月%d日')
    data = {'now': datetime.now().strftime('%Y年%m月%d日')}
    week = datetime.now().isoweekday()
    data['week'] = format_week(week)
    # 格式化大图片链接
    data['max_paper'] = max_paper.num
    data['pic_url'] = app.config['HOST'] + "/Newspaper/paper" + pic_info.pic_url[3:]
    data['current_num'] = model.get_paper_info(pic_info.paper_id)  # 当前期数
    data['current_page'] = page_id
    data['column_list'] = column_list
    # 格式化报纸页面div
    for i in range(len(area_list)):
        y = str(area_list[i].y)[:-2]
        height = str(area_list[i].height)[:-2]
        title_y = int(y) + int(height) + 7
        area_list[i].title_y = str(title_y) + 'px'
        area_list[i].article_title = model.get_article_info(area_list[i].article_id).title
    return render_template("paper_index.html", paper_list=paper_list, area_list=area_list, data=data,
                           article_list=article_list)


@app.route('/paper/<int:paper_id>')
def paper(paper_id):
    model = Model()
    paper_list = model.get_all_paper()
    max_paper = model.get_max_paper()
    try:
        pic_info = model.get_pic_info(paper_id)
        article_list = model.get_article_list(pic_info.id)
        page_id = pic_info.id
    except IndexError, e:
        return "该报纸页面不存在!"
    area_list = model.get_area_list(page_id)
    column_list = model.get_column_list(pic_info.paper_id)
    model.close_session()

    for i in range(len(paper_list)):
        paper_list[i].pub_time = paper_list[i].time.strftime('%Y年%m月%d日')
    data = {'now': datetime.now().strftime('%Y年%m月%d日')}
    week = datetime.now().isoweekday()
    data['week'] = format_week(week)
    # 格式化大图片链接
    data['max_paper'] = max_paper.num
    data['pic_url'] = app.config['HOST'] + "/Newspaper/paper" + pic_info.pic_url[3:]
    data['current_num'] = model.get_paper_info(paper_id)  # 当前期数
    data['current_page'] = page
    data['current_page'] = pic_info.id
    data['column_list'] = column_list
    print data
    # 格式化图片div位置
    for i in range(len(area_list)):
        y = str(area_list[i].y)[:-2]
        height = str(area_list[i].height)[:-2]
        title_y = int(y) + int(height) + 7
        area_list[i].title_y = str(title_y) + 'px'
        area_list[i].article_title = model.get_article_info(area_list[i].article_id).title
    return render_template("paper_index.html", data=data, area_list=area_list, paper_list=paper_list,
                           article_list=article_list)


@app.route('/article/<int:article_id>')
def article(article_id):
    data = {'now': datetime.now().strftime('%Y年%m月%d日')}
    week = datetime.now().isoweekday()
    data['week'] = format_week(week)
    model = Model()
    paper_list = model.get_all_paper()
    max_paper = model.get_max_paper()
    try:
        article_info = model.get_article_info(article_id)
        print article_info.paper_id
        pic_info = model.get_page_info(article_info.page_id)
        data['current_num'] = model.get_paper_info(article_info.paper_id)  # 当前期数
    except Exception, e:
        return "so sad,article not found!"
    area_list = model.get_area_list(article_info.page_id)
    column_list = model.get_column_list(pic_info.paper_id)
    model.close_session()

    for i in range(len(paper_list)):
        paper_list[i].pub_time = paper_list[i].time.strftime('%Y年%m月%d日')
    # 格式化大图片链接
    data['max_paper'] = max_paper.num
    data['pic_url'] = app.config['HOST'] + "/Newspaper/paper" + pic_info.pic_url[3:]
    data['current_page'] = pic_info.id
    data['column_list'] = column_list
    # 格式化图片div位置
    for i in range(len(area_list)):
        y = str(area_list[i].y)[:-2]
        height = str(area_list[i].height)[:-2]
        title_y = int(y) + int(height) + 7
        area_list[i].title_y = str(title_y) + 'px'
        area_list[i].article_title = model.get_article_info(area_list[i].article_id).title
    return render_template("article_index.html", article=article_info, data=data, paper_list=paper_list,
                           area_list=area_list)





