from django.db import models
from django.contrib.auth.models import User
from Location.models import CountryMaster, StateMaster,CityMaster,AreaMaster
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.safestring import mark_safe
from zapio.settings import MEDIA_URL
from smart_selects.db_fields import ChainedForeignKey
from django.contrib.auth.models import AbstractBaseUser
from Brands.models import Company
from UserRole.models import UserType
from django.contrib.postgres.fields import ArrayField,JSONField
from UserRole.models import ManagerProfile


class OutletProfile(models.Model):
	auth_user = models.OneToOneField(User, 
		on_delete=models.CASCADE,
		related_name='instaoutlet_profile_auth_user', 
		null=True,
		blank=True)
	Company = models.ForeignKey(Company, 
		related_name='OutletProfile_Company',
		on_delete=models.CASCADE,
		verbose_name='Company',
		limit_choices_to={'active_status':'1'})
	outlet_image =  models.ImageField(upload_to='outlet_image/', 
		verbose_name='Image', 
		null=True,blank=True)
	Outletname =  models.CharField(
		max_length=100, 
		verbose_name='Outlet Name', 
		unique=True)
	outlet_phone = models.CharField(
		max_length=100, 
		null = True,
		blank = True,
		verbose_name='Outlet Phone' )
	outlet_email = models.CharField(
		max_length=100, 
		blank = True,
		null = True,
		verbose_name='Outlet Email')
	min_delivery_time= models.PositiveIntegerField(
		null=True, 
		blank=True, 
		verbose_name='Minimum Delivery Time')
	min_picking_time= models.PositiveIntegerField(
		null=True, 
		blank=True, 
		verbose_name='Minimum Picking Time')
	address = models.CharField(
		max_length=150,
		verbose_name='Address')
	latitude = models.CharField(
		max_length=50,
		verbose_name='Latitude')
	longitude = models.CharField(
		max_length=50,
		verbose_name='Longitude')
	country = models.ForeignKey('Location.CountryMaster',
		related_name='Outlet_country',
		on_delete=models.CASCADE,
		verbose_name='Country',
		limit_choices_to={'active_status': '1'}, 
		null=True, blank=True)
	prefecture = models.CharField(max_length=50,
		null=True, 
		blank=True, 
		verbose_name='Prefecture')
	city = models.CharField(max_length=50,
		null=True, 
		blank=True, 
		verbose_name='city')
	landmark = models.CharField(max_length=50,
		null=True, 
		blank=True, 
		verbose_name='city')
	pincode = models.CharField(max_length=50,
		verbose_name='Pincode')
	map_city = ArrayField(models.TextField(),
		null=True, 
		blank=True, 
		verbose_name="All City")
	map_locality = ArrayField(models.TextField(),
		null=True, 
		blank=True, 
		verbose_name="Locality")
	payment_method = ArrayField(models.TextField(),
		null=True, 
		blank=True, 
		verbose_name="payment_method")
	address = models.CharField(
		max_length=200,
		null=True, 
		blank=True, 
		verbose_name='Address')
	ip_address = models.CharField(
		max_length=200,
		null=True, 
		blank=True, 
		verbose_name='IP Address')
	active_status = models.BooleanField(default=1, 
		verbose_name='Is Active')
	is_open = models.BooleanField(default=1, 
		verbose_name='Is Open')
	is_pos_open = models.BooleanField(default=1, 
		verbose_name='Is Pos Open')
	is_company_active = models.BooleanField(default=1, 
		verbose_name='Is Comapny Active')
	opening_time = models.TimeField(auto_now=False, 
		auto_now_add=False, 
		null=True,blank=True,
		verbose_name="Opening Time")
	closing_time = models.TimeField(auto_now=False, 
		auto_now_add=False, 
		null=True,
		blank=True,
		verbose_name="Closing Time")
	priority = models.PositiveIntegerField(
		null=True, 
		blank=True, 
		verbose_name='Priority')
	min_value = models.FloatField(
		blank=True,
		null=True,
		verbose_name='Min Value')
	average_delivery_time = models.TimeField(
		auto_now=False, 
		auto_now_add=False, 
		null=True,blank=True,
		verbose_name="Average Delivery Time")
	no_of_days = models.CharField(
		max_length=300,
		null=True, 
		blank=True, 
		verbose_name='No Of Days')
	time_range = models.CharField(
		max_length=300,
		null=True, 
		blank=True, 
		verbose_name='Time Range')
	radius = models.CharField(
		max_length=300,
		null=True, 
		blank=True, 
		verbose_name='Time Range')
	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(
		blank=True, 
		null=True,
		verbose_name='Updation Date & Time')
	check_list = ArrayField(
		models.TextField(),
		null=True, 
		blank=True, 
		verbose_name="Check List")
	cam_url = models.CharField(
		max_length=255,
		verbose_name='Cam Url', 
		null=True, 
		blank=True)
	delivery_zone = JSONField(blank=True,null=True)
	is_hide = models.BooleanField(
		default=0, 
		verbose_name='Is Hide')
	sanitized_restaurant = models.BooleanField(
		default=0, 
		verbose_name='Is sanitized_restaurant')
	temperature_check = models.BooleanField(
		default=0, 
		verbose_name='Is temperature_check')
	clean_kitchen = models.BooleanField(
		default=0, 
		verbose_name='Is clean_kitchen')
	acceptance =  models.CharField(
		max_length=100, 
		verbose_name='Acceptance Time')
	processing =  models.CharField(
		max_length=100, 
		verbose_name='Processing Time')
	dispatch =  models.CharField(
		max_length=100, 
		verbose_name='Dispatch Time')
	api_key = models.CharField(
		max_length=500, 
		null=True, 
		blank=True,
		unique=True)
	eion_outlet_id = models.IntegerField(
		null=True, 
		blank=True)
	def customer_mobile_with_isd(self):
		return "+"+str(self.mobile_with_isd) if self.mobile_with_isd else "-"
	customer_mobile_with_isd.short_description = 'Mobile No. with ISD Code'

	class Meta:
		verbose_name = 'Outlet'
		verbose_name_plural = '  Outlet Profiles'
		#unique_together = ('Company', 'priority',)

	def __str__(self):
		return self.Outletname

	def om_picture(self):
		if self.om_pic:
			return mark_safe('<img src='+MEDIA_URL+'%s width="50" height="50" />' % (self.om_pic))
			om_picture.allow_tags = True
		else:
			return 'No Image'
			
	om_picture.short_description = 'Profile Picture'

