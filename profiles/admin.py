from django.contrib import admin
from profiles.models import Student, Interest, Badge, Team, Chatroom, up_file, file_info, Role, Teamroom, Insurance, Domain, Talent, Grade, Category, Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register your models here.

'''
# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class StudentInline(admin.StackedInline):
    model = Student
    can_delete = False
    verbose_name_plural = 'student'
# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (StudentInline, )
# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
'''
class StudentAdmin(admin.ModelAdmin):
	list_display = ('name', 'realname', 'nickname', 'department', 'team')
	

admin.site.register(Student, StudentAdmin)
admin.site.register(Interest)
admin.site.register(Badge)
admin.site.register(Team)
#admin.site.register(Follow)
admin.site.register(Chatroom)
admin.site.register(up_file)
admin.site.register(file_info)
admin.site.register(Role)
admin.site.register(Teamroom)
admin.site.register(Insurance)
admin.site.register(Domain)
admin.site.register(Talent)
admin.site.register(Grade)
admin.site.register(Category)
admin.site.register(Group)


