# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from profiles.models import Student, Interest, Chatroom, Team, Badge, up_file, file_info, Teamroom, Role, Insurance, Domain, Talent, Grade, Category, Group
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone
import shutil, os, allauth
from django.contrib.auth.models import Permission, User
import urllib

@permission_required('profiles.can_view_base_profile', login_url='/wait/')
def search(request):
	first_user_list = Student.objects.all()
	category_all = Category.objects.all()
	group_all = Group.objects.all()
	word = False
	search = False
	if 'word' in request.GET:
		word = True
		student_list = []
		keyword = request.GET['word']
		if not keyword:
			return HttpResponseRedirect('/search/')
		else:
			students = Student.objects.filter(realname__icontains = keyword)
			students2 = Student.objects.filter(nickname__icontains = keyword)

			for each in students:
				student_list.append(each)
			for each in students2:
				student_list.append(each)
			student_list = list(set(student_list))
			slen = len(student_list)
			return render_to_response('search.html', RequestContext(request, locals()))
	if 'search' in request.GET:
		search = True
		interests = request.GET.getlist("interest[]")
		roles = request.GET.getlist("role[]")
		categorys = request.GET.getlist("category[]")
		groups = request.GET.getlist("group[]")
		interest_list = []
		role_list = []
		category_list = []
		group_list = []
		talent_list = []
		#user_list = []
		for interest in interests:
			students = Student.objects.filter(interest_id=interest)
			for each in students:
				interest_list.append(each)
#-------interest OR role search------
		for role in roles:#OR search
			students = Student.objects.filter(role_id=role)
			for each in students:
				role_list.append(each)
				##
		for category in categorys:
			mycategory = Category.objects.get(name=category)
			for group in mycategory.group_set.all():
				mygroup = Group.objects.get(name=group)
				for talent in mygroup.talent_set.all():
					students = Student.objects.filter(talent=talent)
					talent_list = list(set(talent_list).union(set(students)))

		for group in groups:
			mygroup = Group.objects.get(name=group)
			for talent in mygroup.talent_set.all():
				students = Student.objects.filter(talent=talent)
				talent_list = list(set(talent_list).union(set(students)))
				##  AND
		#student_list = list(set(interest_list).intersection(set(role_list)))
		#student_list = list(set(talent_list).intersection(set(student_list)))
				##
				##  OR
		student_list = list(set(interest_list).union(set(role_list)))
		student_list = list(set(talent_list).union(set(student_list)))
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
		slen = len(student_list)
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
	if request.user.has_perm('profiles.kicked'):
		return HttpResponseRedirect('/kick/')
	student = Student.objects.get(name=request.user)
	if request.user.socialaccount_set.first() != None:
		facebook_id = request.user.socialaccount_set.first().uid
	#students = Student.objects.all()
	return render_to_response('my_profile.html', RequestContext(request, locals()))

#@permission_required('profiles.can_edit_base_profile', login_url='/permission_error/')
@permission_required('profiles.wait', login_url='/wait/')
def edit(request):
	student = Student.objects.get(name=request.user)
	interest = Interest.objects.all()
	role = Role.objects.all()
	categorys = Category.objects.all()
	groups = Group.objects.all()
	talents = Talent.objects.all()
	mytalents = Talent.objects.filter(student=student)
	number = len(mytalents)
	counters = list(range(number,6))
	if request.POST:
		motto = request.POST['motto']
		experience = request.POST['experience']
		experience =experience.replace("\n","<br>")
		myinterest = request.POST['interest']
		myrole = request.POST['role']

		talent = request.POST.getlist("talent[]")
		
		student.motto = motto
		student.experience = experience
		student.interest = Interest.objects.get(name=myinterest)
		student.role = Role.objects.get(name=myrole)
		for clean in mytalents:
			student.talent.remove(clean)
		for item in talent:
			student.talent.add(Talent.objects.get(name=item))
		student.save()
		return HttpResponseRedirect('/my_profile/')
	else:
		return render_to_response('edit_profile.html', RequestContext(request, locals()))

