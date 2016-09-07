# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from profiles.models import Student, Interest, Chatroom, Team, Badge, Talent, up_file, file_info
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone
import shutil, os

# Create your views here.
def list_student(request):
#	student1 = { 'name':'陳紹恩', 'department':'IM', 'interest':'', 'talent':'', 'badge':'haha', 'follow':'', 'team':'', 'motto':'hahaha'}
	students = Student.objects.all()
	interests = Interest.objects.all()
	me = Student.objects.get(name=request.user)
	return render_to_response('student_list.html', locals())

@permission_required('profiles.can_view_base_profile', login_url='/create_student/')
def profile(request):
	student = Student.objects.get(name=request.user)
	#students = Student.objects.all()
	return render_to_response('my_profile.html', RequestContext(request, locals()))

@permission_required('profiles.can_edit_base_profile', login_url='/permission_error/')
def edit(request):
	student = Student.objects.get(name=request.user)
	team = Team.objects.all()
	talent = Talent.objects.all()
	if request.POST:
		motto = request.POST['motto']
		myteam = request.POST['team']
		mytalent = request.POST['talent']
		student.motto = motto
		student.team = Team.objects.get(name=myteam)
		student.talent = Talent.objects.get(name=mytalent)
		student.save()
		return render_to_response('my_profile.html', RequestContext(request, locals()))
	else:
		return render_to_response('edit_profile.html', RequestContext(request, locals()))

def student_create(request):
	errors = []
	inter = Interest.objects.all()
	if request.POST:
		name = request.user
		realname = request.POST['realname']
		nickname = request.POST['nickname']
		department = request.POST['department']
		motto = request.POST['motto']
		interest = Interest.objects.get(name='none')
		team = Team.objects.get(name='none')
		talent = Talent.objects.get(name='none')
		badge = Badge.objects.get(name='none')
		#follow = Follow.objects.get(name='none')
		# interest = request.POST['interest']
		# team = request.POST['team']
		# talent = request.POST['talent']
		# badge = request.POST['badge']
		# follow = request.POST['follow']
		if any(not request.POST[k] for k in request.POST):
			errors.append('* 有空白欄位！請不要留空！')
		if not errors:
			Student.objects.create(
				name=name,
				realname = realname,
				nickname = nickname,
				department = department,
				motto = motto,
				interest = interest,
				team = team,
				talent = talent,
				badge = badge,
			)
		return render_to_response('complete.html', RequestContext(request, locals()))
	else:
		return render_to_response('create_student.html', RequestContext(request, locals()))

def chatroom(request, idfrom, idto):
	s1=Student.objects.get(id=idfrom)
	s2=Student.objects.get(id=idto)
	chatroom1 = Chatroom.objects.filter(student1=s1, student2=s2)
	chatroom2 = Chatroom.objects.filter(student1=s2, student2=s1)
	chatroom = (chatroom1 | chatroom2).order_by('date_time')
	if request.POST:

		content = request.POST['content']
		date_time = timezone.localtime(timezone.now())
		Chatroom.objects.create(
			student1=Student.objects.get(id=idfrom),
			student2=Student.objects.get(id=idto),
			content=content,
			date_time=date_time
		)
	return render_to_response('chatroom.html', RequestContext(request, locals()))

#@permission_required('profiles.can_view_base_profile', login_url='/create_student/')
def other_profile(request):
	if request.GET.get('id'):
		myid = request.user.student_set.first().id
		me = Student.objects.get(name=request.user)
		student = Student.objects.get(id=request.GET['id'])
		return render_to_response('other_profile.html', RequestContext(request, locals()))
	if request.GET.get('follow'):
 		me = Student.objects.get(name=request.user)
 		student = Student.objects.get(id=request.GET['follow'])
 		me.follow.add(student)	
 		me.save()
 		return render_to_response('follow_complete.html', locals())
	else:
		return HttpResponseRedirect("/student_list/")

