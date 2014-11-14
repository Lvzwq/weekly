# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from flask import request, redirect, url_for
from flask import flash
from model import Model
from datetime import datetime
import json
from util import format_week, check_login, check_param
from config.appconfig import Config, ADMIN_USER
import sys

app = Flask(__name__)
app.config.from_object(Config)
reload(sys)
sys.setdefaultencoding("utf-8")

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
    print paper_id
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
    data['current_paper'] = max_paper.num  # 当前期数
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
    data['current_paper'] = model.get_paper_info(pic_info.paper_id)  # 当前期数
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
        return "该报纸页面不存在！"
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
    data['current_paper'] = paper_id  # 当前期数
    data['current_page'] = page
    data['current_page'] = pic_info.id
    data['column_list'] = column_list
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
        data['current_paper'] = model.get_paper_info(article_info.paper_id)  # 当前期数
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

# 安装Flask-Session  sudo pip install Flask-Session
from flask import session
import hashlib
from datetime import timedelta


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        username = request.form['uid']
        password = request.form['pwd']
        result = json.loads(check_login(username.strip(), password.strip()))
        if result['status'] == True:
            flash('You were successfully logged in')
            session.permanent = True
            app.permanent_session_lifetime = timedelta(minutes=5)
            session['uid'] = hashlib.md5(username).hexdigest()
            session['logged'] = 1
            print session['uid']
            return redirect(url_for("admin"))
        else:
            flash(result['msg'])
            return redirect(url_for("login"))


@app.route("/admin")
def admin():
    if not session.get('uid') or not session.get('logged'):
        return redirect(url_for("index"))
    else:
        uid = session.get('uid')
        logged = session.get('logged')
        if uid == hashlib.md5(ADMIN_USER).hexdigest() and logged == 1:
            model = Model()
            # 重复需要优化
            if not request.args.get("limit"):
                limit = app.config['PAPER_LIMIT']
            else:
                if request.args.get('limit').isdigit():
                    limit = request.args.get('limit')
                else:
                    limit = app.config['PAPER_LIMIT']
            # 初始化
            current_id = 1
            offset = 0
            prev = 1
            next = 2
            if not request.args.get("pid"):
                pass
            else:
                if request.args.get('pid').isdigit():
                    current_id = int(request.args.get("pid"))
                    offset = (current_id - 1) * limit
                    prev = current_id - 1
                    next = current_id + 1

            paper_list = model.get_paper_list(offset, limit)
            paper_count = model.get_paper_count()
            data = {'paper_list': paper_list}
            data['count'] = int(paper_count) / int(limit) + 1
            data['current_id'] = current_id
            data['prev'] = prev
            data['next'] = next
            return render_template("admin.html", data=data)
        else:
            return redirect(url_for("login"))


@app.route("/edit")
def edit():
    model = Model()
    if not request.args.get("paper_num"):
        return redirect("/index")
    else:
        paper_num = request.args.get('paper_num')
        if paper_num.isdigit():
            try:
                pass

            except Exception, e:
                pass
    return render_template("edit_page.html")


from werkzeug.utils import secure_filename
import os


@app.route("/upload", methods=('GET', 'POST'))
def upload():
    if not request.files:
        return redirect(url_for("admin"))
    else:
        f = request.files['file']
        fname = secure_filename(f.filename)  # 获取一个安全的文件名，且仅仅支持ascii字符；
        f.save(os.path.join(app.config['/home/ilovey/workspace/images'], fname))
        return '上传成功'


@app.route("/submit", methods=('GET', 'POST'))
def submit():
    article = {}
    article['title'] = request.form.get('title', None)
    article['sub_title'] = request.form.get('sub_title', None)
    article['content'] = request.form.get('content', None)
    article['reply_title'] = request.form.get('reply_title', None)
    article['author'] = request.form.get('author', '')
    article['keyword'] = request.form.get('Nkeyword', '')
    article['has_pic'] = request.form.get('has_pic', 'a')
    article['show_author'] = request.form.get("show_author", 0)
    article['time'] = datetime.now()
    model = Model()
    result= model.insert_article(7421, article)
    print result
    # result = model.insert_article(article)
    return "kkk"


@app.route("/update/<int:article_id>")
def update(article_id):
    pass



@app.route("/logout")
def logout():
    pass


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5000)
