# -*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from profiles.models import Student, Interest, Chatroom, Team, Badge, up_file, file_info, Teamroom, Role, Insurance
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone
import shutil, os, allauth
from django.contrib.auth.models import Permission, User


@permission_required('profiles.can_view_base_profile', login_url='/wait/')
def search(request):
	first_user_list = []
	first_user_list.append(User.objects.get(student=Student.objects.get(id=1)))
	if 'word' in request.GET:
		user_list = []
		keyword = request.GET['word']
		if not keyword:
			return render(request,'index.html')
		else:
			students = Student.objects.filter(realname__icontains = keyword)
			students2 = Student.objects.filter(nickname__icontains = keyword)

			for each in students:
				user = User.objects.get(student=each)
				user_list.append(user)
			for each in students2:
				user = User.objects.get(student=each)
				user_list.append(user)
			user_list = list(set(user_list))
			if len(user_list) == 0 :
				return render(request,'search.html', {'user_list' : [], 'error' : True, 'len' : 0, 'word': True, 'keyword' : keyword})
			else :
				return render(request,'search.html', {'user_list' : user_list, 'error' : False, 'len' : len(user_list), 'search': True, 'keyword' : keyword})
	if 'search' in request.GET:
		interests = request.GET.getlist("interest[]")
		roles = request.GET.getlist("role[]")
		#student_list = []
		user_list = []
		for interest in interests:
			students = Student.objects.filter(interest_id=interest)
			for each in students:
				user = User.objects.get(student=each)
				user_list.append(user)
#-------interest OR role search------
		for role in roles:#OR search
			students = Student.objects.filter(role_id=role)
			for each in students:
				if each not in student_list:
					user = User.objects.get(student=each)
					user_list.append(user)
#-------interst AND role search-----
#		final_student_list = []
#		for role in roles:
#			students = Student.objects.filter(role_id=role)
#			for each in students:
#				if each in student_list:
#					final_student_list.append(each)
#		if roles:
#			if final_student_list:
#				student_list = final_student_list
#			else:
#				student_list = []
#-------interest And role search-----
#-------to show the keyword on html-----
		Interests = []
		Roles = []
		for each in interests:
			tmp_interest = Interest.objects.filter(id=each)
			for each in tmp_interest:
				Interests.append(each)
		for each in roles:
			tmp_role = Role.objects.filter(id=each)
			for each in tmp_role:
				Roles.append(each)
#-------to show the keyword on html-----
		if len(user_list) == 0:
			return render(request, 'search.html', {'user_list': [], 'error': True, 'len': 0, 'search': True, 'interests': Interests, 'roles': Roles})
		else :
			return render(request, 'search.html', {'user_list': user_list, 'error' : False, 'len' : len(user_list), 'search': True, 'interests': Interests, 'roles': Roles})
		return render_to_response('search.html', RequestContext(request, locals()))
	else:
		return render_to_response('search.html', RequestContext(request, locals()))

# Create your views here.
@permission_required('profiles.can_view_base_profile', login_url='/wait/')
def list_student(request):
	students = Student.objects.all()
	interests = Interest.objects.all()
	me = Student.objects.get(name=request.user)
	return render_to_response('student_list.html', locals())

@permission_required('profiles.can_view_base_profile', login_url='/wait/')
def profile(request):
	student = Student.objects.get(name=request.user)
	if request.user.socialaccount_set.first() != None:
		facebook_id = request.user.socialaccount_set.first().uid
	#students = Student.objects.all()
	return render_to_response('my_profile.html', RequestContext(request, locals()))

@permission_required('profiles.can_edit_base_profile', login_url='/permission_error/')
def edit(request):
	student = Student.objects.get(name=request.user)
	interest = Interest.objects.all()
	role = Role.objects.all()
	if request.POST:
		motto = request.POST['motto']
		talent = request.POST['talent']
		myinterest = request.POST['interest']
		myrole = request.POST['role']
		student.motto = motto
		student.interest = Interest.objects.get(name=myinterest)
		student.role = Role.objects.get(name=myrole)
		student.save()
		return render_to_response('my_profile.html', RequestContext(request, locals()))
	else:
		return render_to_response('edit_profile.html', RequestContext(request, locals()))

def agree(request):
	if request.user.has_perm('profiles.can_write_student'):
		return HttpResponseRedirect('/create_student/')
	if 'agree' in request.POST:
		perm = Permission.objects.get(codename='can_write_student')
		request.user.user_permissions.add(perm)
		return render_to_response('create_student.html', RequestContext(request, locals()))
	return render_to_response('agree.html', RequestContext(request, locals()))