class OutletMilesRules(models.Model):
	rule_name = models.CharField(
		max_length=100, 
		unique=True, 
		verbose_name='Rule Name', 
		db_index=True)
	active_status = models.BooleanField(
		default=0,
		verbose_name='Active Status')
	Company = models.ForeignKey(
		Company, 
		related_name='OutletMilesRules_Company',
		on_delete=models.CASCADE,
		verbose_name='Company',
		limit_choices_to={'active_status':'1'})
	unloaded_miles = models.PositiveIntegerField(
		verbose_name='Circle Radius in Kms')
	created_at = models.DateTimeField(
			auto_now_add=True, 
			verbose_name='Created Date & Time') 
	updated_at = models.DateTimeField(
		auto_now=True, 
		verbose_name='Updated Date & Time')

	class Meta:
		verbose_name = "Circle Radius Rule"
		verbose_name_plural = "   Outlet Circle Radius Rule"

	def __str__(self):
		return str(self.rule_name)


class DeliveryBoy(models.Model):
	outlet = ArrayField(
		models.TextField(),
		null=True, 
		blank=True, 
		verbose_name="Outlet Mapped Ids")
	name = models.CharField(
		max_length=100, 
		verbose_name='Name')
	email = models.EmailField(
		max_length=100, 
		verbose_name='Email Id',
		null=True,
		blank=True)
	profile_pic = models.ImageField(
		upload_to='deliveryboy_profile',
		null=True, 
		blank=True, 
		verbose_name='Profile Pic')
	mobile = models.CharField(
		max_length=20,
		verbose_name='Mobile',
		null=True,
		blank=True)
	address = models.CharField(
		max_length=150,
		verbose_name='Address')
	Company = models.ForeignKey(
		Company, 
		related_name='DeliveryBoy_Company',
		null=True, blank=True,
		on_delete=models.CASCADE,
		verbose_name='Company',
		limit_choices_to={'active_status':'1'})
	active_status = models.BooleanField(
		default=1, 
		verbose_name='Is Active')
	is_assign = models.BooleanField(
		default=0, 
		verbose_name='Is Assigned')
	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(
		blank=True, 
		null=True,
		verbose_name='Updation Date & Time')
	
	class Meta:
		verbose_name = 'DeliveryBoy'
		verbose_name_plural = 'Delivery Person Details'

	def _str_(self):
		return self.name

	def om_picture(self):
		if self.om_pic:
			return mark_safe('<img src='+MEDIA_URL+'%s width="50" height="50" />' % (self.om_pic))
			om_picture.allow_tags = True
		else:
			return 'No Image'
	om_picture.short_description = 'Profile Picture'


