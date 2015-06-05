# -*- coding: utf-8 -*-
# 安装Flask-Session  sudo pip install Flask-Session
from flask import Blueprint
from flask import (render_template, request, redirect, url_for, abort)
from models.model import Model
from models.helper import *
from models.url import (login_required, do_signin, is_login, destroy_session, set_login)

app = Blueprint("admin", __name__)


@app.route("/admin/login", methods=["GET", "POST"])
def login():
    if is_login():
        return redirect(url_for("admin.admin"))
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        username = request.form['uid']
        password = request.form['pwd']
        result = do_signin(username.strip(), password.strip())
        if result['status']:
            set_login(username)
            return response_with_json(result['msg'])
        else:
            return response_with_json(result['msg'], -1)
    else:
        return abort(404)


@app.route("/admin/index")
@login_required
def admin():
    model = Model()
    param = request.args
    arr = set_param_default(param)
    if arr['paper_num'] is None:
        max_paper = model.get_max_paper_issued()
        paper_info = model.get_paper(max_paper.num - arr['offset'])
    else:
        paper_info = model.get_paper(arr['paper_num'])
    paper_list = model.get_paper_list(arr['offset'], arr['limit'])
    paper_count = model.get_paper_count()
    if paper_info is None:
        page_list = list()
    else:
        page_list = model.get_column_list(paper_info.id)
    for i in range(len(page_list)):
        page_list[i].pic = update_pic_url(page_list[i].pic_url)
    data = dict(paper_list=paper_list, page_list=page_list)
    data['count'] = int(paper_count) / int(arr['limit']) + 1
    data.update(arr)
    model.close_session()
    return render_template("admin_index.html", data=data, paper_info=paper_info)


@app.route("/admin/edit/page/<int:page_id>", methods=['GET'])
@login_required
def page_edit(page_id):
    model = Model()
    page_info = model.get_page_info(page_id)
    if page_info is None:
        abort(404)
    page_info.pic = update_pic_url(page_info.pic_url)
    area_list = model.get_area_list(page_info.id)
    area_list = divide_area(area_list)
    return render_template("article_edit.html", page_info=page_info, area_list=area_list)


@app.route("/admin/file/upload", methods=['POST'])
@login_required
def file_upload():
    ckeditor = request.args.get("CKEditor")
    ckeditor_func_name = request.args.get("CKEditorFuncNum")
    print ckeditor, ckeditor_func_name
    print "request.files=", request.files
    print dir(request.files)
    fileobj = request.files.get("upload")
    print "fileobj=", fileobj, dir(fileobj)
    file_path = mk_file_dir()
    filename = save_file(fileobj, upload_folder=file_path)
    filename += '/static/upload/'
    return """<script type="text/javascript">
                window.parent.CKEDITOR.tools.callFunction(%s, '%s', '%s');
              </script>""" % (ckeditor_func_name, filename, "")


@app.route("/admin/add_paper", methods=['GET'])
@login_required
def add_paper():
    """添加新的一期"""
    new = False  # 是添加新的期刊还是修改期刊
    pages = []
    model = Model()
    paper_num = request.args.get("paper_num")
    if paper_num is None:
        new = True
        paper_info = model.get_max_paper_issued()
        paper_info.new_paper_num = paper_info.num + 1
        paper_info.current_time = time_to_str(format="%Y-%m-%d")
    else:
        paper_info = model.get_paper(paper_num)
        if paper_info is None:
            abort(404)
        pages = model.get_column_list(paper_info.id)
        for i in range(len(pages)):
            pages[i].pic = update_pic_url(pages[i].pic_url)
        model.close_session()
        print pages
    return render_template("new_paper.html", paper_info=paper_info, new=new, pages=pages)


@app.route("/admin/add_paper", methods=['POST'])
@login_required
def new_paper():
    """提交新的一期数据到数据库."""
    paper_num = request.form.get("paper_num")
    pub_time = request.form.get("pub_time")
    values = parse_param(params=["paper_num", "pub_time"],
                         param_values=[paper_num, pub_time],
                         param_types=[int, str],
                         param_required=[True, True])
    if not values["status"]:
        return response_with_json(values["msg"], -1)
    model = Model()
    paper = model.new_paper(values['msg']["paper_num"], pub_time=values['msg']['pub_time'])
    print paper
    if paper.id is None:
        return response_with_json("添加新的期刊失败")
    model.close_session()
    return response_with_json("添加成功")


@app.route("/admin/image/upload", methods=['POST'])
@login_required
def image_upload():
    """报刊中的大图上传"""
    page_id = request.form.get("page_id")
    page_num = request.form.get("page_num")
    page_name = request.form.get("page_name")
    paper_num = request.args.get("paper_num")
    values = parse_param(params=["page_id", "page_num", "page_name", "paper_num"],
                         param_values=[page_id, page_num, page_name, paper_num],
                         param_required=[False, True, True, True],
                         param_types=[int, int, str, int],
                         param_default=dict(page_id=0))
    if not values["status"]:
        return response_with_json(value["msg"], -1)
    print values
    model = Model()
    paper = model.get_paper(values["msg"]["paper_num"])
    if paper is None:
        return response_with_json("期刊还没有创建，不能添加报刊", -1)
    file_data = request.files.get("Filedata")
    filename = request.form.get("Filename")  # 原图片名
    print "file_data=", file_data

    """每期报刊的图片"""
    return "1"


@app.route("/admin/logout")
def logout():
    """退出登录"""
    destroy_session()
    return redirect(url_for("admin.login"))


@app.route("/admin/updatePassword", methods=['GET', 'POST'])
@login_required
def update_password():
    """修改密码"""
    return "update password"


@app.route("/admin/article/<int:article_id>", methods=["GET"])
@login_required
def get_article(article_id):
    """获得一篇文章的信息"""
    model = Model()
    article_info = model.get_article_info(article_id)
    print article_info, article_info.__dict__
    article = dict(id=article_info.id, content=article_info.content,
                   title=article_info.title, sub_title=article_info.sub_title,
                   time=time_to_str(article_info.time), author=article_info.author,
                   reply_title=article_info.reply_title, has_pic=article_info.has_pic,
                   show_author=article_info.show_author)
    return response_with_json(article)


@app.route("/admin/paper/delete", methods=['POST'])
@login_required
def paper_delete():
    """删除一周期刊"""
    paper_id = request.form.get("paper_id")
    value = parse_param(params=["paper_id"],
                        param_values=[paper_id],
                        param_required=[True],
                        param_types=[int])
    if not value['status']:
        return response_with_json("删除失败", -1)
    print value
    model = Model()
    model.close_session()
    return response_with_json("删除成功")

@app.route("/update/<int:article_id>")
def update(article_id):
    pass