def upload(request):
	s1=Student.objects.get(id=request.user.student_set.first().id)
	if request.method == 'POST':# request.POST.get 如果沒有request到資料時會丟回None
		date = timezone.localtime(timezone.now())
        # 存入資料庫
		form = up_file(upload_datetime = date, student = s1) 
		form.save()
		files = [f for key, f in request.FILES.items()] #抓取檔案(可能多個檔案)
		if len(files) > 0:
			try:
				file_dir = os.path.join('/Users/handsome/Desktop/upload' , str(form.pk))
                #如果路徑中的檔案夾不存在就建立一個新的
				if not os.path.exists(file_dir):
					os.makedirs(file_dir) 
					for file in files:    
                        #為了避免檔案名稱重複，因此存在server端時，把修改檔案名稱
						local_name = timezone.now().strftime('%Y%m%d%H%M%S')
						file_path = os.path.join(file_dir, local_name)
                        #存入資料庫
						file_save = file_info(
									File = up_file.objects.get(id=form.pk),
									local_name = local_name, #存在server檔名
									upload_name = file.name #原本檔名
									)
						file_save.save()
				# 開始讀寫檔案至server
    #              'b' 如果檔案存在就會被覆蓋
						destination =open(file_path,'wb+')
						for chunk in file.chunks():
 							destination.write(chunk)
 							destination.close()
			except:
				pass
			# 		shutil.rmtree(file_dir, True)   #發生例外，就刪除路徑檔案
	return render_to_response('upload.html', RequestContext(request, locals()))

def upload_head(request):
	s1=Student.objects.get(id=request.user.student_set.first().id)
	if request.method == 'POST':# request.POST.get 如果沒有request到資料時會丟回None
		date = timezone.localtime(timezone.now())
        # 存入資料庫
		form = up_file(upload_datetime = date, student = s1) 
		form.save()
		files = [f for key, f in request.FILES.items()] #抓取檔案(可能多個檔案)
		if len(files) > 0:
			try:
				file_dir = os.path.join('/Users/handsome/Desktop/upload' , str(form.pk))
                #如果路徑中的檔案夾不存在就建立一個新的
				if not os.path.exists(file_dir):
					os.makedirs(file_dir) 
					for file in files:    
                        #為了避免檔案名稱重複，因此存在server端時，把修改檔案名稱
						local_name = timezone.now().strftime('%Y%m%d%H%M%S')
						file_path = os.path.join(file_dir, local_name)
                        #存入資料庫
						file_save = file_info(
									File = up_file.objects.get(id=form.pk),
									local_name = local_name, #存在server檔名
									upload_name = file.name #原本檔名
									)
						file_save.save()
				# 開始讀寫檔案至server
    #              'b' 如果檔案存在就會被覆蓋
						destination =open(file_path,'wb+')
						for chunk in file.chunks():
 							destination.write(chunk)
 							destination.close()
			except:
				pass
			# 		shutil.rmtree(file_dir, True)   #發生例外，就刪除路徑檔案
	return render_to_response('upload_head.html', RequestContext(request, locals()))

def follow_complete(request):
	return render_to_response('follow_complete.html', locals())

def list_team(request):
	students = Student.objects.all()
	teams = Team.objects.all()
	return render_to_response('team_list.html', locals())

def create_team(request):
	errors = []
	if request.POST:
		student = request.user.student_set.first()
		teamname = request.POST['teamname']
		need = request.POST['need']
		interest = Interest.objects.get(name='Sustainable Environment')
		if any(not request.POST[k] for k in request.POST):
			errors.append('* 有空白欄位！請不要留空！')
		if not errors:
			t = Team.objects.create(
					name=teamname,
					interest = interest,
					need = need,
				)
			student.team = t
			student.save()
		return render_to_response('complete.html', RequestContext(request, locals()))
	else:
		return render_to_response('create_team.html', RequestContext(request, locals()))

def individual_profile(request):
	try:
		student = Student.objects.get(name=request.user)
	except Student.DoesNotExist:
		student=None

	if request.GET.get('id'):
		individual = Student.objects.get(id=request.GET['id'])
		return render_to_response('individual_profile.html', locals())
	elif request.GET.get('follow'):
		individual = Student.objects.get(id=request.GET['follow'])
		student.follow.add(individual)	
		student.save()
		return render_to_response('follow_complete.html', locals())
	else:
		return HttpResponse("errr...")

def follow_complete(request):
 	return render_to_response('follow_complete.html', locals())

