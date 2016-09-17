# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.template import RequestContext
from django.contrib.sessions.models import Session
from django.contrib.auth.forms import UserCreationForm




def welcome(request):
	if 'user_name' in request.GET and request.GET['user_name'] != '':
		return HttpResponse('Welcome!~'+request.GET['user_name'])
	else:
		return render_to_response('welcome.html', locals())

def login(request):
	if request.user.is_authenticated():
		return HttpResponse('/index/')
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')

	user = auth.authenticate(username=username, password=password)

	if user is not None and user.is_active:
		auth.login(request, user)
		return HttpResponseRedirect('/index/')
	else:
		return render_to_response('login.html', RequestContext(request, locals()))

def index(request):
	return render_to_response('index.html', RequestContext(request, locals()))

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/index/')

def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			perm = Permission.objects.get(codename='wait')
			request.user.user_permissions.add(perm)
			return HttpResponseRedirect('/accounts/login/')
	else:
		form = UserCreationForm()
	return render_to_response('register.html', RequestContext(request, locals()))

def perror(request):
	return render_to_response('permission_error.html', RequestContext(request, locals()))

def wait(request):
	return render_to_response('waiting.html', RequestContext(request, locals()))

def use_session(request):
	request.session['lucky_number'] = 8
	if 'lucky_number' in request.session:
		lucky_number = request.session['lucky_number']
		response = HttpResponse('Your lucky_number is ' + str(lucky_number))
	del request.session['lucky_number']
	return response

def complete(request):
	return render_to_response('complete.html', RequestContext(request, locals()))

