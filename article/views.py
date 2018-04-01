#coding: utf8
from django.shortcuts import render,reverse
from .models import UserModel
from django.http import HttpResponse,HttpResponseRedirect
import uuid

# 1. 如果用户没有登陆,跳转到登陆页面
# 2. 如果用户登陆完成,跳转到index页面
# 3. 如果用户之前登陆过,访问index页面的时候,直接渲染

def index(request):
	sessionid = request.COOKIES.get("mysessionid",None)
	username = request.session.get(sessionid,None)
	if username:
		html = u'这是主界面,您的用户名是: {0}, sessionid = {1}'.format(username, sessionid)
		return HttpResponse(html)
	else:
		return HttpResponseRedirect(reverse('login'))

def login(request):
	if request.method == 'GET':
		return render(request,'login.html')
	else:
		username = request.POST.get('username',None)
		password = request.POST.get('password',None)
		userModel = UserModel.objects.filter(name=username,password=password).first()
		if userModel:
			# 代表登录成功
			# 1. 给客户端设置cookie
			response = HttpResponseRedirect(reverse('index'))
			sessionid = str(uuid.uuid4())
			response.set_cookie('mysessionid',sessionid)
			# 2. 设置session的值
			request.session[sessionid] = userModel.name
			# 3. 跳转到index页面
			return response
		else:
			return HttpResponse(u'用户名或密码错误')

def test(request):
	name = "xiang"
	password = "123456"
	userModel = UserModel(name=name,password=password)
	userModel.save()
	return HttpResponse('<h1>{0}</h1> user has created.'.format(name))

from django import forms
