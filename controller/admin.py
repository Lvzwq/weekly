# -*- coding: utf-8 -*-
# 安装Flask-Session  sudo pip install Flask-Session
from flask import session, flash
from flask import render_template, request, redirect, url_for
import hashlib
from datetime import timedelta
from models.model import Model
from models.util import *
from controller import is_login, do_signin, check_param


@app.route("/login", methods=["GET", "POST"])
def login():
    if is_login():
        return redirect(url_for("admin"))
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        username = request.form['uid']
        password = request.form['pwd']
        result = json.loads(do_signin(username.strip(), password.strip()))
        if result['status'] == True:
            flash('You were successfully logged in')
            session.permanent = True
            app.permanent_session_lifetime = timedelta(minutes=5)
            session['uid'] = hashlib.md5(username).hexdigest()
            session['logged'] = 1
            return redirect(url_for("admin"))
        else:
            flash(result['msg'])
            return redirect(url_for("login"))
    else:
        return "unsupported login way"


@app.route("/admin")
def admin():
    if is_login():
        model = Model()
        param = request.args
        arr = check_param(param)
        print arr
        if arr['paper_num'] == None:
            arr['paper_num'] = model.get_max_paper().num
        paper_list = model.get_paper_list(arr['limit'] * (arr['current_id'] - 1), arr['limit'])
        paper_count = model.get_paper_count()
        paper_info = model.get_paper(arr['paper_num'])
        print paper_info
        data = {}
        data['paper_list'] = paper_list
        data['count'] = int(paper_count) / int(arr['limit']) + 1
        data.update(arr.copy())
        return render_template("admin.html", data=data,paper_info=paper_info)
    return redirect(url_for("login"))


@app.route("/edit")
def edit():
    model = Model()
    if not request.args.get("paper_num"):
        return redirect(url_for("admin"))
    else:
        paper_num = request.args.get('paper_num')
        if paper_num.isdigit():
            try:
                print paper_num

            except Exception, e:
                print e
                pass
    return render_template("edit_page.html")


from werkzeug.utils import secure_filename
import os


@app.route("/upload", methods=('GET', 'POST'))
def upload():
    if request.method == "POST":
        if not request.files:
            return redirect(url_for("admin"))
        else:
            f = request.files['upload']
            print f
            # print f.read()
            # print f.stream.read()
            fname = secure_filename(f.filename)  # 获取一个安全的文件名，且仅仅支持ascii字符；
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], fname)
            print filepath
            print f.save(filepath)
            return 'upload success'
    else:
        return "upload"


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
    result = model.insert_article(7421, article)
    print result
    # result = model.insert_article(article)
    return "kkk"


@app.route("/update/<int:article_id>")
def update(article_id):
    pass


@app.route("/logout")
def logout():
    pass
