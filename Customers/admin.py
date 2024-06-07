from django.contrib import admin
from django.db.models import Q
from Customers.models import CustomerProfile, customer_otp
import datetime

# Register your models here.

def make_active(modeladmin, request, queryset):
	queryset.update(active_status='1',updated_at=datetime.datetime.now())
make_active.short_description = "Move Items to Active"

def make_deactive(modeladmin, request, queryset):
	queryset.update(active_status='0',updated_at=datetime.datetime.now())
make_deactive.short_description = "Move Items to Deactive"

class CustomerAdmin(admin.ModelAdmin):

	exclude = [
		'authuser',
		'active_status',
		'created_at',
		'updated_at', 
		'created_by',
		'updated_by', 
	]
	list_filter = ['active_status','is_pos']
	search_fields = ['username', 'email', 'mobile']
	list_display = [
		'username',
		'first_name', 
		'email',
		'profile_pic',
		'company',
		'active_status',
		'is_pos',
		'created_at',
		'updated_at'
	]
	readonly_fields = [
		'username',
		'first_name',
		'address',
		'mobile',
		'email',
		'profile_picture',
		'active_status',
	]

	actions = [make_active,make_deactive]
	list_per_page = 10

	# fieldsets = (
	#   ('User Details', {
	# 	  'classes': ('wide', 'extrapretty'),
	# 	  'fields': ('username','isd','mobile','email','gender','profile_picture',\
	# 	  	'mobile_with_isd')
	#   }),
	#   ('Address Details', {
	# 	  # 'classes': ('wide',),
	# 	  'fields': ('country','address')
	#   }),
	 #  ('Registrations Details', {
		#   'classes': ('wide',),
		#   'fields': ('registration_datetime','refer_id',
		# 'facebook_email_id',
		# 'linkedIn_id',
		# 'linkedIn_email_id',
		# 'instagram_id',
		# 'instagram_email_id',),
	 #  }),
   # )

	def has_delete_permission(self, request, obj=None):
		return True

	def has_add_permission(self, request, obj=None):
		return False

	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_by = request.user
		else:
			obj.updated_by = request.user
			obj.updated_at = datetime.datetime.now()
		obj.save()



class CustomerOTPAdmin(admin.ModelAdmin):
	list_filter = ['is_mobile_verified', 'is_email_verfied']
	# search_fields = ['username', 'email', 'mobile']
	list_display = [
		'customer', 
		'mobile_OTP',
		'email_OTP',
		'is_mobile_verified',
		'is_email_verfied',
		'is_email_otp_used',
		'is_mob_otp_used',
		'created_at',
		# 'updated_at'
	]
	readonly_fields = [
		'customer', 
		'mobile_OTP',
		'email_OTP',
		'is_mobile_verified',
		'is_email_verfied',	
	]


	def has_delete_permission(self, request, obj=None):
		return False

	def has_add_permission(self, request, obj=None):
		return False

	def save_model(self, request, obj, form, change):
		obj.save()

admin.site.register(CustomerProfile,CustomerAdmin)
admin.site.register(customer_otp,CustomerOTPAdmin)