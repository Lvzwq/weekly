# -*- coding: utf-8 -*-
from config import appconfig
import json
from datetime import datetime
import os
import random
import decimal


def format_week(week=datetime.now().isoweekday()):
    weekly = [u'日', u'一', u'二', u'三', u'四', u'五', u'六', u'日']
    return weekly[week]


def time_to_str(tm=datetime.now(), format="%Y-%m-%d %H:%M:%S"):
    return tm.strftime(format).decode("utf-8")


def response_with_json(data, code=1):
    if code == 1:
        return json.dumps(dict(code=code, status="ok", data=data))
    else:
        return json.dumps(dict(code=code, status="error", data=data))


def set_param_default(param):
    """初始化."""
    paper_num = param.get('paper_num')
    pid = param.get('pid')
    dic = dict(prev=1, next=2, current_id=1, offset=0,
               paper_num=paper_num,
               limit=int(appconfig['paper_limit']))
    if not paper_num or not paper_num.isdigit():
        dic['paper_num'] = None
    if param.get('limit') and param.get('limit').isdigit():
        dic['limit'] = param.get('limit')
    if pid and pid.isdigit() and int(pid) > 1:
        dic['current_id'] = int(pid)
        dic['prev'] = dic['current_id'] - 1
        dic['next'] = dic['current_id'] + 1
        dic['offset'] = dic['limit'] * (dic['current_id'] - 1)
    return dic


def parse_param(params=[], param_values=[], param_types=[], param_required=[], param_default={}, param_length={}):
    """对参数进行校验."""
    result = dict(status=False, msg="")
    if len(params) != len(param_values) or len(params) != len(param_types):
        result["msg"] = "参数长度不一致"
    else:
        d = dict()
        zip_params = zip(params, param_values, param_types, param_required)
        for k in zip_params:
            k_default = param_default.get(k[0])
            k_length = param_length.get(k[0], {})
            try:
                k_result = check_param(k[0], k[1], k[2], k[3], param_default=k_default, param_length=k_length)
                if k_result["status"]:
                    d[k[0]] = k_result["msg"]
                else:
                    result["msg"] = k_result['msg']
                    return result
            except ValueError, error:
                result['msg'] = "[%s]不合法的数据类型,%s" % (k[0], str(error))
                return result
        result["status"] = True
        result['msg'] = d
    return result


def check_param(param, param_value, param_type, param_required, param_default=None, param_length={}):
    """参数类型检查."""
    if param_value is None and param_required:
        return dict(status=False, msg=err_msg(param, error_code=1))
    if param_value is None and not param_required:
        return dict(status=True, msg=param_default)
    if hasattr(param_value, "__len__") and param_length.get(param):
        length = param_value.__len__()
        if hasattr(param_length, "lt") and hasattr(param_length, "gt") and (
                        param_length["lt"] < length or param_length["gt"] > length):
            return dict(status=False, msg="{param}的长度应该小于{min}并且大于{max}".
                        farmat(param=param, mix=param_length["lt"], max=param_length["gt"]))
    try:
        param_value = param_type(param_value)
    except ValueError:
        try:
            if param_type is decimal.Decimal:
                param_value = param_type(str(param_value), param)
            else:
                param_value = param_type(param_value, param)
        except TypeError:
            param_value = param_type(param_value)
    return dict(status=True, msg=param_value)


code_num = {
    1: u"不能为空",
    2: u"应该是正整数"
}


def err_msg(param, error_code=1):
    error = code_num[error_code]
    return "{param}{error}".format(param=param, error=error)


def divide_area(area_list):
    for i in range(len(area_list)):
        y = str(area_list[i].y)[:-2]
        height = str(area_list[i].height)[:-2]
        title_y = int(y) + int(height) + 7
        area_list[i].title_y = str(title_y) + 'px'
    return area_list


def update_pic_url(pic_url):
    if pic_url[0:3] == "pic":
        return appconfig['host'] + "/Newspaper/paper" + pic_url[3:]
    else:
        return join_folder("/", appconfig["upload_folder"], pic_url)


def mk_file_dir(file_type="image"):
    date = time_to_str(format='%Y%m')
    upload_dir = os.path.join(appconfig['web_root'], appconfig['upload_folder'], file_type, date)  # 绝对路径
    http_folder = os.path.join("/", appconfig["upload_folder"], file_type, date)  # 相对浏览器路径
    db_folder = os.path.join(file_type, date)  # 存储到数据库中路径
    print "upload_folder", upload_dir
    if not os.path.exists(upload_dir):
        try:
            os.makedirs(upload_dir)
        except OSError:
            return False
    return upload_dir, http_folder, db_folder


def get_filename():
    return '%s%s' % (time_to_str(format='%Y%m%d%H%M%S'), random.randrange(1000, 10000))


def join_folder(*args):
    """拼接文件夹"""
    return os.path.join(*args)


def save_file(file_obj, upload_folder=None, filename=None):
    """保存文件, 图片需要重新命名."""
    image_types = ["image/jpeg", 'image/jpg', 'image/png', "image/gif"]
    secure_type = [".jpg", ".jpeg", ".png", ".doc", ".gif", ".zip", ".rar"]
    name, ext = os.path.splitext(file_obj.filename)  # 获得文件后缀
    if filename is None:
        filename = get_filename() + ext
    else:
        filename += ext
    if upload_folder is None:
        upload_folder = mk_file_dir()
    if not upload_folder:
        return dict(status=False, result=u"文件夹没有写权限")
    # 对文件上传类型进行安全检验
    if file_obj.mimetype == "application/octet-stream":  # 以二进制文件上传
        if ext in secure_type:
            fullname = os.path.join(upload_folder[0], filename)
            file_obj.save(fullname)
        else:
            return dict(status=False, result=u"不支持的文件格式")
    else:
        if file_obj.mimetype in image_types:  # 图片格式的文件上传
            fullname = os.path.join(upload_folder[0], filename)
            # 可能进行特殊处理
            """doing something"""
            file_obj.save(fullname)
        elif file_obj.mimetype in secure_type:  # 其他类型的文件上传
            fullname = os.path.join(upload_folder[0], filename)
            file_obj.save(fullname)
        else:
            return dict(status=False, result=u"文件格式不支持上传")
    return dict(status=True, result=(join_folder(upload_folder[1], filename),
                                     join_folder(upload_folder[2], filename)))















