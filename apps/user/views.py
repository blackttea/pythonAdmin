import hashlib
import json
import random
from io import BytesIO

from apps.user.models import Book, Code
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

from utils.captcha.captcha import Captcha
from utils.util import gen_verify_code

# 日志输出常量定义
logger = logging.getLogger('mylogger')


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


@request_verify('get')
@token_required()
def info(request):
    return response_success(message='success', data={'roles': ['admin'], 'username': 'admin'})


@request_verify('post')
def register(request):
    logger.info("post request body 请求数据提交")
    json_str = request.body
    json_str = json_str.decode()  # python3.6及以上不用这一句代码
    dict_data = json.loads(json_str)  # loads把str转换为dict，dumps把dict转换为str

    item = User()
    dict_data['password'] = md5(dict_data['password'], dict_data['username'])
    print(dict_data, "==================")
    objDictTool.to_obj(item, **dict_data)
    # 执行数据库插入
    item.save()
    return response_success(message="数据入库成功")


# 登入方法认证
def login(request):
    json_str = request.body
    # json_str = json_str.decode()  # python3.6及以上不用这一句代码
    dict_data = json.loads(json_str)  # loads把str转换为dict，dumps把dict转换为str
    # 录入用户
    username = dict_data.get('username')
    # 录入密码
    password = md5(dict_data.get('password'), dict_data.get('username'))
    # 查询用户是否存在
    u = User.objects.filter(username=username, password=password)
    if u:
        # 生成用户登入凭证
        token = u[0].token
        return response_success(message='用户登入成功', data={'token': token})
    else:
        return response_failure(message='用户登入失败')


# Create your views here.
@token_required()
@request_verify('get')
def select(request):
    books = Book.objects.all()
    for i in range(len(books)):
        print("主键：%s   值：%s" % (i + 1, books[i]))

    return response_success(message='后台响应成功', data_list=serializers.serialize("json", books))


@token_required()
@request_verify('post')
def selectAll(request):
    books = Book.objects.all()
    for i in range(len(books)):
        print("主键：%s   值：%s" % (i + 1, books[i]))
    return response_success(message='后台响应成功', data_list=serializers.serialize("json", books))


@token_required()
@request_verify('get', ['page', 'pageSize'])
def selectPage(request):
    # 当前页码
    page = request.GET.get('page')
    # 当前分页大小
    page_size = request.GET.get('pageSize')
    book_list = Book.objects.all()
    # django 分页实体对象
    paginator = Paginator(book_list, page_size)
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
    return response_page_success(message='后台响应成功', data_list=serializers.serialize("json", books), total=total,
                                 page=page, pageSize=page_size)


@token_required()
@request_verify('post', ['page', 'pageSize'])
def selectPageAll(request):
    json_str = request.body
    json_str = json_str.decode()  # python3.6及以上不用这一句代码
    dict_data = json.loads(json_str)  # loads把str转换为dict，dumps把dict转换为str

    # 当前页码
    page = dict_data.get('page')
    # 当前分页大小
    page_size = dict_data.get('pageSize')
    book_list = Book.objects.all()
    # django 分页实体对象
    paginator = Paginator(book_list, page_size)
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
    return response_page_success(message='后台响应成功', data_list=serializers.serialize("json", books), total=total,
                                 page=page, pageSize=page_size)


@token_required()
def insert(request):
    # 获取参数,放入表单校验
    book_form = BookFrom(request.POST)
    # 判断校验是否成功
    if book_form.is_valid():  # 验证成功
        name = book_form.cleaned_data.get("name")
        author = book_form.cleaned_data.get("author")
        print("名称：%s   作者：%s" % (name, author))
        return response_success(message="Django 实体表单验证成功")
    else:
        errorDict = book_form.errors
        for key, value in errorDict.items():
            print("属性：%s   错误信息：%s" % (key, value))
        return response_success(message="Django 实体表单验证失败")


# json 数据提交,并转换为实体，执行入库操作
@token_required()
def insertJSON(request):
    logger.info("post request body 请求数据提交")
    json_str = request.body
    json_str = json_str.decode()  # python3.6及以上不用这一句代码
    dict_data = json.loads(json_str)  # loads把str转换为dict，dumps把dict转换为str

    item = Book()
    objDictTool.to_obj(item, **dict_data)
    print("名称: {}, 价格: {},  作者: {}".format(item.name, item.price, item.author))
    # 执行数据库插入
    item.save()
    return response_success(message="数据入库成功")


def response_success(message, data=None, data_list=[]):
    return HttpResponse(json.dumps({
        'code': 200,  # code由前后端配合指定
        'message': message,  # 提示信息
        'data': data,  # 返回单个对象
        'dataList': data_list  # 返回对象数组
    }, ensure_ascii=False), 'application/json')


def md5(pwd, SALT):
    # 实例化对象
    obj = hashlib.md5(SALT.encode('utf-8'))
    # 写入要加密的字节
    obj.update(pwd.encode('utf-8'))
    # 获取密文
    return obj.hexdigest()

def response_failure(message):
    return HttpResponse(json.dumps({
        'code': 500,
        'message': message
    }, ensure_ascii=False), 'application/json')


def response_page_success(message, data=None, data_list=[], total=None, page=None, pageSize=None):
    return HttpResponse(json.dumps({
        'code': 200,  # code由前后端配合指定
        'message': message,  # 提示信息
        'data': data,  # 返回单个对象
        'dataList': data_list,  # 返回对象数组
        'total': total,  # 记录总数
        'page': page,  # 当前页面
        'pageSize': pageSize  # 当前页面分页大小
    }, ensure_ascii=False), 'application/json')