def agree(request):
	if request.user.has_perm('profiles.can_write_student'):
		return HttpResponseRedirect('/create_student/')
	if 'agree' in request.POST:
		perm = Permission.objects.get(codename='can_write_student')
		request.user.user_permissions.add(perm)
		return HttpResponseRedirect('/create_student/')
	if 'no' in request.POST:
		return HttpResponseRedirect('/index/')
	return render_to_response('agree.html', RequestContext(request, locals()))


def student_create(request):
	interests = Interest.objects.all()
	roles = Role.objects.all()
	domains = Domain.objects.all()
	grades = Grade.objects.all()
	categorys = Category.objects.all()
	groups = Group.objects.all()
	talents = Talent.objects.all()
	counters = list(range(1,7))


	if request.user.has_perm('profiles.can_insurance'):
		return HttpResponseRedirect('/insurance_create/')
	errors = []
	# inter = Interest.objects.all()
	if request.POST:
		name = request.user
		realname = request.POST['realname']
		nickname = request.POST['nickname']
		school = request.POST['school']
		department = request.POST['department']
		grade = request.POST['grade']
		motto = request.POST['motto']
		experience = request.POST['experience']
		email = request.POST['email']
		none_team = Team.objects.get(name='none')
		interest = request.POST['interest']
		role = request.POST['role']

		talent = request.POST.getlist('talent[]')
		domain = request.POST.getlist('domain[]')
		talent = list(set(talent))
		
#		if any(not request.POST[k] for k in request.POST):
#			errors.append('* 有空白欄位！請不要留空！')
		if not errors:
			student = Student.objects.create(
				name=name,
				realname = realname,
				nickname = nickname,
				school = school,
				department = department,
				motto = motto,
				email = email,
				experience = experience,
				team = none_team,
				grade = Grade.objects.get(name=grade),
				interest = Interest.objects.get(name=interest),
				role = Role.objects.get(name=role)
			)
			
			for item in talent:
				student.talent.add(Talent.objects.get(name=item))
			for item2 in domain:
				student.domain.add(Domain.objects.get(name=item2))
			student.save()
			#student.talent.set(mytalent)
			#student.domain.set(mydomain)
			perm = Permission.objects.get(codename='can_insurance')
			request.user.user_permissions.add(perm)
			return HttpResponseRedirect('/insurance_create/')
		return render_to_response('insurance.html', RequestContext(request, locals()))
	else:
		return render_to_response('create_student.html', RequestContext(request, locals()))

def check(y,m,d):
	
	if (y % 4) == 0:
		if m == 2:
			if d > 29:
				return False
		elif m in [4,6,9,11]:
			if d ==31:
				return False
	else:
		if m == 2:
			if d > 28:
				return False
		elif m in [4,6,9,11]:
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
			to = '/'
			return render_to_response('complete.html', RequestContext(request, locals()))
	return render_to_response('insurance.html', RequestContext(request, locals()))

@permission_required('profiles.can_view_base_profile', login_url='/wait/')
def chatroom(request, idfrom, idto):
	me = Student.objects.get(name=request.user)
	s1=Student.objects.get(id=idfrom)
	s2=Student.objects.get(id=idto)
	if me in [s1, s2]:
		chatroom1 = Chatroom.objects.filter(student1=s1, student2=s2)
		chatroom2 = Chatroom.objects.filter(student1=s2, student2=s1)
		chatroom = (chatroom1 | chatroom2).order_by('date_time')
		# for each in chatroom:
		# 	each.content = each.content.replace("/n","<br>")
		if request.POST:
			content = request.POST['content']
			content =content.replace("\n","<br>")
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
	else:
		error_msg = 'NO_ACCESS'
		return render_to_response('permission_error.html', RequestContext(request, locals()))

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
		myid = request.user.student_set.first().id
		user = User.objects.get(student=student)
		me = Student.objects.get(name=request.user)
		student = Student.objects.get(id=request.GET['follow'])
		me.follow.add(student)	
		me.save()
		return render_to_response('other_profile.html', RequestContext(request, locals()))
	if request.GET.get('cancel'):
		myid = request.user.student_set.first().id
		user = User.objects.get(student=student)
		me = Student.objects.get(name=request.user)
		student = Student.objects.get(id=request.GET['cancel'])
		me.follow.remove(student)	
		me.save()
		return render_to_response('other_profile.html', RequestContext(request, locals()))
	else:
		return HttpResponseRedirect("/search/")

