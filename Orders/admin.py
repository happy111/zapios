from django.contrib import admin
from Brands.models import Company
from datetime import datetime
from Orders.models import *
from django.contrib.admin import site
from django.forms.utils import ErrorList
from django import forms
from django.contrib.auth.models import User
from Configuration.admin import make_active, make_deactive


class OrderStatusMasterAdmin(admin.ModelAdmin):
	# form = CompanyForm
	exclude = [
			'created_at',
			'updated_at',
			'active_status'
			]
	search_fields = [
		'Order_staus_name',
		]
	list_display = [
		  'Order_staus_name',
		  'active_status',
		  'can_process',
		  'created_at',
		  'updated_at'
			]
	list_filter = [
		'active_status',
		'created_at',
		'updated_at'
		]
	actions = [make_active, make_deactive]
	list_per_page = 5
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

class OrderMasterAdmin(admin.ModelAdmin):
	# form = InstaOutletForm
	exclude = ['is_paid','synced']
	list_filter = ['is_paid','outlet__Outletname','Company__company_name','payment_mode',
	'order_status','is_completed','has_been_here','order_source','order_type','is_aggregator']
	search_fields = ['order_id']
	list_display = ['order_id','order_time','delivery_time','payment_mode','order_status',\
					'is_aggregator','urban_order_id',\
					'has_been_here','sub_total','discount_value','taxes','total_bill_value']
	# readonly_fields = ['updated_at']
	readonly_fields = ['Company','outlet','order_id','outlet_order_id','address','customer',
	'Company_outlet_details','settlement_details','delivery_boy_details',\
	'tax_detail','Aggregator_order_status',\
	'order_status',
	'is_aggregator','urban_order_id','payment_source','is_accepted','discount_Offers',\
	'transaction_id','packing_charge','delivery_charge','order_source','user',\
	'order_description','order_time','delivery_time','taxes','payment_mode','special_instructions',\
	'delivery_boy','sub_total','discount_value','payment_id','coupon_code','discount_name','is_paid',\
	'total_bill_value','total_items','is_completed','has_been_here','is_seen','is_rider_assign',\
	'order_type',\
	'order_cancel','cancel_responsibility','order_cancel_reason','channel_order_id']

	# 
	list_per_page = 105

	# list_display_links = None
	actions = [make_active, make_deactive]
	def has_add_permission(self, request, obj=None):
		return False

	def has_delete_permission(self, request, obj=None):
		return True

	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_at = datetime.now()
		else:
			obj.updated_at = datetime.now()
		obj.save()


class OrderTrackingAdmin(admin.ModelAdmin):
	# form = InstaOutletForm
	exclude = []
	list_filter = ['Order_staus_name','created_at','order__Company__company_name',
															'order__outlet__Outletname']
	search_fields = ['order__order_id']
	list_display = ['order','Order_staus_name','created_at','updated_at']
	readonly_fields = ['updated_at']

	actions = [make_active, make_deactive]

	list_per_page = 100

	# list_display_links = None

	# change_form_template = 'custom_form_outlet.html'

	def has_add_permission(self, request, obj=None):
		return True

	def has_delete_permission(self, request, obj=None):
		return True

	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_at = datetime.now()
		else:
			obj.updated_at = datetime.now()
		obj.save()


admin.site.register(OrderStatusType,OrderStatusMasterAdmin)
admin.site.register(Order,OrderMasterAdmin)
admin.site.register(OrderTracking,OrderTrackingAdmin)





