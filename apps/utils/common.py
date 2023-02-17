import json

from django.http import HttpResponse


def response_failure(message):
    return HttpResponse(json.dumps({
        'code': 500,
        'message': message
    }, ensure_ascii=False), 'application/json')


def response_success(message, data=None, data_list=[], total=None, page=None, pageSize=None):
    return HttpResponse(json.dumps({
        'code': 200,  # code由前后端配合指定
        'message': message,  # 提示信息
        'data': data,  # 返回单个对象
        'dataList': data_list,  # 返回对象数组
        'total': total,  # 记录总数
        'page': page,  # 当前页面
        'pageSize': pageSize  # 当前页面分页大小
    }, ensure_ascii=False), 'application/json')