@permission_required('profiles.can_view_base_profile', login_url='/wait/')
@permission_required('profiles.can_upload', login_url='/agree2/')
def upload(request):
	s1=Student.objects.get(id=request.user.student_set.first().id)
	if request.method == 'POST':# request.POST.get 如果沒有request到資料時會丟回None
		date = timezone.localtime(timezone.now())
        # 存入資料庫
		form = up_file(upload_datetime = date, student = s1) 
		form.save()
		files = request.FILES.getlist('file') #抓取檔案(可能多個檔案)
		if len(files) > 0:
			try:
				file_dir = os.path.join('/home/ubuntu/upload' , str(form.student.name))
				file_dir2 = file_dir
                #如果路徑中的檔案夾不存在就建立一個新的
				if not os.path.exists(file_dir):
					os.makedirs(file_dir) 
				counter = 0
				for file in files:
					if counter == 0:
	               	    #為了避免檔案名稱重複，因此存在server端時，把修改檔案名稱
						local_name = '1'#timezone.now().strftime('%Y%m%d%H%M%S')
						file_path = os.path.join(file_dir, local_name)
	               		    #存入資料庫
						file_info.objects.create(
								File = up_file.objects.get(id=form.pk),
								local_name = local_name, #存在server檔名
								upload_name = file.name #原本檔名
								)
					# 開始讀寫檔案至server
	    #              'b' 如果檔案存在就會被覆蓋
						destination =open(file_path,'wb+')
						for chunk in file.chunks():
							destination.write(chunk)
							destination.close()
					if counter == 1:
						local_name = '2'
						file_path2 = os.path.join(file_dir2, local_name)
						file_info.objects.create(
								File = up_file.objects.get(id=form.pk),
								local_name = local_name, #存在server檔名
								upload_name = file.name #原本檔名
								)
						destination =open(file_path2,'wb+')
						for chunk in file.chunks():
							destination.write(chunk)
							destination.close()
					counter = counter + 1
			except:
					pass
			# 		shutil.rmtree(file_dir, True)   #發生例外，就刪除路徑檔案
		return HttpResponseRedirect('/team_list/')
	return render_to_response('upload.html', RequestContext(request, locals()))

@permission_required('profiles.can_view_base_profile', login_url='/wait/')
@permission_required('profiles.can_upload', login_url='/agree2/')
def upload2(request):
	error_msg = 'UPLOAD_FAILED'
	return render_to_response('permission_error.html', RequestContext(request, locals()))

@permission_required('profiles.can_view_base_profile', login_url='/wait/')
def get_file (request):
	try:
		file_dir = os.path.join('/home/ubuntu/upload' , str(request.user)) 	
		file_path = os.path.join( file_dir , '1')
		f=open(file_path,'rb')
		data=f.read()   #開始讀寫檔案至data變數裡面
		f.close()
		# content_type有很多種，有強制下載轉乘PDF的、有ZIP的，我就用force-download
		response = HttpResponse(data , content_type='application/pdf')
		#要import urllib
		#檔案原本名稱.encode("utf-8") 記得要換回檔案原本的名稱，轉成utf-8格式以免亂碼
		#不是存在service端的檔案名稱唷！
		response['Content-Disposition'] = 'attachment; filename=1.pdf'# % urllib.quote( '1'.encode("utf-8") )
		return response
	except:
		return HttpResponse('error to download file')

@permission_required('profiles.can_view_base_profile', login_url='/wait/')
def get_file2 (request):
	try:
		file_dir = os.path.join('/home/ubuntu/upload' , str(request.user)) 	
		file_path = os.path.join( file_dir , '2')
		f=open(file_path,'rb')
		data=f.read()   #開始讀寫檔案至data變數裡面
		f.close()
		# content_type有很多種，有強制下載轉乘PDF的、有ZIP的，我就用force-download
		response = HttpResponse(data , content_type='application/pdf')
		#要import urllib
		#檔案原本名稱.encode("utf-8") 記得要換回檔案原本的名稱，轉成utf-8格式以免亂碼
		#不是存在service端的檔案名稱唷！
		response['Content-Disposition'] = 'attachment; filename=2.pdf'# % urllib.quote( '1'.encode("utf-8") )
		return response
	except:
		return HttpResponse('error to download file')


