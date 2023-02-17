import json
import time

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
    print(menu)
    return response_success(message='用户登入成功', data=menu)


@token_required()
def addMenu(request):
    json_str = request.body
    json_str = json_str.decode()  # python3.6及以上不用这一句代码
    dict_data = json.loads(json_str)  # loads把str转换为dict，dumps把dict转换为str

    print(dict_data, "==================")
    # 执行数据库插入
    menuList = []
    for m in dict_data:
        print(m['component'])
        menuList.append(Menu(
            title=m['title'],
            name=m['name'],
            path=m['path'],
            component=m['component'],
            hidden=m['hidden'],
            redirect=m['redirect'],
            parentId=m['parentId'],
            svgIcon=m['svgIcon'],
            seq=m['seq']))

    print(menuList)
    Menu.objects.bulk_create(menuList)
    return response_success(message="数据入库成功")


@token_required()
def updateMenu(request):
    json_str = request.body
    json_str = json_str.decode()  # python3.6及以上不用这一句代码
    dict_data = json.loads(json_str)  # loads把str转换为dict，dumps把dict转换为str
    # 执行数据库插入
    print(dict_data)

    queryset = Menu.objects.filter()
    upMenu = []  # 创建列表，用与承载批量更新的对象数据
    # 使用for循环，这里循环的是查询条件，如果不需要循环查询条件那么直接循环上面的queryset就可以省略下面的.first()步骤
    for _id in dict_data:  # goods_id_list 是无数查询 条件的列表，这里使用的 商品的id
        _obj = queryset.filter(id=_id['id']).first()  # 很重要！！！，必须先获得一条唯一的数据
        if _obj:  # 很重要！！！ 判断这条数据是否存在
            upMenu.append(_obj)  # 把修改数据后的对象添加到列表

    Menu.objects.bulk_update(upMenu, ['title', 'name', 'hidden', 'svgIcon', 'parentId', 'seq',
                                      'component', 'redirect'])
    return response_success(message="数据入库成功")


@token_required()
def delMenu(request):
    json_str = request.body
    json_str = json_str.decode()  # python3.6及以上不用这一句代码
    dict_data = json.loads(json_str)  # loads把str转换为dict，dumps把dict转换为str
    delList = [str(i) for i in dict_data]
    idstring = ','.join(delList)
    print(idstring)
    try:
        Menu.objects.extra(where=['id IN (' + idstring + ')']).delete()
        return response_success(message="菜单删除成功!")
    except:
        return response_failure('{"status":"fail", "msg":"ID不存在"}')


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
