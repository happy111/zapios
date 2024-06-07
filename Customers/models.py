from django.db import models
from django.contrib.auth.models import User
from Location.models import CountryMaster, StateMaster,CityMaster,AreaMaster
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.safestring import mark_safe
from zapio.settings import MEDIA_URL
from smart_selects.db_fields import ChainedForeignKey
from django.contrib.auth.models import AbstractBaseUser
from Brands.models import Company
from django.contrib.postgres.fields import JSONField


class CustomerProfile(models.Model):
	auth_user = models.OneToOneField(
		User, 
		on_delete=models.CASCADE,
		related_name='CustomerProfile_auth_user', 
		null=True,
		blank=True)
	company = models.ForeignKey(
		Company, 
		related_name='CustomerProfile_Company',
		on_delete=models.CASCADE,
		verbose_name='Company',
		limit_choices_to={'active_status':'1'})
	username = models.CharField(
		max_length=100, 
		verbose_name='User Name')

	pass_pin = models.CharField(
		max_length=20,
		verbose_name='Pin')
	mobile = models.CharField(
		max_length=20,
		verbose_name='Mobile No',
		null=True,
		blank=True)
	first_name = models.CharField(
		max_length=100,
		verbose_name='First Name', 
		null=True, 
		blank=True)
	last_name = models.CharField(
		max_length=100,
		verbose_name='Last Name', 
		null=True, 
		blank=True)

	email = models.EmailField(
		max_length=100, 
		verbose_name='Email Id', 
		null=True,
		blank=True)
	profile_pic = models.ImageField(
		upload_to='customer_profile',
		null=True, 
		blank=True, 
		verbose_name='Profile Pic')
	address = models.CharField(
		max_length=150, 
		null=True, 
		blank=True, 
		verbose_name='Address')
	address1 = JSONField(
		blank=True,
		null=True,
		verbose_name='Address1')
	locality = models.CharField(
		max_length=50, 
		null=True, 
		blank=True, 
		verbose_name='locality')
	latitude = models.CharField(
		max_length=50, 
		null=True, 
		blank=True, 
		verbose_name='Latitude')
	longitude = models.CharField(
		max_length=50, 
		null=True, 
		blank=True, 
		verbose_name='Longitude')
	active_status = models.BooleanField(
		default=0, 
		verbose_name='Is Active')
	is_pos = models.BooleanField(
		default=0, 
		verbose_name='Is Pos')
	is_google = models.BooleanField(
		default=0, 
		verbose_name='Is Google')
	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(
		blank=True, 
		null=True,
		verbose_name='Updation Date & Time')

	def customer_mobile_with_isd(self):
		return "+"+str(self.mobile_with_isd) if self.mobile_with_isd else "-"
	customer_mobile_with_isd.short_description = 'Mobile No. with ISD Code'
	
	class Meta:
		verbose_name = 'Customer'
		verbose_name_plural = ' Customer Profiles'

	def __str__(self):
		if self.first_name:
			return self.first_name
		else:
			return self.email


	def profile_picture(self):
		if self.profile_pic:
			return mark_safe('<img src='+MEDIA_URL+'%s width="50" height="50" />' % (self.profile_pic))
			profile_pic.allow_tags = True
		else:
			return 'No Image'
	profile_picture.short_description = 'Profile Picture'


class customer_otp(models.Model):
	customer = models.ForeignKey(
		CustomerProfile,
		on_delete=models.CASCADE,
		related_name='customer_customer',
		verbose_name='Customer', 
		null=True, 
		blank=True)
	mobile_OTP = models.CharField(
		max_length=10, 
		verbose_name = 'Mobile OTP', 
		null=True, 
		blank=True,)
	email_OTP = models.CharField(
		max_length=10, 
		verbose_name = 'Email OTP', 
		null=True, 
		blank=True,)
	is_mobile_verified = models.BooleanField(
		default=False,
		verbose_name='Is Mobile Number Verified')
	is_email_verfied = models.BooleanField(
		default=False,
		verbose_name='Is Email Verified')
	is_email_otp_used = models.BooleanField(
		default=False,
		verbose_name='Is Email OTP Used')
	is_mob_otp_used = models.BooleanField(
		default=False,
		verbose_name='Is Mobile OTP Used')
	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name='Creation Date')

	class Meta:
		verbose_name = ' Customer OTP'
		verbose_name_plural = 'Customer OTP'

	def __int__(self):
		return self.customer