def follow_complete(request):
	return render_to_response('follow_complete.html', locals())

@permission_required('profiles.can_view_base_profile', login_url='/wait/')
def team_list(request):
	students = Student.objects.all()
	teams = Team.objects.all()
	news = Team.objects.filter(captain_name='postgres')
	teams = list(set(teams).difference(set(news)))

	word = False
	search = False
	if 'word' in request.GET:
		word = True
		keyword = request.GET['word']
		if not keyword:
			return HttpResponseRedirect('/team_list/')
		else:
			teams = Team.objects.filter(name__icontains = keyword)

			slen = len(teams)
			return render_to_response('team_list.html', RequestContext(request, locals()))
	if 'search' in request.GET:
		search = True
		interests = request.GET.getlist("interest[]")
		teams = []
		for interest in interests:
			interest_list = Team.objects.filter(interest_id=interest)
			for each in interest_list:
				teams.append(each)
				
		slen = len(teams)
		return render_to_response('team_list.html', RequestContext(request, locals()))
	return render_to_response('team_list.html', RequestContext(request, locals()))

@permission_required('profiles.can_create_team_profile', login_url='/permission_error/')
def create_team(request):
	errors = []
	interests = Interest.objects.all()
	if request.POST:
		student = request.user.student_set.first()
		teamname = request.POST['teamname']
		content = request.POST['content']
		content =content.replace("\n","<br>")
		team_interest = request.POST['interest']
		captain_name = student.name
		if any(not request.POST[k] for k in request.POST):
			errors.append('* 有空白欄位！請不要留空！')
		if not errors:
			t = Team.objects.create(
				name=teamname,
				captain_name=captain_name,
				interest = Interest.objects.get(name=team_interest),
				content = content
			)
			student.team = t
			perm = Permission.objects.get(codename='can_create_team_profile')
			request.user.user_permissions.remove(perm)
			student.save()
			to = '/team_profile/' + str(t.id)
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
		content =content.replace("\n","<br>")
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
			return render_to_response('team_profile.html', RequestContext(request, locals()))
		else:
			error_msg = 'NO_ACCESS'
			return render_to_response('permission_error.html', RequestContext(request, locals()))

	if request.POST.get('quit'):
		if me.team == team:
			me.team = none_team
			me.save()
			perm = Permission.objects.get(codename='can_create_team_profile')
			request.user.user_permissions.add(perm)
			return HttpResponseRedirect('/team_list/')
	if request.POST.get('dismiss'):
		if me.name.username == team.captain_name :
			if len(team.student_set.all()) == 1:
				me.team = none_team	
				me.save()
				team.delete()
				perm = Permission.objects.get(codename='can_create_team_profile')
				request.user.user_permissions.add(perm)
				return HttpResponseRedirect('/team_list/')
			else:
				error_msg = 'MORE_THAN_ONE_MEMBER'
				return render_to_response('permission_error.html', RequestContext(request, locals()))

	if request.POST.get('cancel'):
		if me.team != team:
			me.applied.remove(team)	
			me.save()
			return render_to_response('team_profile.html', RequestContext(request, locals()))
	if request.POST.get('kick') and me.name.username == team.captain_name :
		student = Student.objects.get(id=request.POST['kick'])
		if student.team == team:
			student.team = none_team	
			student.save()
			perm = Permission.objects.get(codename='can_create_team_profile')
			user = User.objects.get(student=student)
			user.user_permissions.add(perm)
			perm = Permission.objects.get(codename='kicked')
			user.user_permissions.add(perm)
			user.save()
			return render_to_response('team_profile.html', RequestContext(request, locals()))
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
		error_msg = 'NO_ACCESS'
		return render_to_response('permission_error.html', RequestContext(request, locals()))

