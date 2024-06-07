# from django.contrib import admin
# from kitchen.models import Ingredient,StepToprocess,ProcessTrack
# from django import forms
# from datetime import datetime
# from Configuration.admin import make_active, make_deactive

# def shift_to_complete(modeladmin, request, queryset):
# 	queryset.update(process_status='0')
# shift_to_complete.short_description = "Shift to Complete Status"

# def shift_to_progress(modeladmin, request, queryset):
# 	queryset.update(process_status='1')
# shift_to_progress.short_description = "Shift to In Progess Status"

# def shift_to_pending(modeladmin, request, queryset):
# 	queryset.update(process_status='2')
# shift_to_pending.short_description = "Shift to Pending Status"

# def shift_time_to_two(modeladmin, request, queryset):
# 	queryset.update(time_of_process=2)
# shift_time_to_two.short_description = "Set Timing to 2 Secs"

# def shift_time_to_five(modeladmin, request, queryset):
# 	queryset.update(time_of_process=5)
# shift_time_to_five.short_description = "Set Timing to 5 Secs"

# def shift_time_to_thirty(modeladmin, request, queryset):
# 	queryset.update(time_of_process=30)
# shift_time_to_thirty.short_description = "Set Timing 30 Secs"




# class IngredientAdmin(admin.ModelAdmin):
# 	exclude = [
# 		'active_status',
# 		'created_at',
# 		'updated_at',
# 	  ]

# 	list_filter = [
# 		'active_status',
# 		]

# 	search_fields = [
# 	  	'name',
# 	  ]

# 	list_display = [
# 	  'name',
# 	  'food_type',
# 	  'company',
# 	  'active_status',
# 	  'created_at', 
# 	  ]

# 	actions = [make_active, make_deactive]

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

# class StepToprocessAdmin(admin.ModelAdmin):
# 	exclude = [
# 		'active_status',
# 		'created_at',
# 		'updated_at',
# 	  ]

# 	list_filter = [
# 		'active_status',
# 		]

# 	search_fields = [
# 	  	'process',
# 	  ]

# 	list_display = [
# 	  'company',
# 	  # 'Ingredient',
# 	  'process',
# 	  'time_of_process',
# 	  'active_status',
# 	  'created_at', 
# 	  ]

# 	actions = [make_active, make_deactive, shift_time_to_two, shift_time_to_five, shift_time_to_thirty]

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


# class ProcessTrackAdmin(admin.ModelAdmin):
# 	exclude = [
# 		'started_at',
# 		'completed_at',
# 	  ]

# 	list_filter = [
# 		'process_status',
# 		'Order'
# 		]

# 	# search_fields = [
# 	#   	'process',
# 	#   ]

# 	list_display = [
# 	  'company',
# 	  # 'Ingredient',
# 	  'Step',
# 	  'Order',
# 	  'product',
# 	  'Variant', 
# 	  'process_status'
# 	  ]

# 	actions = [shift_to_complete,shift_to_progress,shift_to_pending]

# 	list_per_page = 10

# 	def has_delete_permission(self, request, obj=None):
# 		return False

# 	def has_add_permission(self, request, obj=None):
# 		return False

# 	def save_model(self, request, obj, form, change):
# 		# if not change:
# 		# 	obj.created_at = datetime.now()
# 		# else:
# 		# 	obj.updated_at = datetime.now()
# 		obj.save()



# admin.site.register(Ingredient,IngredientAdmin)
# admin.site.register(StepToprocess,StepToprocessAdmin)
# admin.site.register(ProcessTrack,ProcessTrackAdmin)