def student_create(request):
	if request.user.has_perm('profiles.can_insurance'):
		return HttpResponseRedirect('/insurance_create/')
	errors = []
	# inter = Interest.objects.all()
	if request.POST:
		name = request.user
		realname = request.POST['realname']
		nickname = request.POST['nickname']
		department = request.POST['department']
		motto = request.POST['motto']
		talent = request.POST['talent']
		none_team = Team.objects.get(name='none')
#		if any(not request.POST[k] for k in request.POST):
#			errors.append('* 有空白欄位！請不要留空！')
		if not errors:
			Student.objects.create(
				name=name,
				realname = realname,
				nickname = nickname,
				department = department,
				motto = motto,
				talent = talent,
				team = none_team
			)
			perm = Permission.objects.get(codename='can_insurance')
			request.user.user_permissions.add(perm)
		return render_to_response('insurance.html', RequestContext(request, locals()))
	else:
		return render_to_response('create_student.html', RequestContext(request, locals()))

def check(y,m,d):
	
	if (y % 4) == 0:
		if m == 2:
			if d > 29:
				return False
		if m == 4 or 6 or 9 or 11:
			if d ==31:
				return False
	else:
		if m == 2:
			if d > 28:
				return False
		if m == 4 or 6 or 9 or 11:
			if d ==31:
				return False
	return True

def insurance_create(request):
	if request.user.has_perm('profiles.wait'):
		return HttpResponseRedirect('/wait/')
	errors = []
	year = list(range(1950, 2001))
	month = list(range(1, 13))
	day = list(range(1, 32))
	if request.POST:
		student = request.user.student_set.first()
		birthday_y = request.POST["birthday_y"]
		birthday_m = request.POST["birthday_m"]
		birthday_d = request.POST["birthday_d"]

		security_id = request.POST['security_id']
		phone = request.POST['phone']
		emergency = request.POST['emergency']
		emergency_relationship = request.POST['emergency_relationship']
		emergency_phone = request.POST['emergency_phone']
#		if any(not request.POST[k] for k in request.POST):
#			errors.append('* 有空白欄位！請不要留空！')
		if check(int(birthday_y), int(birthday_m), int(birthday_d))==False:
			errors.append('生日錯誤請重新輸入！')

		if not errors:
			Insurance.objects.create(
				student=student,
				birthday_y=birthday_y,
				birthday_m=birthday_m,
				birthday_d=birthday_d,
				security_id=security_id,
				phone=phone,
				emergency=emergency,
				emergency_relationship=emergency_relationship,
				emergency_phone=emergency_phone
			)
			perm = Permission.objects.get(codename='wait')
			request.user.user_permissions.add(perm)
			return render_to_response('complete.html', RequestContext(request, locals()))
	return render_to_response('insurance.html', RequestContext(request, locals()))

@permission_required('profiles.can_view_base_profile', login_url='/wait/')
def chatroom(request, idfrom, idto):
	me = Student.objects.get(name=request.user)
	s1=Student.objects.get(id=idfrom)
	s2=Student.objects.get(id=idto)
	chatroom1 = Chatroom.objects.filter(student1=s1, student2=s2)
	chatroom2 = Chatroom.objects.filter(student1=s2, student2=s1)
	chatroom = (chatroom1 | chatroom2).order_by('date_time')
	if request.POST:
		content = request.POST['content']
		date_time = timezone.localtime(timezone.now())
		# #如果session沒有被設置，才將資料加入資料庫
		# if 'ok' not in request.session:
		# 	request.session['ok'] = 'ok'
		Chatroom.objects.create(
				student1=Student.objects.get(id=idfrom),
				student2=Student.objects.get(id=idto),
				content=content,
				date_time=date_time
			)
	return render_to_response('chatroom.html', RequestContext(request, locals()))

@permission_required('profiles.can_view_base_profile', login_url='/wait/')
def other_profile(request):
	if request.GET.get('id'):
		myid = request.user.student_set.first().id
		me = Student.objects.get(name=request.user)
		student = Student.objects.get(id=request.GET['id'])
		user = User.objects.get(student=student)
		if user.socialaccount_set.first() != None:
			facebook_id = user.socialaccount_set.first().uid
		return render_to_response('other_profile.html', RequestContext(request, locals()))
	if request.GET.get('follow'):
 		me = Student.objects.get(name=request.user)
 		student = Student.objects.get(id=request.GET['follow'])
 		me.follow.add(student)	
 		me.save()
 		return render_to_response('follow_complete.html', locals())
	else:
		return HttpResponseRedirect("/student_list/")

