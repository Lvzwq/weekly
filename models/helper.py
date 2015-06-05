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
    return appconfig['host'] + "/Newspaper/paper" + pic_url[3:]


def mk_file_dir():
    date = time_to_str(format='%Y%m')
    upload_dir = os.path.join(appconfig['web_root'], appconfig['upload_folder'], date)
    if not os.path.exists(upload_dir):
        try:
            os.makedirs(upload_dir)
        except OSError:
            return False
    return upload_dir


def get_filename():
    return '%s%s' % (time_to_str(format='%Y%m%d%H%M%S'), random.randrange(1000, 10000))


def save_file(fileobj, upload_folder, filename=None):
    """保存文件, 图片需要重新命名."""
    image_types = ["image/jpeg", 'image/jpg', 'image/png', "image/gif"]
    secure_type = []
    name, ext = os.path.splitext(fileobj.filename)  # 获得文件后缀
    if filename is None:
        filename = get_filename() + ext
    else:
        filename += ext
    if fileobj.mimetype in image_types:  # 图片格式
        print "图片格式"
        fullname = os.path.join(upload_folder, filename)
    elif fileobj.mimetype in secure_type:
        fullname = os.path.join(upload_folder, fileobj.filename)
    else:
        return False
    fileobj.save(fullname)
    return os.path.join(time_to_str(format="%Y%m"), filename)















