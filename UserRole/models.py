from django.db import models
from django.contrib.auth.models import User
from Brands.models import Company
from django.contrib.postgres.fields import ArrayField,JSONField
from Outlet.models import *


class UserType(models.Model):
	Company = models.ForeignKey(
		Company, 
		related_name='UserType_Company',
		on_delete=models.CASCADE,
		verbose_name='Company',
		limit_choices_to={'active_status':'1'}) 
	user_type = models.CharField(
		max_length=100, 
		verbose_name='User Type', 
		null=True, 
		blank=True)
	active_status = models.BooleanField(
		default=0, 
		verbose_name='Is Active')
	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(
		blank=True, 
		null=True,
		verbose_name='Updation Date & Time')

	class Meta:
		verbose_name = 'User Type'
		verbose_name_plural = '       User Type'

	def __str__(self):
		return self.user_type


class ManagerProfile(models.Model):
	auth_user = models.OneToOneField(
		User, 
		on_delete=models.CASCADE,
		related_name='ManagerProfile_auth_user', 
		null=True,
		blank=True)
	login_type = ArrayField(
		models.TextField(),
		null=True, 
		blank=True, 
		verbose_name="Login Type")
	outlet = ArrayField(
		models.TextField(),
		null=True, 
		blank=True, 
		verbose_name="Outlet Mapped Ids")
	Company = models.ForeignKey(
		Company, 
		related_name='ManagerProfile_Company',
		on_delete=models.CASCADE,
		verbose_name='Company',
		limit_choices_to={'active_status':'1'})
	user_type = models.ForeignKey(
		UserType, 
		related_name='ManagerProfile_UserType',
		on_delete=models.CASCADE,
		verbose_name='User Type',
		limit_choices_to={'active_status':'1'},
		null=True,
		blank=True)
	username = models.CharField(
		max_length=100, 
		verbose_name='User Name')
	employee_id = models.CharField(
		max_length=100, 
		verbose_name='Employee ID',
		null=True, 
		blank=True)
	manager_name =  models.CharField(
		max_length=100, 
		verbose_name='First Name')
	last_name =  models.CharField(
		max_length=100, 
		null=True,
		blank=True,
		verbose_name='last Name')
	email = models.EmailField(
		max_length=100, 
		verbose_name='Email Id', 
		unique=True,
		null=True,
		blank=True)
	manager_pic = models.ImageField(
		upload_to='manager_profile',
		null=True, 
		blank=True, 
		verbose_name='Profile Pic')
	password = models.CharField(
		max_length=20,
		verbose_name='Password')
	active_status = models.BooleanField(
		default=1, 
		verbose_name='Is Active')
	is_attandance = models.BooleanField(
		default=0, 
		verbose_name='Is Attandance')
	is_rider = models.BooleanField(
		default=0, 
		verbose_name='Is Rider')
	is_assign = models.BooleanField(
		default=0, 
		verbose_name='Is Rider')
	is_firstUser = models.BooleanField(
		default=0,
		blank=True, 
		null=True, 
		verbose_name='is_firstUser')
	mobile = models.CharField(
		max_length=20,
		verbose_name='Mobile',
		null=True,
		blank=True)
	km = models.CharField(
		max_length=20,
		verbose_name='Kiolmeter',
		null=True,
		blank=True)
	compensation = models.CharField(
		max_length=20,
		verbose_name='compensation',
		null=True,
		blank=True)
	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(
		blank=True, 
		null=True,
		verbose_name='Updation Date & Time')
	is_hide = models.BooleanField(
		default=0, 
		verbose_name='Is Hide')
	class Meta:
		verbose_name = 'Manager Profile'
		verbose_name_plural = '      Manager Profiles'

	def __str__(self):
		return self.username


	def manager_picture(self):
		if self.manager_pic:
			return mark_safe('<img src='+MEDIA_URL+'%s width="50" height="50" />' % (self.manager_pic))
			manager_picture.allow_tags = True
		else:
			return 'No Image'
	manager_picture.short_description = 'Profile Picture'



class MainRoutingModule(models.Model):
	module_id = models.CharField(
		max_length=100, 
		verbose_name='Module Id', 
		unique=True)
	module_name = models.CharField(
		max_length=100, 
		verbose_name='Main Module Name', 
		unique=True,
		blank=True, 
		null=True)
	icon = models.CharField(
		max_length=100, 
		verbose_name='Icon')
	label = models.CharField(
		max_length=100, 
		verbose_name='Label')
	to = 	models.CharField(
		max_length=100, 
		verbose_name='Url Path')
	component = models.CharField(
		max_length=100, 
		verbose_name='Component',
		blank=True, 
		null=True)
	priority = models.PositiveIntegerField(
		null=True, 
		blank=True, 
		verbose_name='Priority')
	active_status = models.BooleanField(
		default=1, 
		verbose_name='Is Active')
	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(
		blank=True, 
		null=True,
		verbose_name='Updation Date & Time')

	class Meta:
		verbose_name = 'Main-Module Routing'
		verbose_name_plural = '     Main-Module Routing'

	def __str__(self):
		return self.module_name


