import hashlib
import json
import random
from io import BytesIO

from django.forms import model_to_dict

from apps.user.models import Book, Code, Role
from apps.user.models import User
from django.http import HttpResponse
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.user.check import request_verify
from apps.user.check import token_required
from apps.user.formValidation import BookFrom
from apps.user.tool import objDictTool
import logging
import uuid
from ast import literal_eval

from utils.captcha.captcha import Captcha
from utils.util import gen_verify_code, send_email_code, rand_code, getUsername
from utils.common import response_failure, response_success

# 日志输出常量定义
logger = logging.getLogger('mylogger')

modelDict = {
    'user': User,
    'role': Role,
}


@request_verify('post')
def code(request):
    json_str = request.body
    # json_str = json_str.decode()  # python3.6及以上不用这一句代码
    dict_data = json.loads(json_str)  # loads把str转换为dict，dumps把dict转换为str
    print(json_str, "===========")
    text, image = Captcha.gene_graph_captcha()
    # 实例化管道,保存图片流数据
    out = BytesIO()
    # 图片保存管道中,png格式
    image.save(out, 'png')
    # 读取得时候指针回零0
    out.seek(0)
    # 把图片返回到浏览器上，通过response对象返回浏览器上
    response = HttpResponse(content_type='image/png')
    # 从管道把图片读取出来
    response.write(out.read())
    print(uuid.uuid1(), '===============', text)

    response['Content-length'] = out.tell()

    # books = Code.objects.all()
    # print(serializers.serialize("json", books))
    # for i in range(len(books)):
    #     print("主键：%s   值：%s" % (i + 1, books[i]))
    return response


@request_verify('post')
@token_required()
def info(request):
    username = getUsername(request)
    u = User.objects.filter(username=username)
    userInfo = model_to_dict(u[0])
    return response_success(message='success', data={'roles': ['admin'],
                                                     'menu': literal_eval(userInfo['menu']),
                                                     'page': userInfo['page'],
                                                     'level': userInfo['level'],
                                                     'username': userInfo['username']})


@request_verify('post')
def sendEmailCode(request):
    json_str = request.body
    json_str = json_str.decode()  # python3.6及以上不用这一句代码
    dict_data = json.loads(json_str)  # loads把str转换为dict，dumps把dict转换为str
    email_code = rand_code()
    send_email_code(email_code, "")
    # 执行数据库插入
    return response_success(message="验证码发送成功!")


# 登入方法认证
def login(request):
    json_str = request.body
    # json_str = json_str.decode()  # python3.6及以上不用这一句代码
    dict_data = json.loads(json_str)  # loads把str转换为dict，dumps把dict转换为str
    # 录入用户
    username = dict_data.get('username')
    # 录入密码
    password = md5(dict_data.get('password'), dict_data.get('username'))
    print(password)
    # 查询用户是否存在
    u = User.objects.filter(username=username, password=password)
    if u:
        # 生成用户登入凭证
        token = u[0].token
        return response_success(message='用户登入成功', data={'token': token})
    else:
        return response_failure(message='用户登入失败')


def getCommon(request, name, handle_data=None):
    m = modelDict.get(name)
    json_str = request.body
    dict_data = json.loads(json_str)
    # 当前页码
    page = dict_data['currentPage']
    # 当前分页大小
    page_size = dict_data['pageSize']
    cond = dict_data.get('data', {})
    condition = {}
    for c in cond:
        if cond.get(c):
            condition.setdefault(c, cond.get(c))
    role = m.objects.filter(**condition).order_by('id')
    # django 分页实体对象
    paginator = Paginator(role, page_size)
    # 查询总记录数
    total = paginator.count
    try:
        # 执行分页查询
        books = paginator.page(page)
    except PageNotAnInteger:
        # 执行分页查询,默认指定页码
        books = paginator.page(1)
    except EmptyPage:
        # 执行分页查询,默认指定页码
        books = paginator.page(paginator.num_pages)

    user_list = []
    for u in books:
        d = model_to_dict(u)
        if handle_data:
            handle_data(d)
        user_list.append(d)
    return response_success(message='后台响应成功', total=total, data=user_list,
                            page=page, pageSize=page_size)


def insertCommon(request, name, handle_fun):
    json_str = request.body
    json_str = json_str.decode()  # python3.6及以上不用这一句代码
    dict_data = json.loads(json_str)  # loads把str转换为dict，dumps把dict转换为str

    _obj = modelDict.get(name)()
    if handle_fun:
        handle_fun(dict_data)
    objDictTool.to_obj(_obj, **dict_data)
    # 执行数据库插入
    _obj.save()
    return response_success(message="数据入库成功")


def updateCommon(request, name, up_list, key_list=['id']):
    json_str = request.body.decode()
    dict_data = json.loads(json_str)
    m = modelDict.get(name)
    queryset = m.objects.filter()
    condition = {}
    up_data = {}
    update_list = []
    for _id in dict_data:
        for k in key_list:
            condition.setdefault(k, _id.get(k))
        for u in up_list:
            up_data.setdefault(u, _id.get(u))
        _obj = queryset.filter(**condition).first()
        if _obj:
            update_list.append(m(**_id))
    m.objects.bulk_update(update_list, up_list)
    return response_success(message="数据入库成功")


@request_verify('post')
def register(request):
    def md5Pass(dict_data):
        dict_data['password'] = md5(dict_data['password'], dict_data['username'])

    return insertCommon(request, 'user', md5Pass)


@request_verify('post')
@token_required()
def addRole(request):
    return insertCommon(request, 'role')


@token_required()
@request_verify('post')
def getRole(request):
    def dealMenu(d):
        if d['menu']:
            d['menu'] = literal_eval(d['menu'])
        else:
            d['menu'] = []

    return getCommon(request, 'role', dealMenu)


@token_required()
@request_verify('post')
def getUser(request):
    def dealMenu(d):
        if d['menu']:
            d['menu'] = literal_eval(d['menu'])
        else:
            d['menu'] = []

    return getCommon(request, 'user', dealMenu)


@token_required()
@request_verify('post')
def updateRole(request):
    up_list = ['name', 'menu', 'page', 'level']
    return updateCommon(request, 'role', up_list)


@token_required()
@request_verify('post')
def updateUser(request):
    up_list = ['username', 'password', 'email', 'phone', 'menu', 'page', 'level']
    return updateCommon(request, 'user', up_list)


def md5(pwd, SALT):
    # 实例化对象
    obj = hashlib.md5(SALT.encode('utf-8'))
    # 写入要加密的字节
    obj.update(pwd.encode('utf-8'))
    # 获取密文
    return obj.hexdigest()
