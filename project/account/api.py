from django.views.decorators.csrf import csrf_exempt
from django.urls import path
from django.http import JsonResponse

from .urls import urlpatterns

import re
import json


def api(func):
	'''
		前后端分离, post + json 数据交互
		@author dusc
	'''
	name = func.__name__

	@csrf_exempt
	def django_view(request):
		if request.method != 'POST':
			return JsonResponse({'code': 400, 'msg': '只支持POST'})
		print(dir(request))
		print(request.user)
		token = request.META['HTTP_TOKEN']
		print(request.COOKIES)

		try:
			params = json.loads(request.body.decode('utf8'))
		except:
			return JsonResponse({'code': 400, 'msg': '参数格式错误'})

		'''判断token'''
		 
		# token = Token.objects.filter(token=token)
		# if not token.exists():
		# 	return JsonResponse({'code': 401, 'msg': '未登录'})
		# else:
		# 	token = token.first()
		# 	if token.update_time < datetime.datetime.now() + datetime.timedelta(minutes=-30):
		# 		return JsonResponse({'code': 401, 'msg': '登录过期'})

		# token.update_time = datetime.datetime.now()
		# token.save()
		# params['user'] = token.user

		try:
			result = func(**params)
		except TypeError as e:
			a = re.findall(r'missing 1 required positional argument: \'(.*)\'', str(e))
			if a:
				return JsonResponse({'code': 400, 'msg': '缺少参数%s'% a[0]})
			else:
				return JsonResponse({'code': 400, 'msg': '参数类型错误'})
			

		return result

	urlpatterns.append(path('api/%s/' % name, django_view))