class RoutingModule(models.Model):
	main_route = models.ForeignKey(
		MainRoutingModule, 
		related_name='RoutingModule_MainRoutingModule',
		on_delete=models.CASCADE,
		verbose_name='Main Module',
		limit_choices_to={'active_status':'1'})
	module_name = models.CharField(
		max_length=100, 
		verbose_name='Module Name', 
		unique=True,
		blank=True, 
		null=True)
	icon = models.CharField(
		max_length=100, 
		verbose_name='Icon')
	label = models.CharField(
		max_length=100, 
		verbose_name='Label')
	to = 	models.CharField(
		max_length=100, 
		verbose_name='Url Path')
	component = models.CharField(
		max_length=100, 
		verbose_name='Component',
		blank=True, 
		null=True)
	priority = models.PositiveIntegerField(
		null=True, 
		blank=True,
		verbose_name='Priority')
	active_status = models.BooleanField(
		default=1, 
		verbose_name='Is Active')
	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(
		blank=True, 
		null=True,
		verbose_name='Updation Date & Time')

	class Meta:
		verbose_name = 'Module Routing'
		verbose_name_plural = '    Module Routing'

	def __str__(self):
		return self.label+' | '+str(self.main_route)


class SubRoutingModule(models.Model):
	route = models.ForeignKey(
		RoutingModule, 
		related_name='SubRoutingModule_RoutingModule',
		on_delete=models.CASCADE,
		verbose_name='Module',
		limit_choices_to={'active_status':'1'})
	sub_module_name = models.CharField(
		max_length=100, 
		verbose_name='Sub-Module Name', 
		unique=True,
		blank=True,
		null=True)
	icon = models.CharField(
		max_length=100, 
		verbose_name='Icon')
	label = models.CharField(
		max_length=100, 
		verbose_name='Label')
	to = models.CharField(
		max_length=100, 
		verbose_name='Url Path')
	component = models.CharField(
		max_length=100, 
		verbose_name='Component',
		blank=True, 
		null=True)
	priority = models.PositiveIntegerField(
		null=True, 
		blank=True, 
		verbose_name='Priority')
	active_status = models.BooleanField(
		default=1, 
		verbose_name='Is Active')
	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(
		blank=True, 
		null=True,
		verbose_name='Updation Date & Time')

	class Meta:
		verbose_name = 'Sub-Module Routing'
		verbose_name_plural = '   Sub-Module Routing'

	def __str__(self):
		return self.icon +' | '+self.label


class UserTypeAuthorization(models.Model):
	UserType = models.ForeignKey(
		UserType, 
		related_name='UserType_Auth',
		on_delete=models.CASCADE,
		verbose_name='User Type',
		limit_choices_to={'active_status':'1'},
		blank=True, 
		null=True)
	main_route = ArrayField(
		models.TextField(),
		null=True, 
		blank=True, 
		verbose_name="Main Route Ids")
	route = ArrayField(
		models.TextField(),
		null=True, 
		blank=True, 
		verbose_name="Route Ids")
	subroute = ArrayField(
		models.TextField(),
		null=True, 
		blank=True, 
		verbose_name="Sub Route Ids")
	action_granted = JSONField(
		blank=True,
		null=True,
		verbose_name="Action Granted")
	active_status = models.BooleanField(
		default=1, 
		verbose_name='Is Active')
	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(
		blank=True, 
		null=True,
		verbose_name='Updation Date & Time')

	class Meta:
		verbose_name = 'User Type Authorization'
		verbose_name_plural = '   User Type Authorization'

	def __int__(self):
		return self.UserType


class RollPermission(models.Model):
	user_type = models.ForeignKey(
		UserType, 
		related_name='RollPermission_UserType',
		on_delete=models.CASCADE,
		verbose_name='User Type',
		limit_choices_to={'active_status':'1'},
		null=True,blank=True)
	main_route = models.ForeignKey(
		MainRoutingModule, 
		related_name='RollPermission_main_route',
		on_delete=models.CASCADE,
		verbose_name='Main Module',
		limit_choices_to={'active_status':'1'})
	label = models.BooleanField(
		default=0, 
		verbose_name='Label')
	company = models.ForeignKey(
		Company, 
		related_name='RollPermission_Company',
		on_delete=models.CASCADE,
		verbose_name='Company')

	active_status = models.BooleanField(
		default=1, 
		verbose_name='Is Active')
	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(
		blank=True, 
		null=True,
		verbose_name='Updation Date & Time')

	class Meta:
		verbose_name = 'RollPermission'
		verbose_name_plural = '    RollPermission'

	def __str__(self):
		return str(self.label)



#  Billing Module Integrate

