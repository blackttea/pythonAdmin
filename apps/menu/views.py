import json

from django.forms import model_to_dict
from django.shortcuts import render
from django.http import HttpResponse
from apps.user.check import token_required
from menu.models import Menu


@token_required()
def getMenu(request):
    json_str = request.body
    # json_str = json_str.decode()  # python3.6及以上不用这一句代码
    # dict_data = json.loads(json_str)  # loads把str转换为dict，dumps把dict转换为str
    print('1.==========================>')
    menu = []
    for item in Menu.objects.all():
        menu.append(model_to_dict(item))
    return response_success(message='用户登入成功', data={'code': '0', 'list': menu})


def response_success(message, data=None, data_list=[]):
    return HttpResponse(json.dumps({
        'code': 200,  # code由前后端配合指定
        'message': message,  # 提示信息
        'data': data,  # 返回单个对象
        'dataList': data_list  # 返回对象数组
    }, ensure_ascii=False), 'application/json')


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
