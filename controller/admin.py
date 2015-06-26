# -*- coding: utf-8 -*-
# 安装Flask-Session  sudo pip install Flask-Session
from flask import Blueprint
from flask import (render_template, request, redirect, url_for, abort)
from models.model import Model
from models.helper import *
from models.url import (login_required, do_signin, is_login, destroy_session, set_login)
import collections

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
    """编辑文章."""
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
    """添加文章时的页面图片和文件上传"""
    ckeditor = request.args.get("CKEditor")
    ckeditor_func_name = request.args.get("CKEditorFuncNum")
    print ckeditor, ckeditor_func_name

    fileobj = request.files.get("upload")
    print "fileobj=", fileobj, dir(fileobj)
    is_saved = save_file(fileobj)
    if is_saved['status']:
        error = ""
        url = is_saved["result"][0]
    else:
        error = is_saved["result"]
        url = ""
    return """<script type="text/javascript">
            window.parent.CKEDITOR.tools.callFunction(%s, '%s', '%s');
          </script>""" % (ckeditor_func_name, url, error)


@app.route("/admin/add_paper", methods=['GET'])
@login_required
def add_paper():
    """新的期刊"""
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
    return render_template("new_paper.html", paper_info=paper_info, new=new, pages=pages)


@app.route("/admin/add_paper", methods=['POST'])
@login_required
def new_paper():
    """提交新的期刊数据到数据库."""
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
    """报刊中的大图上传以及新增报刊"""
    page_id = request.form.get("page_id")
    page_num = request.form.get("page_num")
    page_name = request.form.get("page_name").encode("utf-8")
    paper_num = request.args.get("paper_num")
    values = parse_param(params=["page_id", "page_num", "page_name", "paper_num"],
                         param_values=[page_id, page_num, page_name, paper_num],
                         param_required=[False, True, True, True],
                         param_types=[int, int, str, int],
                         param_default=dict(page_id=0))
    if not values["status"]:
        return response_with_json(values["msg"], -1)
    model = Model()
    paper_info = model.get_paper(values['msg']["paper_num"])
    if paper_info is None:
        return response_with_json("期刊不存在", -1)
    # 上传图片处理
    file_data = request.files.get("Filedata")
    model = Model()
    if values["msg"]["page_id"] == 0:  # 新增一张报刊
        page = model.new_page(paper_info.id,
                              values["msg"]["page_num"], "",
                              values["msg"]["page_name"])
        if page.id is None:
            return response_with_json("添加失败，请重试", -1)
        values["msg"]["page_id"] = str(page.id)
        upload_dir = save_file(file_data, filename=str(page.id))
    else:  # 修改报刊
        upload_dir = save_file(file_data, filename=str(page_id))
    if not upload_dir["status"]:  # 上传失败
        return response_with_json(upload_dir["result"], -1)
    model.update_page(values["msg"]["page_id"],
                      paper_id=paper_info.id,
                      num=values['msg']["page_num"],
                      pic_url=upload_dir["result"][1],
                      name=values["msg"]["page_name"])
    return response_with_json("操作成功")


@app.route("/admin/page", methods=['POST'])
def page_add():
    return


@app.route("/admin/updatePage", methods=["POST"])
@login_required
def update_page():
    """更新报刊"""
    page_id = request.form.get("page_id")
    page_num = request.form.get("page_num")
    page_name = request.form.get("page_name").encode("utf-8")
    values = parse_param(params=["page_id", "page_num", "page_name"],
                         param_values=[page_id, page_num, page_name],
                         param_types=[int, int, str],
                         param_required=[True, True, True])
    if values["status"]:
        print values
        model = Model()
        model.update_page(values["msg"]["page_id"],
                          num=values["msg"]["page_num"],
                          name=values["msg"]["page_name"])
        return response_with_json("更新成功")
    return response_with_json(values["msg"], -1)


@app.route("/admin/deletePage", methods=["POST"])
@login_required
def delete_page():
    """删除报刊"""
    page_id = request.form.get("page_id")
    values = parse_param(params=["page_id"],
                         param_values=[page_id],
                         param_types=[int],
                         param_required=[True])
    if not values["status"]:
        return response_with_json(values["msg"], -1)
    model = Model()
    model.delete_page(page_id)
    model.close_session()
    return response_with_json("删除成功")


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