class BillingMainRoutingModule(models.Model):
	module_id = models.CharField(
		max_length=100,
		null=True, 
		blank=True, 
		verbose_name='Module Id',)
	module_name = models.CharField(
		max_length=100, 
		null=True, 
		blank=True,
		verbose_name='Main Module Name', 
		unique=True)
	icon = models.CharField(
		max_length=100,
		null=True, 
		blank=True, 
		verbose_name='Icon')
	label = models.CharField(
		max_length=100, 
		null=True, 
		blank=True,
		verbose_name='Label')
	to = 	models.CharField(
		max_length=100,
		null=True, 
		blank=True, 
		verbose_name='Url Path')
	component = models.CharField(
		max_length=100,
		null=True, 
		blank=True, 
		verbose_name='Component')
	priority = models.PositiveIntegerField(
		null=True, 
		blank=True, 
		verbose_name='Priority')
	active_status = models.BooleanField(
		default=1, 
		verbose_name='Is Active')
	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(
		blank=True, 
		null=True,
		verbose_name='Updation Date & Time')

	class Meta:
		verbose_name = 'Main-Module Routing'
		verbose_name_plural = '     Main-Module Routing'

	def __str__(self):
		return self.module_name


class BillingRoutingModule(models.Model):
	main_route = models.ForeignKey(
		BillingMainRoutingModule, 
		related_name='BillingRoutingModule_MainRoutingModule',
		on_delete=models.CASCADE,
		verbose_name='Main Module',
		limit_choices_to={'active_status':'1'})
	module_name = models.CharField(
		max_length=100, 
		verbose_name='Module Name', 
		blank=True, null=True)
	icon = models.CharField(
		max_length=100, 
		null=True, 
		blank=True,
		verbose_name='Icon')
	label = models.CharField(
		max_length=100,
		null=True, 
		blank=True, 
		verbose_name='Label')
	to = 	models.CharField(
		max_length=100,
		null=True, 
		blank=True, 
		verbose_name='Url Path')
	component = models.CharField(
		max_length=100,
		verbose_name='Component',
		blank=True, 
		null=True)
	priority = models.PositiveIntegerField(
		null=True, 
		blank=True, 
		verbose_name='Priority')
	active_status = models.BooleanField(
		default=1, 
		verbose_name='Is Active')
	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(
		blank=True, 
		null=True,
		verbose_name='Updation Date & Time')

	class Meta:
		verbose_name = 'Module Routing'
		verbose_name_plural = '    Module Routing'

	def __str__(self):
		return self.label+' | '+str(self.main_route)


class BillingSubRoutingModule(models.Model):
	route = models.ForeignKey(
		BillingRoutingModule, 
		related_name='BillingSubRoutingModule_RoutingModule',
		on_delete=models.CASCADE,
		verbose_name='Module',
		limit_choices_to={'active_status':'1'})
	sub_module_name = models.CharField(
		max_length=100, 
		verbose_name='Sub-Module Name', 
		unique=True,
		blank=True,
		null=True)
	icon = models.CharField(
		max_length=100, 
		verbose_name='Icon',
		null=True, 
		blank=True,)
	label = models.CharField(
		max_length=100, 
		verbose_name='Label',
		null=True, 
		blank=True,)
	to = 	models.CharField(
		max_length=100, 
		verbose_name='Url Path',
		null=True, 
		blank=True,)
	component = models.CharField(
		max_length=100, 
		verbose_name='Component',
		blank=True, 
		null=True)
	priority = models.PositiveIntegerField(
		null=True, 
		blank=True, 
		verbose_name='Priority')
	active_status = models.BooleanField(
		default=1, 
		verbose_name='Is Active')
	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(
		blank=True, 
		null=True,
		verbose_name='Updation Date & Time')

	class Meta:
		verbose_name = 'Sub-Module Routing'
		verbose_name_plural = '   Sub-Module Routing'

	def __str__(self):
		return self.icon +' | '+self.label


class BillRollPermission(models.Model):
	user_type = models.ForeignKey(
		UserType, 
		related_name='BillRollPermission_UserType',
		on_delete=models.CASCADE,
		verbose_name='User Type',
		limit_choices_to={'active_status':'1'},
		null=True,blank=True)
	
	main_route = models.ForeignKey(
		BillingMainRoutingModule, 
		related_name='BillRollPermission_main_route',
		on_delete=models.CASCADE,
		verbose_name='Main Module',
		limit_choices_to={'active_status':'1'})
	
	company = models.ForeignKey(Company, 
		related_name='BillRollPermission_Company',
		on_delete=models.CASCADE,
		verbose_name='Company')
	label = models.BooleanField(
		default=0, 
		verbose_name='Label',
		null=True, 
		blank=True,)
	active_status = models.BooleanField(
		default=1,
		null=True, 
		blank=True, 
		verbose_name='Is Active')
	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(
		blank=True, 
		null=True,
		verbose_name='Updation Date & Time')

	class Meta:
		verbose_name = 'BillRollPermission'
		verbose_name_plural = '    BillRollPermission'

	def __str__(self):
		return str(self.label)

