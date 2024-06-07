from django.contrib import admin
from Configuration.models import *
from datetime import datetime
from django.contrib.admin import site


def make_active(modeladmin, request, queryset):
	queryset.update(active_status='1',updated_at=datetime.now())
make_active.short_description = "Move Items to Active"

def make_deactive(modeladmin, request, queryset):
	queryset.update(active_status='0',updated_at=datetime.now())
make_deactive.short_description = "Move Items to Deactive"



class BusinessTypeAdmin(admin.ModelAdmin):
	# form = BusinessTypeForm
	exclude = [
			'active_status',
			'created_at',
			'updated_at',
			]
	search_fields = ['business_type']
	list_filter = [
				'active_status',
				'created_at', 
				'updated_at'
				]
	list_display=[
				'business_type',
				'description',
				'active_status',
				'created_at', 
				'updated_at',
				]
	actions = [
			make_active,
			make_deactive,
			]
	list_per_page = 10

	def has_delete_permission(self, request, obj=None):
		return False

	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_by = request.user
		else:
			obj.updated_by = request.user
			obj.updated_at = datetime.now()
		obj.save()



class CurrencyMasterAdmin(admin.ModelAdmin):
	# form = BusinessTypeForm
	exclude = [
			'active_status',
			'created_at',
			'updated_at',
			]
	search_fields = ['currency']
	list_filter = [
				'active_status',
				'created_at', 
				'updated_at'
				]
	list_display=[
				'currency',
				'symbol',
				'hexsymbol', 
				'active_status',
				'created_at'
				]
	actions = [
			make_active,
			make_deactive,
			]
	list_per_page = 10

	def has_delete_permission(self, request, obj=None):
		return False

	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_at = datetime.now()
		else:
			obj.updated_at = datetime.now()
		obj.save()




class PaymentDetailsAdmin(admin.ModelAdmin):
	exclude = [
			'active_status',
			'created_at',
			'updated_at',
			]
	search_fields = ['name']
	list_filter = [
				'active_status',
				'created_at', 
				'updated_at'
				]
	list_display=[
				'name',
				'company',
				'keyid', 
				'keySecret',
				'symbol',
				'active_status',
				'created_at'
				]
	actions = [
			make_active,
			make_deactive,
			]
	list_per_page = 10

	def has_delete_permission(self, request, obj=None):
		return False

	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_at = datetime.now()
		else:
			obj.updated_at = datetime.now()
		obj.save()


class ColorSettingAdmin(admin.ModelAdmin):
	exclude = [
			'active_status',
			'created_at',
			'updated_at',
			]
	search_fields = ['accent_color']
	list_filter = [
				'active_status',
				'company__company_name',
				'created_at', 
				'updated_at'
				]
	list_display=[
				'accent_color',
				'textColor',
				'secondaryColor',
				'company',
				'active_status',
				'created_at'
				]
	actions = [
			make_active,
			make_deactive,
			]
	list_per_page = 10

	def has_delete_permission(self, request, obj=None):
		return False

	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_at = datetime.now()
		else:
			obj.updated_at = datetime.now()
		obj.save()



class DeliverySettingAdmin(admin.ModelAdmin):
	exclude = [
			'active_status',
			'created_at',
			'updated_at',
			]
	search_fields = []
	list_filter = [
				'active_status',
				'company__company_name',
				'created_at', 
				'updated_at'
				]
	list_display=[
				'delivery_charge',
				'package_charge',
				'active_status',
				'created_at'
				]
	actions = [
			make_active,
			make_deactive,
			]
	list_per_page = 10

	def has_delete_permission(self, request, obj=None):
		return False

	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_at = datetime.now()
		else:
			obj.updated_at = datetime.now()
		obj.save()


class AnalyticsSettingAdmin(admin.ModelAdmin):
	exclude = [
			'active_status',
			'created_at',
			'updated_at',
			]
	search_fields = []
	list_filter = [
				'active_status',
				'company__company_name',
				'created_at', 
				'updated_at'
				]
	list_display=[
				'company',
				'u_id',
				'active_status',
				'created_at'
				]
	actions = [
			make_active,
			make_deactive,
			]
	list_per_page = 10

	def has_delete_permission(self, request, obj=None):
		return False

	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_at = datetime.now()
		else:
			obj.updated_at = datetime.now()
		obj.save()

