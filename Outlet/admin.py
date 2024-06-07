from django.contrib import admin
from Brands.models import Company
from datetime import datetime
from Outlet.models import *
from django.contrib.admin import site
from django.forms.utils import ErrorList
from django import forms
from django.contrib.auth.models import User
from Configuration.admin import make_active, make_deactive


def make_pos_open(modeladmin, request, queryset):
	queryset.update(is_pos_open='1',updated_at=datetime.now())
make_pos_open.short_description = "Shift Status to POS Open"


def make_pos_close(modeladmin, request, queryset):
	queryset.update(is_pos_open='0',updated_at=datetime.now())
make_pos_close.short_description = "Shift Status to POS Close"


class OutletMasterAdmin(admin.ModelAdmin):
	# form = CompanyForm
	exclude = [
			'auth_user',
			'created_at',
			'updated_at',
			'active_status'
			]
	search_fields = [
		'Outletname',
		]
	list_display = [
		  'Outletname',
		  'Company',
		  'priority',
		  'is_open',
		  'is_pos_open',
		  'is_company_active',
		  'active_status',
		  'created_at',
		  'api_key',
		  'eion_outlet_id'
			]
	# list_filter = [
	# 	'active_status',
	# 	'is_company_active',
	# 	'is_open',
	# 	'created_at',
	# 	'updated_at',
	# 	'Company__company_name'
	# 	]

	# actions = [make_active, make_deactive, make_pos_open,make_pos_close]
	# list_per_page = 10
	# ordering = ('priority',)
	# readonly_fields = ['Company','Outletname',\
	# 			'address','latitude','longitude',\
	# 			'is_pos_open','is_company_active','opening_time',\
	# 			'closing_time','check_list']
	# list_display_links = None
	
	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_at = datetime.now()
			obj.save()
		else:
			obj.updated_at = datetime.now()
			obj.save()

	def has_delete_permission(self, request, obj=None):
		print("3333333333333333333",obj)
		return True

	def has_add_permission(self, request, obj=None):
		return False


class OutletMilesRulesMasterAdmin(admin.ModelAdmin):
	# form = InstaOutletForm
	exclude = ['active_status']
	list_filter = ['active_status','Company__company_name']
	# search_fields = ['email','username']
	list_display = ['rule_name','unloaded_miles','Company','active_status','created_at','updated_at']
	
	actions = [make_active, make_deactive]
	
	readonly_fields = ['updated_at']


	list_per_page = 5

	# change_form_template = 'custom_form_outlet.html'

	def has_add_permission(self, request, obj=None):
		return True

	def has_delete_permission(self, request, obj=None):
			return False

	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_at = datetime.now()
		else:
			obj.updated_at = datetime.now()
		obj.save()


class DeliveryBoyAdmin(admin.ModelAdmin):
	# form = InstaOutletForm
	exclude = ['active_status']
	list_filter = ['active_status','is_assign']
	search_fields = ['email','name']
	list_display = ['name','outlet','email','mobile','address','is_assign','active_status']

	readonly_fields = ['updated_at']


	list_per_page = 5
	list_display_links = None

	# change_form_template = 'custom_form_outlet.html'

	def has_add_permission(self, request, obj=None):
		return False

	def has_delete_permission(self, request, obj=None):
			return False

	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_at = datetime.now()
		else:
			obj.updated_at = datetime.now()
		obj.save()

admin.site.register(OutletProfile,OutletMasterAdmin)
admin.site.register(OutletMilesRules,OutletMilesRulesMasterAdmin)
admin.site.register(DeliveryBoy,DeliveryBoyAdmin)



