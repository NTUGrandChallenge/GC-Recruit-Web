# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.template import RequestContext
from django.contrib.sessions.models import Session
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Permission, User
from django.contrib.auth.decorators import login_required, permission_required
from profiles.models import Student, Team, Badge
from django.contrib.auth.models import Permission, User
from django.utils import timezone



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
		return render_to_response('registration/login.html', RequestContext(request, locals()))

def index(request):
	all_number = len(User.objects.all())
	students = Student.objects.all()
	wait_number = len(students)
	teams = Team.objects.filter(captain_name='postgres')
	badges = Badge.objects.all()
	return render_to_response('index.html', RequestContext(request, locals()))

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/index/')

def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			# perm = Permission.objects.get(codename='wait')
			# user.user_permissions.add(perm)
			return HttpResponseRedirect('/my_profile/')
	else:
		form = UserCreationForm()
	return render_to_response('register.html', RequestContext(request, locals()))

def perror(request):
	error_msg = 'NO_ACCESS'
	return render_to_response('permission_error.html', RequestContext(request, locals()))

@permission_required('profiles.wait', login_url='/agree/')
def wait(request):
	return render_to_response('waiting.html', RequestContext(request, locals()))

def use_session(request):
    if  'name' in request.session:
        return HttpResponse('your name is %s'%request.session['name'])
    else:
        request.session['name'] = 'Jacky'
        return HttpResponse('Set name as Jacky')

def complete(request):
	to = '/'
	return render_to_response('complete.html', RequestContext(request, locals()))

