# from django.contrib import admin
# from discount.models import *
# from django import forms
# from datetime import datetime
# from Configuration.admin import make_active, make_deactive
# from django.forms.utils import ErrorList
# # from AdroitInventry.admin_validation import CityMasterForm, CountryMasterForm, StateMasterForm
# from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter


# class CouponMasterAdmin(admin.ModelAdmin):
# 	# form = CountryMasterForm
# 	exclude = [
# 	  # 'status',
# 		'active_status',
# 		'created_at',
# 		'updated_at',
# 	  ]

# 	list_filter = [
# 		'active_status',
# 		'created_at',
# 		'updated_at', 
# 		'valid_frm',
# 		'valid_till',
# 		'Company__company_name',
# 		'category__category_name'
# 		]

# 	search_fields = [
# 	  'coupon_code',
# 	  ]

# 	list_display = [
# 	  'coupon_type',
# 	  'coupon_code',
# 	  'frequency',
# 	  'category',
# 	  'Company',
# 	  'is_min_shop',
# 	  'min_shoping',
# 	  'max_shoping',
# 	  'active_status',
# 	  'valid_frm',
# 	  'valid_till' 
# 	  ]

# 	actions = [make_active, make_deactive]
# 	# list_display_links = None
# 	list_per_page = 10

# 	def has_delete_permission(self, request, obj=None):
# 		return False

# 	def has_add_permission(self, request, obj=None):
# 		return False

# 	def save_model(self, request, obj, form, change):
# 		if not change:
# 			obj.created_at = datetime.now()
# 		else:
# 			obj.updated_at = datetime.now()
# 		obj.save()

# class QuantityComboMasterAdmin(admin.ModelAdmin):
# 	# form = CountryMasterForm
# 	exclude = [
# 	  # 'status',
# 		'active_status',
# 		'created_at',
# 		'updated_at',
# 	  ]

# 	list_filter = [
# 		'active_status',
# 		'created_at',
# 		'updated_at', 
# 		'valid_frm',
# 		'valid_till',
# 		'Company__company_name'
# 		]

# 	search_fields = [
# 	  'combo_name',
# 	  ]

# 	list_display = [
# 	  'combo_name',
# 	  'product',
# 	  'free_product',
# 	  'product_quantity',
# 	  'free_pro_quantity',
# 	  'Company',
# 	  'active_status',
# 	  'valid_frm',
# 	  'valid_till' 
# 	  ]

# 	actions = [make_active, make_deactive]
# 	list_display_links = None
# 	list_per_page = 10

# 	def has_delete_permission(self, request, obj=None):
# 		return False

# 	def has_add_permission(self, request, obj=None):
# 		return False

# 	def save_model(self, request, obj, form, change):
# 		if not change:
# 			obj.created_at = datetime.now()
# 		else:
# 			obj.updated_at = datetime.now()
# 		obj.save()


# class PercentComboMasterAdmin(admin.ModelAdmin):
# 	# form = CountryMasterForm
# 	exclude = [
# 	  # 'status',
# 		'active_status',
# 		'created_at',
# 		'updated_at',
# 	  ]

# 	list_filter = [
# 		'active_status',
# 		'created_at',
# 		'updated_at', 
# 		'valid_frm',
# 		'valid_till',
# 		'Company__company_name'
# 		]

# 	search_fields = [
# 	  'pcombo_name',
# 	  ]

# 	list_display = [
# 	  'pcombo_name',
# 	  'product',
# 	  'discount_product',
# 	  'discount_percent',
# 	  'Company',
# 	  'active_status',
# 	  'valid_frm',
# 	  'valid_till' 
# 	  ]

# 	actions = [make_active, make_deactive]
# 	list_display_links = None
# 	list_per_page = 10

# 	def has_delete_permission(self, request, obj=None):
# 		return False

# 	def has_add_permission(self, request, obj=None):
# 		return False

# 	def save_model(self, request, obj, form, change):
# 		if not change:
# 			obj.created_at = datetime.now()
# 		else:
# 			obj.updated_at = datetime.now()
# 		obj.save()



# class PercentOffersAdmin(admin.ModelAdmin):
# 	exclude = [
# 	  # 'status',
# 		'active_status',
# 		'created_at',
# 		'updated_at',
# 	  ]

# 	list_filter = [
# 		# 'active_status',
# 		# 'created_at',
# 		# 'updated_at', 
# 		# 'valid_frm',
# 		# 'valid_till',
# 		# 'Company__company_name'
# 		]

# 	search_fields = [
# 	  # 'pcombo_name',
# 	  ]

# 	list_display = [
# 	  'offer_name',
# 	  'category',
# 	  'discount_percent',
# 	  'company',
# 	  'active_status',
# 	  ]

# 	actions = [make_active, make_deactive]
# 	# list_display_links = None
# 	list_per_page = 10

# 	def has_delete_permission(self, request, obj=None):
# 		return False

# 	def has_add_permission(self, request, obj=None):
# 		return False

# 	def save_model(self, request, obj, form, change):
# 		if not change:
# 			obj.created_at = datetime.now()
# 		else:
# 			obj.updated_at = datetime.now()
# 		obj.save()




# admin.site.register(Coupon,CouponMasterAdmin)
# admin.site.register(QuantityCombo,QuantityComboMasterAdmin)
# admin.site.register(PercentCombo,PercentComboMasterAdmin)

# admin.site.register(PercentOffers,PercentOffersAdmin)