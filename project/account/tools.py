from django.shortcuts import render
from django.utils.http import urlquote
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render,redirect,reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, JsonResponse, HttpRequest, StreamingHttpResponse



def _page_aop_(func):
    def view(request, *args, **kwargs):
        
        pagesize = int(request.POST.get('pagesize','1'))
        page = int(request.POST.get('page','1'))
        
        result = func(request, *args, **kwargs)

        if isinstance(result, tuple):
            print(result)
            res = result[0]
            res['pagesize'] = pagesize
            res['page'] = page
            print(res)
            paginator = Paginator(res['objects'], pagesize) 
            try:
                res['objects'] = paginator.page(page)
            except EmptyPage:
                res['objects'] = paginator.page(paginator.num_pages) 
            return render(request, result[1], res)

        elif isinstance(result, JsonResponse):
            return result

    view.__name__ = func.__name__

    return view



def _check_user_(func):

    def view(request, *args, **kwargs):
        if 'user_id' not in request.session:
            return redirect(operlogin)

        request.user = User.objects.filter(id=request.session['user_id']).first()

        #判断权限
    
        url = request.path
        method = request.method
        print(url)
        print(method)
        if method == 'POST':
            action = request.POST.get('action', '')
        else:
            action = request.GET.get('action', '')
        if action:
            url = url + '?action=' + action
        
        urls = request.session['urls']
        print(urls)
        if 'Admin' not in request.session['role']:
            if url not in urls or urls[url] != method:
                ctx = {'error':'权限拒绝'}
                return render(request, 'error.html', ctx)

        print(request.session['role'])
        return func(request, *args, **kwargs)

    return view


def _save_attr_(obj,request):
    fields = obj._meta.fields

    for field in fields:
        field_name = field.name
        value = request.POST.get(field_name, '')
        if value:
            obj.__setattr__(field_name, value)
        else:
            value = request.FILES.get(field_name, '')
            if value:
                obj.__setattr__(field_name, value)
    obj.save()


def _add_edit_del_(Dan, request, action):
    ''' 通用单表增删改操作 '''
    ''' dusc '''
    
    if action == 'add':
        obj = Dan()
        _save_attr_(obj, request)

    if action == 'delete':
        Dan.objects.get(id=int(id)).delete()

    if action == 'edit':
        id = request.POST.get('id', '')
        obj = Dan.objects.get(id=int(id))
        _save_attr_(obj, request)


