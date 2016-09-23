from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import staticfiles
from django.conf.urls import include, url
from django.contrib import admin
from recruitsite.views import welcome, index, register, logout, perror, use_session, complete, wait#, login#, logout
from django.contrib.auth.views import login#, logout
from django.contrib.auth.decorators import login_required
from profiles.views import list_student, profile, edit, student_create, other_profile, chatroom, upload, follow_complete, list_team, create_team, teamroom, team_profile, applied_list, search
from django.views.static import serve
import allauth

admin.autodiscover()
urlpatterns = [
    url(r'^$', index),
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
    url(r'^team_list/$', login_required(list_team)),
    url(r'^create_team/$', login_required(create_team)),
    url(r'^teamroom/(\d{1,5})/$', login_required(teamroom)),
    url(r'^team_profile/(\d{1,5})/$', login_required(team_profile)),
    url(r'^applied_list/(\d{1,5})/$', login_required(applied_list)),
    url(r'^search/$', login_required(search)),


]
