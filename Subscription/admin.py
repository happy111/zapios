from django.contrib import admin
from Subscription.models import *
from datetime import datetime
from django.contrib.admin import site


def make_active(modeladmin, request, queryset):
	queryset.update(active_status='1',updated_at=datetime.now())
make_active.short_description = "Move Items to Active"

def make_deactive(modeladmin, request, queryset):
	queryset.update(active_status='0',updated_at=datetime.now())
make_deactive.short_description = "Move Items to Deactive"



class SubscriptionPlanTypeAdmin(admin.ModelAdmin):
	exclude = [
			'active_status',
			'created_at',
			'updated_at',
			]

	list_filter = [
				'plan_name',
				'active_status',
				'created_at'
				]
	list_display=['plan_name',
				  'membership_status',
				  'cost',
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



admin.site.register(SubscriptionPlanType, SubscriptionPlanTypeAdmin)

admin.site.register(SubscriptionPaymentModel)



