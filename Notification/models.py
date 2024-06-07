from django.db import models
from django.contrib.auth.models import User
active_inactive = (('1','Active'),('0','Deactive'))
from Brands.models import Company
from Customers.models import CustomerProfile
from Configuration.models import Common
from django.contrib.postgres.fields import ArrayField



class NotificationConfiguration(models.Model):
	notification_type = models.CharField(
		max_length=100,
		verbose_name='Notification Type',unique=True)
	description = models.CharField(
		max_length=200, 
		blank=True, 
		verbose_name='Description')
	notification_for = models.CharField(max_length=20, choices=[
			('customer','Customer'),
			('admin_user','Admin User'),
		], verbose_name='Notification For')
	sample_content = models.TextField(
		verbose_name='Sample Content')
	active_status = models.BooleanField(
		default=0,
		verbose_name='Is Active')
	created_at = models.DateTimeField(
		auto_now_add=True, 
		verbose_name='Creation Date')
	updated_at = models.DateTimeField(
		blank=True, 
		null=True, 
		verbose_name='Updation Date')
	created_by = models.ForeignKey(User,
		related_name='notification_config_created_by',
		blank=True,null=True,
		limit_choices_to=~models.Q(is_staff = 0, is_superuser=0),
		verbose_name='Created by',on_delete=models.CASCADE)
	updated_by = models.ForeignKey(User,
		related_name='notification_config_updated_by',
		blank=True,null=True,limit_choices_to=~models.Q(is_staff = 0, is_superuser=0),
		verbose_name='Updated by',on_delete=models.CASCADE)

	class Meta:
		verbose_name='    Notification Type'
		verbose_name_plural='    Notification Type'

	def __str__(self):
		return self.notification_type

class NotificationRecord(models.Model):
	notification_category = models.CharField(choices=[
			('PUSH', 'PUSH'),
			('SMS', 'SMS'),
			('EMAIL', 'EMAIL')
		], max_length=50, verbose_name='Notification Category')
	notification_type = models.ForeignKey(
		NotificationConfiguration,
		on_delete=models.CASCADE,
			limit_choices_to={
			"active_status": "1",
			}, 
			related_name='NotificationRecord_notification_configuration', 
			null=True, 
			verbose_name='Notification Type')
	user = models.ForeignKey('Customers.CustomerProfile',
		related_name='notification_record_user',
		null=True,
		verbose_name='Notification sent to',
		on_delete=models.CASCADE)
	admin_user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='notification_record_admin_user',
		null=True,
		blank=True,
		verbose_name='Admin User Details')
	notification_for = models.CharField(max_length=20,
			choices=[('Customer', 'Customer'), ('Admin',
			'Admin User')], 
			verbose_name='Notification For')
	status = models.BooleanField(
		choices=[(True,'Delivered'),(False,'Undelivered')],
		verbose_name='Delivery Status')
	reason_for_failed = models.CharField(
		max_length=255,
		verbose_name='Reason For Non Delivery',
		null=True, 
		blank=True)
	message_data = models.CharField(
		max_length=1000,
		verbose_name='Message',null=True)
	massge_body = models.CharField(
		max_length=1000,
		verbose_name='Content',
		null=True,blank=True)
	otp = models.CharField(
		max_length=20,
		verbose_name='Email OTP',
		null=True, 
		blank=True)
	motp = models.CharField(
		max_length=20,
		verbose_name='Mobile OTP',
		null=True, 
		blank=True)
	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name='Creation Date')
	is_read = models.BooleanField(
		default=False,
		verbose_name='Notification Read Status')

	class Meta:
		verbose_name='  Notification History'
		verbose_name_plural='  Notification History'






class EmailVerify(models.Model):
	name = models.CharField(
		max_length=200,
		verbose_name='Name')
	types = models.CharField(
		max_length=200,
		null=True, 
		blank=True,
		verbose_name='types')
	email = models.CharField(
		max_length=200,
		verbose_name='Email')
	otp = models.CharField(
		max_length=20,
		verbose_name='Email OTP',
		null=True, 
		blank=True)
	mphin = models.CharField(
		max_length=20,
		verbose_name='Mphin',
		null=True, 
		blank=True)
	active_status = models.BooleanField(
		default=0,
		verbose_name='Is Active')
	otp_creation_time = models.DateTimeField(
		blank=True, 
		null=True,
		verbose_name='Creation Date')
	otp_use_time = models.DateTimeField(
		blank=True, 
		null=True,
		verbose_name='Otp Use time')

	Company = models.ForeignKey(
		Company, 
		null=True, 
		blank=True,
		related_name='EmailVerify_Company',
		on_delete=models.CASCADE,
		verbose_name='Company',
		limit_choices_to={'active_status':'1'})

	class Meta:
		verbose_name='    Email Verify'
		verbose_name_plural='    Email Verify'

	def __str__(self):
		return self.name




class NotificationCard(Common):
	status_choice = (
		("pending", "Pending"),
		("verified", "Verified"),
		("complete", "Complete"),
	)
	subject = models.CharField(
		max_length=200,
		verbose_name='Subject')
	content = models.CharField(
		max_length=200,
		null=True, 
		blank=True,
		verbose_name='Content')
	status = models.CharField(
		choices=status_choice,
		max_length=50,
		null=True,
		blank=True,
		verbose_name="Status",
	)
	outlet = ArrayField(models.TextField(),
	null=True, 
	blank=True, 
	verbose_name="outlet")
	class Meta:
		verbose_name='    Notice Card'
		verbose_name_plural='    Notice Card'

	def __str__(self):
		return self.subject