class OutletTimingMaster(models.Model):
	outlet= models.ForeignKey(OutletProfile, 
		related_name='OutletTimingMaster_outlet',
		on_delete=models.CASCADE,verbose_name='Outlet Name',
		limit_choices_to={'active_status':'1'},
		null=True,blank=True)
	allday = JSONField(
		blank=True,
		null=True)
	name = models.CharField(
		max_length=100,  
		verbose_name='name',)
	Company = models.ForeignKey(Company, 
		related_name='OutletTimingMaster_Company',
		on_delete=models.CASCADE,verbose_name='Company',
		limit_choices_to={'active_status':'1'})

	class Meta:
		verbose_name = "Outlet Timing"
		verbose_name_plural = "   Outlet Timing"

	def __str__(self):
		return str(self.name)

class OutletTiming(models.Model):
	outlet= models.ForeignKey(OutletProfile, 
		related_name='OutletTiming_outlet',
		on_delete=models.CASCADE,verbose_name='Outlet Name',
		limit_choices_to={'active_status':'1'},
		null=True,blank=True)
	masterid= models.ForeignKey(OutletTimingMaster, 
		related_name='OutletTiming_masterid',
		on_delete=models.CASCADE,verbose_name='Master ID',
		limit_choices_to={'active_status':'1'},
		null=True,blank=True)
	allday = JSONField(blank=True,
		null=True)
	day = models.CharField(max_length=100,  
		verbose_name='Day',)
	active_status = models.BooleanField(default=0,
		verbose_name='Active Status')
	Company = models.ForeignKey(Company, 
		related_name='OutletTiming_Company',
		on_delete=models.CASCADE,verbose_name='Company',
		limit_choices_to={'active_status':'1'})
	opening_time = models.TimeField(
		auto_now=False, 
		auto_now_add=False, 
		null=True,
		blank=True,
		verbose_name="Opening Time")
	closing_time = models.TimeField(
		auto_now=False, 
		auto_now_add=False, 
		null=True,blank=True,
		verbose_name="Closing Time")
	slots = models.CharField(
		max_length=100,  
		verbose_name='slots', 
		null=True,blank=True)
	created_at = models.DateTimeField(
		auto_now_add=True, 
		verbose_name='Created Date & Time')
	updated_at = models.DateTimeField(
		auto_now=True, 
		verbose_name='Updated Date & Time')

	class Meta:
		verbose_name = "Outlet Timing"
		verbose_name_plural = "   Outlet Timing"

	def __str__(self):
		return str(self.day)


class TempTracking(models.Model):
	Company = models.ForeignKey(
		Company, 
		related_name='TempTracking_Company',
		on_delete=models.CASCADE,
		verbose_name='Company',
		limit_choices_to={'active_status':'1'})
	outlet = models.ForeignKey(
		OutletProfile, 
		related_name='TempTracking_outlet',
		on_delete=models.CASCADE,
		verbose_name='Outlet',
		limit_choices_to={'active_status':'1'})
	staff = models.ForeignKey(
		ManagerProfile, 
		related_name='TempTracking_staff',
		on_delete=models.CASCADE,
		verbose_name='Staff Mmeber',
		limit_choices_to={'active_status':'1'})
	body_temp = models.FloatField(
		verbose_name='Body Temp in F')
	is_latest = models.BooleanField(
		default=1, 
		verbose_name='Is Latest')
	created_at = models.DateTimeField(
	auto_now_add=True, 
	verbose_name='Created Date & Time') 
	updated_at = models.DateTimeField(
		null=True, 
		blank=True, 
		verbose_name='Updated Date & Time')

	class Meta:
		verbose_name = "Staff Temperature Tracking"
		verbose_name_plural = "   Staff Temperature Tracking"




