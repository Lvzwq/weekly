# -*- coding: utf-8 -*-
from flask import (render_template, Blueprint, abort, redirect, url_for)
from models.model import Model
from models.helper import *
from config import appconfig

app = Blueprint("app", __name__)


# paper 13-273
# paper 表中num 284-508
# 1 paper = 4 page  page 中又paper_id

@app.route('/')
def index():
    model = Model()
    paper_list = model.get_all_paper()  # 获得所有期数列表
    column_list = model.get_column_list(paper_list[0].id)
    page_info = column_list[0]

    article_list = model.get_article_list(page_info.id)
    area_list = model.get_area_list(page_info.id)
    # 格式化日期时间
    for i in range(len(paper_list)):
        paper_list[i].pub_time = paper_list[i].time.strftime('%Y年%m月%d日')
    data = dict(now=datetime.now().strftime('%Y年%m月%d日'))
    data['week'] = format_week()
    # 格式化大图片链接
    data['max_paper_num'] = paper_list[0].num
    data['pic_url'] = update_pic_url(page_info.pic_url)
    data['current_num'] = paper_list[0].num  # 当前期数
    data['column_list'] = column_list
    data['current_page'] = column_list[0].id
    # 格式化报纸div
    area_list = divide_area(area_list)
    for i in range(len(area_list)):
        area_list[i].article_title = article_list[i].title
    model.close_session()
    return render_template("index.html",
                           article_list=article_list,
                           paper_list=paper_list,
                           data=data, area_list=area_list)


@app.route("/paper/<int:paper_id>", methods=['GET'])
def paper(paper_id):
    model = Model()
    page_info = model.get_pic_info(paper_id, 1)
    if page_info is None:
        abort(404)
    return redirect(url_for("app.page", page_id=page_info.id))


@app.route('/page/<int:page_id>')
def page(page_id):
    model = Model()
    page_info = model.get_page_info(page_id)
    if page_info is None:
        abort(404)
    paper_list = model.get_all_paper()
    area_list = model.get_area_list(page_id)
    column_list = model.get_column_list(page_info.paper_id)
    # 格式化日期时间
    for i in range(len(paper_list)):
        paper_list[i].pub_time = paper_list[i].time.strftime('%Y年%m月%d日')
    data = dict(now=datetime.now().strftime('%Y年%m月%d日'))
    data['week'] = format_week()
    # 格式化大图片链接
    data['max_paper_num'] = paper_list[0].num
    data['pic_url'] = update_pic_url(page_info.pic_url)
    data['current_num'] = model.get_paper_info(page_info.paper_id)  # 当前期数
    data['current_page'] = page_id
    data['column_list'] = column_list
    # 格式化报纸页面div
    article_list = model.get_article_list(page_id)
    area_list = divide_area(area_list)
    for i in range(len(area_list)):
        area_list[i].article_title = article_list[i].title
    return render_template("index.html", paper_list=paper_list, area_list=area_list, data=data,
                           article_list=article_list)

@app.route('/article/<int:article_id>')
def article(article_id):
    data = dict(now=datetime.now().strftime('%Y年%m月%d日'))
    data['week'] = format_week()
    model = Model()
    try:
        article_info = model.get_article_info(article_id)
    except IndexError:
        abort(404)
    paper_list = model.get_all_paper()
    for i in range(len(paper_list)):
        paper_list[i].pub_time = paper_list[i].time.strftime('%Y年%m月%d日')
    page_info = model.get_page_info(article_info.page_id)
    column_list = model.get_column_list(page_info.paper_id)

    data['current_num'] = model.get_paper_info(article_info.paper_id)  # 当前期数
    data['max_paper_num'] = paper_list[0].num
    data['pic_url'] = update_pic_url(page_info.pic_url)
    data['current_page'] = page_info.id
    data['column_list'] = column_list
    # 格式化图片div位置
    article_list = model.get_article_list(page_info.id)
    area_list = model.get_area_list(article_info.page_id)
    area_list = divide_area(area_list)
    for i in range(len(area_list)):
        area_list[i].article_title = article_list[i].title
    return render_template("article.html", article=article_info, data=data, paper_list=paper_list,
                           area_list=area_list)


