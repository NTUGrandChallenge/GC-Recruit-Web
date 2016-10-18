from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import staticfiles
from django.conf.urls import include, url
from django.contrib import admin
from recruitsite.views import welcome, index, register, logout, perror, use_session, complete, wait#, login#, logout
from django.contrib.auth.views import login#, logout
from django.contrib.auth.decorators import login_required
from profiles.views import list_student, profile, edit, student_create, other_profile, chatroom, upload, upload2, follow_complete, team_list, create_team, teamroom, team_profile, applied_list, search, chatroom_list, insurance_create, agree, get_file, get_file2, kick, agree2, board, activity, edit_team
from django.views.static import serve
import allauth

admin.autodiscover()
urlpatterns = [
    url(r'^$', login_required(profile)),
    url(r'^grappelli/', include('grappelli.urls')), # grappelli URLS
    url(r'^accounts/', include('allauth.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', login),
    url(r'^index/$', index),
    url(r'^accounts/logout/$', logout),
    url(r'^accounts/register/$', register),
  	url(r'^u/$', use_session),

    url(r'^static/(?P<path>.*)', serve, {'document_root':'static/img'}),

    url(r'^student_list/$', list_student),
    url(r'^my_profile/$', login_required(profile)),
    url(r'^other_profile/$', login_required(other_profile)),
    url(r'^edit_profile/$', login_required(edit)),
    url(r'^permission_error/$', perror),
    url(r'^wait/$', wait),
    url(r'^create_student/$', login_required(student_create)),
    url(r'^complete/$', complete),
    url(r'^follow_complete/$', follow_complete),
    url(r'^chatroom/(\d{1,5})/(\d{1,5})/$', login_required(chatroom)),
    url(r'^upload/$', login_required(upload)),
    url(r'^upload2/$', login_required(upload2)),

    url(r'^team_list/$', login_required(team_list)),
    url(r'^create_team/$', login_required(create_team)),
    url(r'^teamroom/(\d{1,5})/$', login_required(teamroom)),
    url(r'^team_profile/(\d{1,5})/$', login_required(team_profile)),
    url(r'^applied_list/(\d{1,5})/$', login_required(applied_list)),
    url(r'^search/$', login_required(search)),
    url(r'^chatroom_list/$', login_required(chatroom_list)),
    url(r'^insurance_create/$', login_required(insurance_create)),
    url(r'^agree/$', login_required(agree)),
    url(r'^agree2/$', login_required(agree2)),
    url(r'^get_file/$', login_required(get_file)),
    url(r'^get_file2/$', login_required(get_file2)),
    url(r'^kick/$', login_required(kick)),
    url(r'^board/(\d{1,5})/$', login_required(board)),
    url(r'^activity/(\d{1,5})/$', login_required(activity)),
    url(r'^edit_team/$', login_required(edit_team)),
    
    # url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',{'next_page': '/accounts/login'}),

    #lbforum
    url(r'^forum/', include('lbforum.urls')),
    url(r'^attachments/', include('lbattachment.urls')),
    

]
