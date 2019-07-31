from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import *
from .tools import _check_user_, _page_aop_, _save_attr_, _add_edit_del_


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

    Dan = User

    ctx['objects'] = objs = Dan.objects.all()

    if request.method == 'POST':
        
        action = request.POST.get('action', '')

        _add_edit_del_(Dan, request, action)

        if action == 'search': # 自定义查询
            pass

        if action == 'validate_name': # 自定义ajax交互
            name = request.POST.get('name', '')
            if Dan.objects.filter(name=name).exists():
                return JsonResponse({'valid': False})
            else:
                return JsonResponse({'valid': True})


    return (ctx, 'account/user.html')