@permission_required('profiles.can_view_base_profile', login_url='/wait/')
def chatroom_list(request):
	me = Student.objects.get(name=request.user)
	chatroom1 = Chatroom.objects.filter(student1=me)
	chatrooms = Chatroom.objects.filter(student2=me)
	chatroom_all = (chatroom1 | chatrooms).order_by('-date_time')
	
	s_list = []
	c_list = []
	for chatroom in chatrooms:
		if chatroom not in c_list and chatroom.student1 not in s_list:
			c_list.append(chatroom)
			s_list.append(chatroom.student1)
	chatrooms = c_list

	s_list2 = [me,]
	c_list2 = []
	for chatroom in chatroom_all:
		if chatroom not in c_list2 and chatroom.student1 not in s_list2:
			c_list2.append(chatroom)
			s_list2.append(chatroom.student1)
	for chatroom in chatroom_all:
		if chatroom not in c_list2 and chatroom.student2 not in s_list2:
			c_list2.append(chatroom)
			s_list2.append(chatroom.student2)
	chatroom_all = c_list2


	return render_to_response('chatroom_list.html', locals())

@permission_required('profiles.can_view_base_profile', login_url='/wait/')
def kick(request):
	if 'agree' in request.POST:
		perm = Permission.objects.get(codename='kicked')
		request.user.user_permissions.remove(perm)
		return HttpResponseRedirect('/my_profile/')
	return render_to_response('kick.html', RequestContext(request, locals()))

@permission_required('profiles.can_view_base_profile', login_url='/wait/')
def agree2(request):
	if request.user.has_perm('profiles.can_upload'):
		return HttpResponseRedirect('/upload/')
	if 'agree' in request.POST:
		perm = Permission.objects.get(codename='can_upload')
		request.user.user_permissions.add(perm)
		return HttpResponseRedirect('/upload/')
	if 'no' in request.POST:
		return HttpResponseRedirect('/index/')
	return render_to_response('agree2.html', RequestContext(request, locals()))

@permission_required('profiles.can_view_base_profile', login_url='/wait/')
def board(request,teamid):
	me = Student.objects.get(name=request.user)
	team = Team.objects.get(id=teamid)
	#board = team.teamroom_set.first()
	teamroom = team.teamroom_set.order_by('date_time')
	#teamroom = list(set(teamrooma).difference(set(board)))
	member = True
	if request.POST:
		content = request.POST['content']
		date_time = timezone.localtime(timezone.now())
		Teamroom.objects.create(
			team=team,
			speaker=me,
			content=content,
			date_time=date_time
		)
	return render_to_response('board.html', RequestContext(request, locals()))

@permission_required('profiles.can_view_base_profile', login_url='/wait/')
def activity(request, badgeid):
	me = Student.objects.get(name=request.user)
	badge = Badge.objects.get(id=badgeid)
	if request.POST.get('id'):
		return render_to_response('activity.html', RequestContext(request, locals()))
	if request.POST.get('applied'):
		me.badge.add(badge)	
		me.save()
		return render_to_response('activity.html', RequestContext(request, locals()))	
	if request.POST.get('cancel'):
		me.badge.remove(badge)	
		me.save()
		return render_to_response('activity.html', RequestContext(request, locals()))	
	return render_to_response('activity.html', RequestContext(request, locals()))

@permission_required('profiles.can_view_base_profile', login_url='/permission_error/')
def edit_team(request):
	student = Student.objects.get(name=request.user)
	team = student.team
	if request.POST:
		content = request.POST['content']
		team.content = content
		team.save()
		return HttpResponseRedirect('/team_profile/' + str(team.id))
	else:
		return render_to_response('edit_team.html', RequestContext(request, locals()))

@permission_required('profiles.can_view_base_profile', login_url='/wait/')
def follow_list(request):
	me = request.user.student_set.first()
	follow_list = me.follow.all()
	return render_to_response('follow_list.html', RequestContext(request, locals()))

@permission_required('profiles.can_edit_team_profile', login_url='/wait/')
def statical(request):
	students = Student.objects.all()
	return render_to_response('static.html', RequestContext(request, locals()))



