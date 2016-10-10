from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Interest(models.Model):
	name = models.CharField(max_length=50)
	def __str__(self):
		return str(self.name)

class Domain(models.Model):
	name = models.CharField(max_length=50, blank=True)
	def __str__(self):
		return str(self.name)

class Badge(models.Model):
	name = models.CharField(max_length=50)
	content = models.CharField(max_length=1500, blank=True)
	def __str__(self):
		return self.name

class Team(models.Model):
	name = models.CharField(max_length=50, blank=True)
	captain_name = models.CharField(max_length=50, blank=True)
	interest = models.ForeignKey(Interest, null=True)
	content = models.CharField(max_length=1500, blank=True)
	class Meta:
		permissions = (
			("can_create_team_profile", "Can create team profile"),
			("can_edit_team_profile", "Can edit team profile"),
			("kicked", "Kicked")

		)
	def __str__(self):
		return self.name
class Role(models.Model):
	name = models.CharField(max_length=50)
	def __str__(self):
		return self.name

class Grade(models.Model):
	name = models.CharField(max_length=50)
	def __str__(self):
		return self.name

class Category(models.Model):
	name = models.CharField(max_length=50)
	def __str__(self):
		return self.name

class Group(models.Model):
	name = models.CharField(max_length=50)
	category = models.ForeignKey(Category, null=True)
	def __str__(self):
		return self.name

class Talent(models.Model):
	name = models.CharField(max_length=50)
	group = models.ForeignKey(Group, null=True)
	def __str__(self):
		return self.name

class Student(models.Model):
	name = models.ForeignKey(User, unique=True)
	realname = models.CharField(max_length=50, blank=True)
	nickname = models.CharField(max_length=50, blank=True)
	school = models.CharField(max_length=50, blank=True)
	department = models.CharField(max_length=50, blank=True)
	domain = models.ManyToManyField(Domain, blank=True)
	grade = models.ForeignKey(Grade, null=True)
	motto = models.CharField(max_length=600, blank=True)
	experience = models.CharField(max_length=1000, blank=True)
	email = models.CharField(max_length=50, blank=True)
	interest = models.ForeignKey(Interest, null=True)
	talent = models.ManyToManyField(Talent, blank=True)
	#talent = models.ManyToManyField(Talent, default=1 )#one student can have many badges, one badge can have many students
	badge = models.ManyToManyField(Badge, blank=True )#one student can have many badges, one badge can have many students
	role = models.ForeignKey(Role, null=True)
	team = models.ForeignKey(Team, null=True)
	follow = models.ManyToManyField('self', blank=True, symmetrical=False)
	applied = models.ManyToManyField(Team, blank=True, related_name='applier')
	class Meta:
		permissions = (
			("can_edit_base_profile", "Can edit base profile"),
			("can_view_base_profile", "Can view base profile"),
			("wait", "Wait"),
			("can_insurance", "Can insurance"),
			("can_write_student", "Can write student"),

		)
	def __str__(self):
		return self.realname

class Chatroom(models.Model):
	student1 = models.ForeignKey(Student, null=True, related_name='student1')
	student2 = models.ForeignKey(Student, null=True, related_name='student2')
	content = models.CharField(max_length=300, blank=True)
	date_time = models.DateTimeField()
	def __str__(self):
		return self.content

class up_file(models.Model):
	upload_datetime = models.DateTimeField()
	student = models.ForeignKey(Student, null=True)
	class Meta:
		permissions = (
			("can_upload", "Can upload"),
			
	)
	def __str__(self):
		return self.student.realname

class file_info(models.Model):
	File = models.ForeignKey(up_file, null=True)
	local_name = models.CharField(max_length=50)
	upload_name = models.CharField(max_length=200)
	def __str__(self):
		return self.upload_name

class Teamroom(models.Model):
	team = models.ForeignKey(Team, null=True)
	speaker = models.ForeignKey(Student, null=True)
	content = models.CharField(max_length=300, blank=True)
	date_time = models.DateTimeField()
	def __str__(self):
		return self.content

class Insurance(models.Model):
	student = models.ForeignKey(Student, null=True)
	birthday_y = models.IntegerField(default=2000)
	birthday_m = models.IntegerField(default=1)
	birthday_d = models.IntegerField(default=1)

	security_id = models.CharField(max_length=10)
	phone = models.CharField(max_length=15)
	emergency = models.CharField(max_length=50)
	emergency_relationship = models.CharField(max_length=50)
	emergency_phone = models.CharField(max_length=15)
	def __str__(self):
		return self.student.realname


