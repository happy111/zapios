from django.contrib import admin
from Brands.models import Company
from datetime import datetime
from UserRole.models import *
from django.contrib.admin import site
from django.forms.utils import ErrorList
from django import forms
from django.contrib.auth.models import User
from Configuration.admin import make_active, make_deactive


class UserTypeMasterAdmin(admin.ModelAdmin):
	# form = CompanyForm
	exclude = [
			'created_at',
			'updated_at',
			'active_status'
			]
	search_fields = [
		'user_type',
		]
	list_display = [
		  'user_type',
		  'Company',
		  'active_status',
		  'created_at',
			]
	list_filter = [
		'active_status',
		'created_at',
		'updated_at',
		'Company__company_name'
		]
	actions = [make_active, make_deactive]
	list_per_page = 10
	# list_display_links = None
	
	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_at = datetime.now()
			obj.save()
		else:
			obj.updated_at = datetime.now()
			obj.save()

	def has_delete_permission(self, request, obj=None):
		return False

	def has_add_permission(self, request, obj=None):
		return True


class ManagerProfileMasterAdmin(admin.ModelAdmin):
	# form = CompanyForm
	exclude = [
			'created_at',
			'updated_at',
			'active_status'
			]
	search_fields = [
		'username',
		# 'manager_name'
		]
	list_display = [
		  'user_type',
		  'manager_name',
		  'manager_picture',
		  'Company',
		  'active_status',
		  'created_at',
			]
	list_filter = [
		'active_status',
		'created_at',
		'updated_at',
		'Company__company_name'
		]
	actions = [make_active, make_deactive]
	list_per_page = 10
	# list_display_links = None
	
	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_at = datetime.now()
			obj.save()
		else:
			obj.updated_at = datetime.now()
			obj.save()

	def has_delete_permission(self, request, obj=None):
		return True

	def has_add_permission(self, request, obj=None):
		return False

class MainRoutingModuleMasterAdmin(admin.ModelAdmin):
	# form = CompanyForm
	exclude = [
			'created_at',
			'updated_at',
			'active_status'
			]
	search_fields = [
		'module_id',
		'module_name'
		]
	list_display = [
		  'module_id',
		  'module_name',
		  'icon',
		  'label',
		  'to',
		  'active_status',
		  'created_at',
			]
	list_filter = [
		'active_status',
		'created_at',
		'updated_at'
		]
	actions = [make_active, make_deactive]
	list_per_page = 10
	# list_display_links = None
	
	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_at = datetime.now()
			obj.save()
		else:
			obj.updated_at = datetime.now()
			obj.save()

	def has_delete_permission(self, request, obj=None):
		return False

	def has_add_permission(self, request, obj=None):
		return True

class RoutingModuleMasterAdmin(admin.ModelAdmin):
	# form = CompanyForm
	exclude = [
			'created_at',
			'updated_at',
			'active_status'
			]
	search_fields = [
	'module_name',
		]
	list_display = [
		  'main_route',
		  'module_name',
		  'icon',
		  'label',
		  'to',
		  'active_status',
		  'created_at',
			]
	list_filter = [
		'active_status',
		'created_at',
		'updated_at'
		]
	actions = [make_active, make_deactive]
	list_per_page = 10
	# list_display_links = None
	
	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_at = datetime.now()
			obj.save()
		else:
			obj.updated_at = datetime.now()
			obj.save()

	def has_delete_permission(self, request, obj=None):
		return False

	def has_add_permission(self, request, obj=None):
		return True

class SubRoutingModuleMasterAdmin(admin.ModelAdmin):
	# form = CompanyForm
	exclude = [
			'created_at',
			'updated_at',
			'active_status'
			]
	search_fields = [
		'sub_module_name'
		]
	list_display = [
		  'route',
		  'sub_module_name',
		  'icon',
		  'label',
		  'to',
		  'active_status',
		  'created_at',
			]
	list_filter = [
		'active_status',
		'created_at',
		'updated_at'
		]
	actions = [make_active, make_deactive]
	list_per_page = 10
	# list_display_links = None
	
	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_at = datetime.now()
			obj.save()
		else:
			obj.updated_at = datetime.now()
			obj.save()

	def has_delete_permission(self, request, obj=None):
		return False

	def has_add_permission(self, request, obj=None):
		return True



admin.site.register(MainRoutingModule,MainRoutingModuleMasterAdmin)
admin.site.register(RoutingModule,RoutingModuleMasterAdmin)
admin.site.register(SubRoutingModule,SubRoutingModuleMasterAdmin)

admin.site.register(UserType)

admin.site.register(RollPermission)

admin.site.register(BillRollPermission)

admin.site.register(BillingMainRoutingModule)

admin.site.register(ManagerProfile,ManagerProfileMasterAdmin)
