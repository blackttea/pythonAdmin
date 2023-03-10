import json
import time
from ast import literal_eval

from django.forms import model_to_dict
from django.shortcuts import render
from django.http import HttpResponse
from apps.user.check import token_required
from menu.models import Menu
from utils.common import response_failure, response_success


@token_required()
def getMenu(request):
    menu = []
    for item in Menu.objects.all():
        tem = model_to_dict(item)

        if tem['permission']:
            tem['permission'] = literal_eval(tem['permission'])
        else:
            tem['permission'] = []
        menu.append(tem)
    return response_success(message='菜单获取成功', data=menu)


@token_required()
def addMenu(request):
    json_str = request.body
    json_str = json_str.decode()  # python3.6及以上不用这一句代码
    dict_data = json.loads(json_str)  # loads把str转换为dict，dumps把dict转换为str
    menu = ['title', 'name', 'hidden', 'svgIcon', 'parentId', 'seq', 'component', 'redirect', 'path', 'permission']
    # 执行数据库插入
    menuList = []
    for m in dict_data:
        for key in menu:
            m.get(key, None)
        menuList.append(Menu(**m))
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
    menu = ['title', 'name', 'hidden', 'svgIcon', 'parentId', 'seq', 'component', 'redirect', 'path', 'permission']
    for _id in dict_data:  # goods_id_list 是无数查询 条件的列表，这里使用的 商品的id
        _obj = queryset.filter(id=_id['id']).first()  # 很重要！！！，必须先获得一条唯一的数据
        print(type(_obj))
        if _obj:  # 很重要！！！ 判断这条数据是否存在-
            _obj.title = _id['title']
            _obj.name = _id['name']
            _obj.hidden = _id['hidden']
            _obj.svgIcon = _id['svgIcon']
            _obj.parentId = _id['parentId']
            _obj.seq = _id['seq']
            _obj.component = _id['component']
            _obj.redirect = _id['redirect']
            _obj.path = _id['path']
            _obj.permission = _id['permission']
            upMenu.append(_obj)  # 把修改数据后的对象添加到列表
    Menu.objects.bulk_update(upMenu, menu)
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