# For urbanpiper outlet timing and action logs related to it.............
class OutletTimeTable(models.Model):
	company = models.ForeignKey('Brands.Company', on_delete=models.CASCADE,verbose_name='Company',
												limit_choices_to={'active_status':'1'})
	outlet = models.ForeignKey(OutletProfile, on_delete=models.CASCADE, verbose_name='Outlet',
												limit_choices_to={'active_status':'1'})
	monday_slot_1_opening = models.TimeField(null=True,blank=True,
													verbose_name="Slot 1 Opening Time for Monday")
	monday_slot_1_closing = models.TimeField(null=True,blank=True,
													 verbose_name="Slot 1 Closing Time for Monday")
	monday_slot_2_opening = models.TimeField(null=True,blank=True,
												 verbose_name="Slot 2 Opening Time for Monday")
	monday_slot_2_closing = models.TimeField(null=True,blank=True,
												 verbose_name="Slot 2 Closing Time for Monday")
	
	tuesday_slot_1_opening = models.TimeField(null=True,blank=True,
													verbose_name="Slot 1 Opening Time for Tuesday")
	tuesday_slot_1_closing = models.TimeField(null=True,blank=True,
													 verbose_name="Slot 1 Closing Time for Tuesday")
	tuesday_slot_2_opening = models.TimeField(null=True,blank=True,
												 verbose_name="Slot 2 Opening Time for Tuesday")
	tuesday_slot_2_closing = models.TimeField(null=True,blank=True,
												 verbose_name="Slot 2 Closing Time for Tuesday")

	wednesday_slot_1_opening = models.TimeField(null=True,blank=True,
													verbose_name="Slot 1 Opening Time for Wednesday")
	wednesday_slot_1_closing = models.TimeField(null=True,blank=True,
													 verbose_name="Slot 1 Closing Time for Wednesday")
	wednesday_slot_2_opening = models.TimeField(null=True,blank=True,
												 verbose_name="Slot 2 Opening Time for Wednesday")
	wednesday_slot_2_closing = models.TimeField(null=True,blank=True,
												 verbose_name="Slot 2 Closing Time for Wednesday")

	thursday_slot_1_opening = models.TimeField(null=True,blank=True,
												  verbose_name="Slot 1 Opening Time for Thursday")
	thursday_slot_1_closing = models.TimeField(null=True,blank=True,
												  verbose_name="Slot 1 Closing Time for Thursday")
	thursday_slot_2_opening = models.TimeField(null=True,blank=True,
												 verbose_name="Slot 2 Opening Time for Thursday")
	thursday_slot_2_closing = models.TimeField(null=True,blank=True,
												 verbose_name="Slot 2 Closing Time for Thursday")

	friday_slot_1_opening = models.TimeField(null=True,blank=True,
												  verbose_name="Slot 1 Opening Time for Friday")
	friday_slot_1_closing = models.TimeField(null=True,blank=True,
												  verbose_name="Slot 1 Closing Time for Friday")
	friday_slot_2_opening = models.TimeField(null=True,blank=True,
												 verbose_name="Slot 2 Opening Time for Friday")
	friday_slot_2_closing = models.TimeField(null=True,blank=True,
												 verbose_name="Slot 2 Closing Time for Friday")

	saturday_slot_1_opening = models.TimeField(null=True,blank=True,
												  verbose_name="Slot 1 Opening Time for Saturday")
	saturday_slot_1_closing = models.TimeField(null=True,blank=True,
												  verbose_name="Slot 1 Closing Time for Saturday")
	saturday_slot_2_opening = models.TimeField(null=True,blank=True,
												 verbose_name="Slot 2 Opening Time for Saturday")
	saturday_slot_2_closing = models.TimeField(null=True,blank=True,
												 verbose_name="Slot 2 Closing Time for Saturday")

	sunday_slot_1_opening = models.TimeField(null=True,blank=True,
												  verbose_name="Slot 1 Opening Time for Sunday")
	sunday_slot_1_closing = models.TimeField(null=True,blank=True,
												  verbose_name="Slot 1 Closing Time for Sunday")
	sunday_slot_2_opening = models.TimeField(null=True,blank=True,
												 verbose_name="Slot 2 Opening Time for Sunday")
	sunday_slot_2_closing = models.TimeField(null=True,blank=True,
												 verbose_name="Slot 2 Closing Time for Sunday")

	is_closed_1 = models.BooleanField(default=0,verbose_name="Closed on Day 1")
	is_closed_2 = models.BooleanField(default=0,verbose_name="Closed on Day 2")
	is_closed_3 = models.BooleanField(default=0,verbose_name="Closed on Day 3")
	is_closed_4 = models.BooleanField(default=0,verbose_name="Closed on Day 4")
	is_closed_5 = models.BooleanField(default=0,verbose_name="Closed on Day 5")
	is_closed_6 = models.BooleanField(default=0,verbose_name="Closed on Day 6")
	is_closed_7 = models.BooleanField(default=0,verbose_name="Closed on Day 7")

	class Meta:
		verbose_name = 'Outlet TimeTable'
		verbose_name_plural = 'Outlet TimeTable'

	def __str__(self):
		return str(self.outlet)