class EmailSettingAdmin(admin.ModelAdmin):
	exclude = [
			'active_status',
			'created_at',
			'updated_at',
			]
	search_fields = [
			'content'
	        ]
	list_filter = [
				'company__company_name',
				'active_status',
				'created_at'
				]
	list_display=['company',
				  'image',
				  'content',
				  'coupon',
				  'active_status',
				  'created_at'
				]
	actions = [
			make_active,
			make_deactive,
			]
	list_per_page = 10

	def has_delete_permission(self, request, obj=None):
		return False

	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_at = datetime.now()
		else:
			obj.updated_at = datetime.now()
		obj.save()


class TaxSettingAdmin(admin.ModelAdmin):
	exclude = [
			'active_status',
			'created_at',
			'updated_at',
			]
	search_fields = [
			'tax_name'
	        ]
	list_filter = [
				'company__company_name',
				'active_status',
				'created_at'
				]
	list_display=['company',
				  'tax_name',
				  'tax_percent',
				  'active_status',
				  'created_at'
				]
	actions = [
			make_active,
			make_deactive,
			]
	list_per_page = 10

	def has_delete_permission(self, request, obj=None):
		return False

	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_at = datetime.now()
		else:
			obj.updated_at = datetime.now()
		obj.save()



class HeaderFooterAdmin(admin.ModelAdmin):
	exclude = [
			'active_status',
			'created_at',
			'updated_at',
			]
	search_fields = [
			'gst'
	        ]
	list_filter = [
				'company__company_name',
				'active_status',
				'created_at'
				]
	list_display=['company',
				  'gst',
				  'outlet',
				  'active_status',
				  'created_at'
				]
	actions = [
			make_active,
			make_deactive,
			]
	list_per_page = 10

	def has_delete_permission(self, request, obj=None):
		return True

	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_at = datetime.now()
		else:
			obj.updated_at = datetime.now()
		obj.save()


class ProductWeightageAdmin(admin.ModelAdmin):
	list_display=['company',
				  'product_name',
				  'priority',
				  'allergen_Information',
				  'product_desc',
				  'product_image',
				  'active_status',
				  'created_at'
				]

class AttendanceConfigAdmin(admin.ModelAdmin):
	list_display=['company',
				  'halfday',
				  'fullday',
				  'active_status',
				  'created_at'
				]


class UnitAdmin(admin.ModelAdmin):
	list_display=['company',
				  'unit_name',
				  'active_status',
				  'created_at'
				]

admin.site.register(BusinessType, BusinessTypeAdmin)
admin.site.register(CurrencyMaster, CurrencyMasterAdmin)
admin.site.register(PaymentDetails, PaymentDetailsAdmin)
admin.site.register(ColorSetting, ColorSettingAdmin)
admin.site.register(DeliverySetting, DeliverySettingAdmin)
admin.site.register(AnalyticsSetting, AnalyticsSettingAdmin)
admin.site.register(EmailSetting, EmailSettingAdmin)
admin.site.register(TaxSetting, TaxSettingAdmin)
admin.site.register(HeaderFooter, HeaderFooterAdmin)
admin.site.register(ProductWeightage, ProductWeightageAdmin)
admin.site.register(AttendanceConfig, AttendanceConfigAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(OrderSource)

admin.site.register(PaymentMethod)



class OnlinepaymentStatusAdmin(admin.ModelAdmin):
	list_display=['company',
				  'types',
				  'active_status',
				  'created_at'
				]
admin.site.register(OnlinepaymentStatus,OnlinepaymentStatusAdmin)


class AddressAdmin(admin.ModelAdmin):
	list_display=['pincode',
				  'prefecture',
				  'city',
				  'address'
				]
	search_fields = [
			'pincode'
	        ]
admin.site.register(Address,AddressAdmin)