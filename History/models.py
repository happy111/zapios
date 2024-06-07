from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.safestring import mark_safe
from zapio.settings import MEDIA_URL
from Brands.models import Company
from Product.models import *
from django.contrib.postgres.fields import ArrayField,JSONField
from Outlet.models import OutletProfile
from discount.models import Coupon
from Orders.models import Order
from Brands.models import Company
from Outlet.models import DeliveryBoy
from Orders.models import OrderStatusType,Order
from Event.models import PrimaryEventType
from UserRole.models import ManagerProfile



class CouponUsed(models.Model):
	Coupon =  models.ForeignKey(
		Coupon, 
		related_name='CouponUsed_coupon',
		on_delete=models.CASCADE,
		verbose_name='Coupon',
		limit_choices_to={'active_status':'1'})
	customer = JSONField(
		blank=True,
		null=True,
		verbose_name="Customer Details")
	order_id = models.ForeignKey(
		Order, 
		related_name='CouponUsed_order',
		on_delete=models.CASCADE,
		verbose_name='Order')
	Company = models.ForeignKey(
		Company, 
		related_name='CouponUsed_Company',
		on_delete=models.CASCADE,
		verbose_name='Company',
		limit_choices_to={'active_status':'1'})
	outlet = models.ForeignKey(
		OutletProfile, 
		related_name='CouponUsed_OutletProfile',
		on_delete=models.CASCADE,
		verbose_name='Outlet',
		limit_choices_to={'active_status':'1'})
	created_at = models.DateTimeField(
		auto_now_add=True, 
		verbose_name='Used At')
	class Meta:
		verbose_name ="Used Coupon"
		verbose_name_plural ="  Used Coupons"

	def __str__(self):
		return str(self.Coupon.coupon_code)


class RiderHistory(models.Model):
	Rider =  models.ForeignKey(
		ManagerProfile, 
		related_name='RiderHistory_Rider',
		on_delete=models.CASCADE,
		verbose_name='Rider',
		limit_choices_to={'is_rider':'1','active_status':'1'})
	order_id = models.ForeignKey(
		Order, 
		related_name='RiderHistory_order',
		on_delete=models.CASCADE,
		verbose_name='Order')
	Company = models.ForeignKey(
		Company, 
		related_name='RiderHistory_Company',
		on_delete=models.CASCADE,
		verbose_name='Company',
		limit_choices_to={'active_status':'1'})
	outlet = models.ForeignKey(
		OutletProfile, 
		related_name='RiderHistory_OutletProfile',
		on_delete=models.CASCADE,
		verbose_name='Outlet',
		limit_choices_to={'active_status':'1'})
	created_at = models.DateTimeField(
		auto_now_add=True, 
		verbose_name='Used At')

	class Meta:
		verbose_name ="Rider History"
		verbose_name_plural ="  Rider History"

	def __str__(self):
		return str(self.Rider)



class OutletLogs(models.Model):
	Company = models.ForeignKey(
		Company, 
		related_name='OutletLog_Company',
		on_delete=models.CASCADE,
		verbose_name='Company',
		limit_choices_to={'active_status':'1'})
	outlet = models.ForeignKey(
		OutletProfile, 
		related_name='OutletLog_OutletProfile',
		on_delete=models.CASCADE,
		verbose_name='Outlet',
		limit_choices_to={'active_status':'1'})
	opening_time = models.DateTimeField(
		auto_now_add=False, 
		null=True,
		blank=True,
		verbose_name="Opening Time")
	closing_time = models.DateTimeField(
		auto_now_add=False, 
		null=True,
		blank=True,
		verbose_name="Closing Time")
	auth_user = models.ForeignKey(
		User, 
		on_delete=models.CASCADE,
		related_name='OutletLog_auth_user', 
		null=True,
		blank=True)
	is_open = models.BooleanField(
		default=1, 
		verbose_name='Is Open')
	created_at = models.DateTimeField(
		auto_now_add=True, 
		verbose_name='Used At')

	class Meta:
		verbose_name ="OutletLogHistory"
		verbose_name_plural ="  OutletLog History"

	def __str__(self):
		return str(self.auth_user)



class Logs(models.Model):
	Company = models.ForeignKey(
		Company, 
		related_name='Logs_Company',
		on_delete=models.CASCADE,verbose_name='Company',
		limit_choices_to={'active_status':'1'})
	outlet = models.ForeignKey(
		OutletProfile, 
		related_name='Logs_outlet',
		null=True,
		blank=True,
		on_delete=models.CASCADE,
		verbose_name='Outlet',
		limit_choices_to={'active_status':'1'})
	order_status = models.ForeignKey(
		OrderStatusType, 
		related_name='Logs_order_status',
		null=True,
		blank=True,
		on_delete=models.CASCADE,
		verbose_name='Order Status',
		limit_choices_to={'active_status':'1'})
	order_id = models.CharField(
		max_length=50, 
		null=True,
		blank=True, 
		verbose_name='Order ID')
	relevance = models.CharField(
		max_length=50, 
		null=True,
		blank=True, 
		verbose_name='Relevance')
	trigger = models.ForeignKey(
		PrimaryEventType, 
		related_name='Logs_trigger',
		null=True,
		blank=True,
		on_delete=models.CASCADE,
		verbose_name='Trigger ID')
	event_name = models.CharField(
		max_length=50, 
		null=True,
		blank=True, 
		verbose_name='Event Name')
	event_by = models.CharField(
		max_length=50, 
		null=True,
		blank=True, 
		verbose_name='Event Name')
	event_time = models.DateTimeField(
		auto_now_add=True, 
		null=True,
		blank=True,
		verbose_name="Closing Time")
	count = models.PositiveIntegerField(
		null=True, 
		blank=True, 
		verbose_name='count')
	reason = models.CharField(
		max_length=50, 
		null=True,
		blank=True, 
		verbose_name='Reason')
	auth_user = models.ForeignKey(
		User, 
		on_delete=models.CASCADE,
		related_name='Logs_auth_user', 
		null=True,
		blank=True)

	class Meta:
		verbose_name ="Logs"
		verbose_name_plural ="  Logs"

	def __str__(self):
		return str(self.auth_user)



class MenuCounts(models.Model):
	company = models.ForeignKey(
		'Brands.Company', 
		related_name='MenuCounts_Company',
		on_delete=models.CASCADE,
		verbose_name='Company',
		limit_choices_to={'active_status':'1'})
	menu = models.ForeignKey(
		Menu, 
		related_name='MenuCounts_menu',
		on_delete=models.CASCADE,
		verbose_name='Menu',
		limit_choices_to={'active_status':'1'})
	menu_name = models.CharField(
		max_length=100, 
		verbose_name='Menu Name')
	event_time = models.DateTimeField(
		auto_now_add=True, 
		null=True,
		blank=True,
		verbose_name="Event Time")

	class Meta:
		verbose_name = 'Menu Count'
		verbose_name_plural = '  Menu Count'