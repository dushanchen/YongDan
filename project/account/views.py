from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import *
from .tools import _check_user_, _page_aop_, _save_attr_, _add_edit_del_
from .api import api

def login(request):
    pass


def logout(request):
    pass


# 单表增删改查
@csrf_exempt
# @_check_user_
@_page_aop_
def user(request):
    ctx = {}

    ctx['objects'] = objs = User.objects.all()

    if request.method == 'POST':
        
        action = request.POST.get('action', '')

        _add_edit_del_(User, request, action)

        if action == 'search': # 自定义查询
            pass

        if action == 'validate_name': # 自定义ajax交互
            name = request.POST.get('name', '')
            if User.objects.filter(name=name).exists():
                return JsonResponse({'valid': False})
            else:
                return JsonResponse({'valid': True})


    return (ctx, 'account/user.html')


@api
def testapi(name, password):
    return JsonResponse({'name': name, 'password': password, 'code': 0})