@permission_required('profiles.can_view_base_profile', login_url='/wait/')
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


def follow_complete(request):
	return render_to_response('follow_complete.html', locals())

@permission_required('profiles.can_view_base_profile', login_url='/wait/')
def list_team(request):
	students = Student.objects.all()
	teams = Team.objects.all()
	return render_to_response('team_list.html', locals())

@permission_required('profiles.can_create_team_profile', login_url='/permission_error/')
def create_team(request):
	errors = []
	interests = Interest.objects.all()
	if request.POST:
		student = request.user.student_set.first()
		teamname = request.POST['teamname']
		content = request.POST['content']
		team_interest = request.POST['interest']
		captain_name = student.nickname
		if any(not request.POST[k] for k in request.POST):
			errors.append('* 有空白欄位！請不要留空！')
		if not errors:
			t = Team.objects.create(
					name=teamname,
					captain_name=captain_name,
					interest = Interest.objects.get(name=team_interest),
					content = content,
				)
			student.team = t
			perm = Permission.objects.get(codename='can_create_team_profile')
			request.user.user_permissions.remove(perm)
			student.save()
		return render_to_response('complete.html', RequestContext(request, locals()))
	else:
		return render_to_response('create_team.html', RequestContext(request, locals()))

def follow_complete(request):
 	return render_to_response('follow_complete.html', locals())

@permission_required('profiles.can_view_base_profile', login_url='/wait/')
def teamroom(request,teamid):
	me = Student.objects.get(name=request.user)
	team = Team.objects.get(id=teamid)
	teamroom = team.teamroom_set.order_by('date_time')
	if me.team == team:
		member = True
	else:
		member = False
	if request.POST:
		content = request.POST['content']
		date_time = timezone.localtime(timezone.now())
		Teamroom.objects.create(
			team=team,
			speaker=me,
			content=content,
			date_time=date_time
		)
	return render_to_response('teamroom.html', RequestContext(request, locals()))

@permission_required('profiles.can_view_base_profile', login_url='/wait/')
def team_profile(request, teamid):
	me = Student.objects.get(name=request.user)
	team = Team.objects.get(id=teamid)
	none_team = Team.objects.get(name='none')
	if request.POST.get('id'):
		return render_to_response('team_profile.html', RequestContext(request, locals()))
	if request.POST.get('applied'):
		if me.team == none_team:
			me.applied.add(team)	
			me.save()
			return render_to_response('applied_complete.html', locals())
		else:
			return HttpResponseRedirect("/permission_error/")

	if request.POST.get('quit'):
		if me.team == team:
			me.team = none_team	
			me.save()
			perm = Permission.objects.get(codename='can_create_team_profile')
			request.user.user_permissions.add(perm)
			return HttpResponseRedirect('/team_list/')
	if request.POST.get('dismiss'):
		if me.nickname == team.captain_name:
			me.team = none_team	
			me.save()
			team.delete()
			perm = Permission.objects.get(codename='can_create_team_profile')
			request.user.user_permissions.add(perm)
			return HttpResponseRedirect('/team_list/')
	return render_to_response('team_profile.html', RequestContext(request, locals()))

@permission_required('profiles.can_view_base_profile', login_url='/permission_error/')
def applied_list(request, teamid):
	me = Student.objects.get(name=request.user)
	team = Team.objects.get(id=teamid)
	if me.team == team:
		if request.POST.get('allow'):
			student = Student.objects.get(id=request.POST['allow'])
			team.applier.remove(student)
			student.team = team	
			team.save()
			student.save()
			perm = Permission.objects.get(codename='can_create_team_profile')
			user = User.objects.get(student=student)
			user.user_permissions.remove(perm)
			
		return render_to_response('applied_list.html', RequestContext(request, locals()))
	else:
		return HttpResponseRedirect("/permission_error/")

@permission_required('profiles.can_view_base_profile', login_url='/wait/')
def chatroom_list(request):
	me = Student.objects.get(name=request.user)
	chatrooms = Chatroom.objects.filter(student2=me).order_by('-date_time')
	chatrooms = list(set(chatrooms))
	return render_to_response('chatroom_list.html', locals())

