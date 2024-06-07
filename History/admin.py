from django.contrib import admin
from History.models import *
from django import forms
from datetime import datetime
from Configuration.admin import make_active, make_deactive
from django.forms.utils import ErrorList
# from AdroitInventry.admin_validation import CityMasterForm, CountryMasterForm, StateMasterForm
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter


class CouponUsedMasterAdmin(admin.ModelAdmin):
	# form = CountryMasterForm
	exclude = [
	  # 'status',
		'created_at',
	  ]

	list_filter = [
		'created_at',
		]

	search_fields = [
	  'Coupon__coupon_code',
	  ]

	list_display = [
	  'Coupon',
	  'created_at'
	  ]

	list_display_links = None
	list_per_page = 10

	def has_delete_permission(self, request, obj=None):
		return True

	def has_add_permission(self, request, obj=None):
		return False

	def save_model(self, request, obj, form, change):
		if not change:
			obj.created_at = datetime.now()
		else:
			obj.created_at = datetime.now()
		obj.save()


admin.site.register(CouponUsed,CouponUsedMasterAdmin)
admin.site.register(RiderHistory)