@app.route("/admin/paper/delete", methods=['POST'])
@login_required
def paper_delete():
    """删除一周期刊"""
    paper_num = request.form.get("paper_num")
    value = parse_param(params=["paper_num"],
                        param_values=[paper_num],
                        param_required=[True],
                        param_types=[int])
    if not value['status']:
        return response_with_json("删除失败", -1)
    model = Model()
    is_deleted = model.delete_paper(value["msg"]["paper_num"])
    if is_deleted is None:
        return response_with_json("期刊已经不存在")
    model.close_session()
    return response_with_json("删除成功")


@app.route("/admin/article/<int:article_id>", methods=["GET"])
@login_required
def get_article(article_id):
    """获得一篇文章的信息"""
    model = Model()
    article_info = model.get_article_info(article_id)
    article = dict(id=article_info.id, content=article_info.content,
                   title=article_info.title, sub_title=article_info.sub_title,
                   time=time_to_str(article_info.time), author=article_info.author,
                   reply_title=article_info.reply_title, has_pic=article_info.has_pic,
                   show_author=article_info.show_author)
    return response_with_json(article)



@app.route("/admin/article", methods=["POST"])
@login_required
def admin_article_new():
    """新增一篇文章"""
    params = collections.OrderedDict()
    params["width"] = request.form.get("width")
    params["height"] = request.form.get("height")
    params["x"] = request.form.get("x")
    params["y"] = request.form.get("y")
    params["title"] = request.form.get("title").encode("utf-8")
    params["reply_title"] = request.form.get("reply_title").encode("utf-8")
    params["content"] = request.form.get("content").encode("utf-8")
    params["sub_title"] = request.form.get("sub_title").encode("utf-8")
    params["author"] = request.form.get("author").encode("utf-8")
    params["has_pic"] = request.form.get("has_pic")
    params["show_author"] = request.form.get("show_author")
    params["page_id"] = request.form.get("page_id")
    params_type = [int, int, int, int, str, str, str, str, str, int, int, int]
    params_required = [True for _ in range(12)]
    values = parse_param(params=params.keys(),
                         param_values=params.values(),
                         param_types=params_type,
                         param_required=params_required)
    if not values["status"]:
        return response_with_json(values["msg"], -1)
    model = Model()
    print params
    page = model.get_page_info(values["msg"]["page_id"])
    params["paper_id"] = page.paper_id
    article = model.insert_article(**params)
    params["article_id"] = article.id
    model.insert_area(**params)
    return response_with_json(dict(id=article.id))


@app.route("/admin/article/<int:article_id>", methods=["POST"])
@login_required
def update(article_id):
    """修改已经发布的文章"""
    params = collections.OrderedDict()
    params["id"] = article_id
    params["title"] = request.form.get("title").encode("utf-8")
    params["reply_title"] = request.form.get("reply_title").encode("utf-8")
    params["content"] = request.form.get("content").encode("utf-8")
    params["sub_title"] = request.form.get("sub_title").encode("utf-8")
    params["author"] = request.form.get("author").encode("utf-8")
    params["has_pic"] = request.form.get("has_pic")
    params["show_author"] = request.form.get("show_author")
    params["page_id"] = request.form.get("page_id")
    params_type = [int, str, str, str, str, str, int, int, int]
    params_required = [True for _ in range(9)]
    values = parse_param(params=params.keys(),
                         param_values=params.values(),
                         param_types=params_type,
                         param_required=params_required)
    if not values["status"]:
        return response_with_json(values["msg"], -1)
    model = Model()
    model.update_article(**params)
    return response_with_json("更新成功")


@app.route("/admin/add_page/<int:page_id>", methods=["GET"])
@login_required
def add_page(page_id):
    model = Model()
    page = model.get_page_info(page_id)
    if page is None:
        abort(404)
    num = model.get_paper_info(page.paper_id)
    return redirect(url_for("admin.add_paper", paper_num=num))


@app.route("/admin/paper/article", methods=["GET"])
@login_required
def paper_article():
    """获得一期周刊中所有的文章"""
    page_id = request.args.get("page_id")
    model = Model()
    page = model.get_page_info(page_id)
    if page is None:
        abort(404)
    article_list = model.get_articles(page.paper_id)
    return response_with_json(article_list)


@app.route("/admin/paper/issued/<int:issued>", methods=["GET"])
@login_required
def article_issued(issued):
    paper_id = request.args.get("paper_id")
    if issued not in [1, 0]:
        abort(404)
    model = Model()
    model.paper_issued(paper_id, issued)
    return response_with_json("更新成功")


@app.route("/admin/test", methods=["GET", "POST"])
def admin_test():
    """测试数据"""
    model = Model()
    print model.delete_paper(509)
    return "test"



