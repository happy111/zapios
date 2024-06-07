from django.db import models
from django.contrib.auth.models import User
from Location.models import CountryMaster, StateMaster,CityMaster
from Configuration.models import CurrencyMaster,BusinessType
from smart_selects.db_fields import ChainedForeignKey
from django.core.validators import RegexValidator
from django.utils.safestring import mark_safe
from zapio.settings import MEDIA_URL
from Configuration.models import Common
from django.contrib.postgres.fields import ArrayField,JSONField

class Company(models.Model):
	from Subscription.models import SubscriptionPlanType
	status_choice = (
		("one_time", "One Time"),
		("multiple_time", "Multiple Time"),
	)
	loginType = (
		("plain", "plain"),
		("google", "google"),
	)
	auth_user = models.OneToOneField(
		User, 
		on_delete=models.CASCADE,
		related_name='company_auth_user', 
		null=True,
		blank=True)
	company_name = models.CharField(
		max_length=50,
		unique=True,
		verbose_name='Brand Name')
	subdomain = models.CharField(
		max_length=50, 
		verbose_name="Brand Subdomain", 
		unique=True, 
		null=True)
	plan_name = models.ForeignKey(SubscriptionPlanType, 
		on_delete=models.CASCADE,
		related_name='company_plan_name',
		limit_choices_to={
		'active_status': '1'},
		verbose_name='Plan Name')
	business_nature = models.ForeignKey(
		BusinessType,
		verbose_name='Business Nature',
		on_delete=models.CASCADE,
		limit_choices_to={'active_status': '1'},)
	username = models.CharField(
		max_length=100, 
		verbose_name='User Name', 
		unique=True)
	password = models.CharField(
		max_length=20,
		verbose_name='Password')
	address = models.CharField(
		max_length=250, 
		verbose_name='Address',
		null=True, 
		blank=True,)
	country = models.ForeignKey(
		CountryMaster,  
		null=True, 
		blank=True,
		on_delete=models.CASCADE,
		related_name='company_country',
		limit_choices_to={'active_status': '1'},
		verbose_name='Country')
	state = models.ForeignKey(
		StateMaster,  
		null=True, 
		blank=True,
		on_delete=models.CASCADE,
		related_name='company_state',
		limit_choices_to={'active_status': '1'},
		verbose_name='State')
	city = models.ForeignKey(
		CityMaster,  
		null=True, 
		blank=True,
		on_delete=models.CASCADE,
		related_name='company_city',
		limit_choices_to={'active_status': '1'},
		verbose_name='City',
	  )
	zipcode = models.CharField(
		max_length=6,  
		null=True, 
		blank=True,
		verbose_name='PIN Code')
	company_logo = models.ImageField(
		upload_to='company_logo',
		null=True, 
		blank=True, 
		verbose_name='Company Logo')
	company_landing_imge = models.ImageField(
		upload_to='company_banner',
		null=True, 
		blank=True, 
		verbose_name='Company Banner')
	company_registrationNo = models.CharField(
		max_length=25,  
		null=True, 
		blank=True,
		verbose_name='Company Registration No.')
	company_tinnNo = models.CharField(
		max_length=11, 
		null=True,
		blank=True, 
		verbose_name='TIN No.')
	company_vatNo = models.CharField(
		max_length=13, 
		null=True,
		blank=True,
		verbose_name='VAT No.')
	company_gstNo = models.CharField(
		max_length=15, 
		null=True,
		blank=True, 
		verbose_name='GST No.')
	website = models.URLField(
		max_length=50, 
		blank=True, 
		null=True,
		verbose_name='Company Website')
	company_contact_no = models.CharField( 
		null=True, 
		blank=True,
		max_length=15, 
		verbose_name='Contact No.')
	company_email_id = models.EmailField(
		max_length=50,
		unique=True,  
		verbose_name='Contact Email Id')
	support_person = models.CharField(
		max_length=50,
		verbose_name='Support Person Name',
		null=True,
		blank=True)
	support_person_mobileno = models.CharField(
		max_length=15,
		verbose_name='Support Mobile No.',  
		null=True, 
		blank=True,
		help_text='Please enter Country /ISD code before mobile number'
		 )
	support_person_email_id = models.EmailField(
		max_length=255,  
		null=True, 
		blank=True,
		verbose_name='Support Email ID')
	support_person_landlineno = models.CharField(
		max_length=15,  
		null=True, 
		blank=True,
		verbose_name='Support Landline No.')
	contact_person = models.CharField(
		max_length=50,  
		null=True, 
		blank=True,
		verbose_name='Contact Person Name')
	contact_person_mobileno = models.CharField(
		max_length=15,  
		null=True, 
		blank=True,
		verbose_name='Contact Mobile No.',
		help_text='Please enter Country /ISD code before mobile number'
		)

	contact_person_email_id = models.EmailField(
		max_length=255,  
		null=True, 
		blank=True,
		verbose_name='Contact Other Email ID')
	contact_person_landlineno = models.CharField(
		max_length=15,  
		null=True, 
		blank=True,
		verbose_name='Contact Landline No.')
	owner_name = models.CharField(
		max_length=50,  
		null=True, 
		blank=True,
		verbose_name='Owner Name')
	owner_email = models.EmailField(
		max_length=255,  
		null=True, 
		blank=True,
		verbose_name='Owner Email Id')
	owner_phone = models.CharField(
		max_length=15,  
		null=True, 
		blank=True,
		verbose_name='Owner Mobile No.',
		help_text='Please enter Country /ISD code before mobile number'
		)
	billing_address = models.CharField(
		max_length=250,
		verbose_name='Billing Address', 
		blank=True, 
		null=True)
	is_open = models.BooleanField(
		default=0,
		blank=True, 
		null=True, 
		verbose_name='Is Open')
	is_firstUser = models.BooleanField(
		default=0,
		blank=True, 
		null=True, 
		verbose_name='is_firstUser')
	billing_country = models.ForeignKey(
	  CountryMaster,
	  on_delete=models.CASCADE,
	  related_name='company_billing_country',
	  verbose_name='Billing Country',
	  blank=True,
	  null=True,
	  limit_choices_to={'active_status': '1'},
	  )
	billing_state = models.ForeignKey(
	  StateMaster,
	  on_delete=models.CASCADE,
	  related_name='company_billing_state',
	  verbose_name='Billing State',
	  blank=True,
	  null=True,
	  limit_choices_to={'active_status': '1'},
	  )
	billing_city = models.ForeignKey(
	  CityMaster,
	  on_delete=models.CASCADE,
	  related_name='company_billing_city',
	  verbose_name='Billing City',
	  blank=True,
	  null=True,
	  limit_choices_to={'active_status': '1'},
	  )
	attendance_type = models.CharField(
		choices=status_choice,
		max_length=50,
		null=True,
		blank=True,
		verbose_name="Attendance Type",
	)

	login_type = models.CharField(
		choices=loginType,
		max_length=50,
		default = 'plain',
		verbose_name="Login Type",
	)

	active_status = models.BooleanField(
		default=1,
		verbose_name="Is Active")
	is_sound = models.BooleanField(
		default=0,
		verbose_name="Is Sound")
	facebook = models.CharField(
		max_length=255, 
		verbose_name='Facebook',\
		blank=True, null=True)
	instagram = models.CharField(
		max_length=255, 
		verbose_name='Instagram',\
		blank=True, null=True)
	twitter = models.CharField(
		max_length=255, 
		verbose_name='Twitter',\
		blank=True, null=True)
	created_at = models.DateTimeField(
		auto_now_add=True,
		blank=True,
		null=True,
		verbose_name='Creation Date')
	updated_at = models.DateTimeField(
		blank=True,
		null=True,
		verbose_name='Updation Date')
	is_payment = models.BooleanField(
		default=0,
		verbose_name="Is Payment")
	has_locality = models.BooleanField(
		default=0, 
		verbose_name="Has Locality")
	api_key = models.CharField(max_length=500, null=True, blank=True,unique=True)
	eion_brand_id = models.IntegerField(null=True, blank=True)

	class Meta:
		verbose_name = 'Brand'
		verbose_name_plural = 'Brands'

	def __str__(self):
		return str(self.company_name)

	def logo(self):
		if self.company_logo:
			return mark_safe('<img src='+MEDIA_URL+'%s width="50" height="50" />' % (self.company_logo))
			logo.allow_tags = True
		else:
			return 'No Image'
		logo.short_description = 'Company Logo'


	def banner(self):
		if self.company_landing_imge:
			return mark_safe('<img src='+MEDIA_URL+'%s width="50" height="50" />' % (self.company_landing_imge))
			logo.allow_tags = True
		else:
			return 'No Image'
		logo.short_description = 'Company Banner'


class Page(models.Model):
	# page = models.ForeignKey(
	# 	Independent_Page, 
	# 	on_delete=models.CASCADE,
	# 	related_name='Page_page', 
	# 	null=True,
	# 	blank=True)
	company = models.ForeignKey(
		'Brands.Company', 
		related_name='page_Company',
		on_delete=models.CASCADE,
		verbose_name='Company',
		limit_choices_to={'active_status':'1'})
	title = models.CharField(
		max_length=35, 
		verbose_name='Title')
	template = models.CharField(
		max_length=35, 
		verbose_name='Template')
	content = models.CharField(
		max_length=1000, 
		verbose_name='Content',
		null=True, 
		blank=True)
	active_status = models.BooleanField(
		default=1,
		verbose_name="Is Active")
	created_at = models.DateTimeField(
		auto_now_add=True,
		blank=True,
		null=True,
		verbose_name='Creation Date')
	updated_at = models.DateTimeField(
		blank=True,
		null=True,
		verbose_name='Updation Date')

	class Meta:
		verbose_name = 'Page'
		verbose_name_plural = 'Pages'

	def __str__(self):
		return self.title


class HomePage(models.Model):
	company = models.ForeignKey(
		'Brands.Company', 
		related_name='HomePage_Company',
		on_delete=models.CASCADE,
		verbose_name='Company',
		limit_choices_to={'active_status':'1'})
	home = models.CharField(
		max_length=1000,
		blank=True,null=True, 
		verbose_name='home')
	web_slider =  models.ImageField(
		upload_to='webimage/', 
		verbose_name='Hello Image For Web', 
		null=True,blank=True)
	mobile_slider =  models.ImageField(
		upload_to='mobileimage/', 
		verbose_name='Hello Image For Mobile', 
		null=True,blank=True)
	carousel_text = models.CharField(
		max_length=1000,
		blank=True,null=True, 
		verbose_name='Carousel Text')
	carousel_image =  models.ImageField(
		upload_to='carouselImage/', 
		verbose_name='Carousel Image', 
		null=True,blank=True)

	carousel_text1 = models.CharField(
		max_length=1000,
		blank=True,null=True, 
		verbose_name='Carousel Text1')
	carousel_image1 =  models.ImageField(
		upload_to='carouselImage/', 
		verbose_name='CarouselImage', 
		null=True,blank=True)

	health_text = models.CharField(
		max_length=1000,
		blank=True,
		null=True, 
		verbose_name='Carousel Text1')
	health_image =  models.ImageField(
		upload_to='HealthImage/', 
		verbose_name='Health Image', 
		null=True,blank=True)

	promotions_url = models.CharField(
		max_length=1000,
		blank=True,
		null=True, 
		verbose_name='Promotions Url')

	is_promotions = models.BooleanField(
		default=0,
		verbose_name="Is Promotions")
	active_status = models.BooleanField(
		default=1,
		verbose_name="Is Active")
	created_at = models.DateTimeField(
		auto_now_add=True,
		blank=True,
		null=True,
		verbose_name='Creation Date')
	updated_at = models.DateTimeField(
		blank=True,
		null=True,
		verbose_name='Updation Date')

	def _str_(self):
		return str(self.company)

	class Meta:
		verbose_name = 'Homepage'
		verbose_name_plural = '  Homepage'



class HomepagePromotion(models.Model):
	homepage = models.ForeignKey(
		HomePage, 
		related_name='HomepagePromotion_homepage',
		on_delete=models.CASCADE,
		verbose_name='Home Page',
		limit_choices_to={'active_status':'1'})
	promotions_image =  models.ImageField(
		upload_to='promotions/', 
		verbose_name='Promotions Image', 
		null=True,
		blank=True)

	def _str_(self):
		return str(self.homepage)

	class Meta:
		verbose_name = 'Homepage Promotions'
		verbose_name_plural = '  Homepage Promotions'




class MergeBrand(Common):
	name = models.CharField(
		max_length=200,
		verbose_name='Name')
	company = models.ManyToManyField(Company)

	class Meta:
		verbose_name='    Merge Brand'
		verbose_name_plural='    Merge Brand'

	def __str__(self):
		return self.name

	def get_brand(self):
		return ", ".join([p.company_name for p in self.company.all()])



class OutOfRange(Common):
	address = models.CharField(
		max_length=500,
		verbose_name='Address')
	company = models.ForeignKey(
		'Brands.Company', 
		related_name='OutOfRange_Company',
		on_delete=models.CASCADE,
		verbose_name='Company',
		limit_choices_to={'active_status':'1'})
	class Meta:
		verbose_name='    Out Of Range'
		verbose_name_plural='    Out Of Range'

	def __str__(self):
		return self.address


class ReviewMaster(models.Model):
	rating = models.CharField(
		max_length=20,
		verbose_name='Rating',
		null=True,
		blank=True)
	review = models.CharField(
		max_length=400,
		verbose_name='Review',
		null=True,
		blank=True)
	product = models.ForeignKey(
		'Product.Product', 
		related_name='Review_product',
		on_delete=models.CASCADE,
		verbose_name='Product')
	company = models.ForeignKey(
		'Brands.Company', 
		related_name='Reviewmaster_comppany',
		on_delete=models.CASCADE,
		verbose_name='Company',
		limit_choices_to={'active_status':'1'})
	outlet = models.ForeignKey(
		'Outlet.OutletProfile', 
		related_name='Review_outlet',
		on_delete=models.CASCADE,
		verbose_name='Company')
	customer = models.ForeignKey(
		'Customers.CustomerProfile', 
		related_name='Review_customer',
		on_delete=models.CASCADE,
		verbose_name='Customer')
	active_status = models.BooleanField(
		default=0, 
		verbose_name='Is Active')
	is_approve = models.BooleanField(
		default=0, 
		verbose_name='Is Approve')
	class Meta:
		verbose_name = 'ReviewMaster'
		verbose_name_plural = 'ReviewMaster'

	def __str__(self):
		return str(self.active_status)



class LinkedAccount(models.Model):
	Account_Name_Rzp = models.CharField(max_length=500, blank=True, null=True)
	Account_Email = models.CharField(max_length=500, blank=True, null=True)
	brand = models.ForeignKey(
		'Brands.Company', 
		related_name='brand_linked_accs',
		on_delete=models.CASCADE,
		verbose_name='Company',
		limit_choices_to={'active_status':'1'})
	BranchIFSC_Code = models.CharField(max_length=500, blank=True, null=True)
	Account_Number = models.CharField(max_length=500, blank=True, null=True)
	Beneficiary_Name = models.CharField(max_length=500, blank=True, null=True)
	acc_id = models.CharField(max_length=500, blank=True, null=True)
	is_verified = models.BooleanField(default=False)
	isStartedUsingEion = models.BooleanField(default=0)
	active_status = models.BooleanField(default=1)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name = "Linked Account"
		verbose_name_plural = "Linked Accounts"

	def __str__(self):
		if self.acc_id:
			return str(self.Account_Name_Rzp+"-"+self.acc_id)
		return str(self.Account_Name_Rzp+"-Not Verified")



class RouteTrack(models.Model):
	brand = models.ForeignKey(
		'Brands.Company', 
		related_name='brand_route_accs',
		on_delete=models.CASCADE,
		verbose_name='Company',
		limit_choices_to={'active_status':'1'})
	transfer_choices = (
		("Processed", "Processed"),
		("Scheduled", "Scheduled"),
	)
	status = models.CharField(max_length=200, blank=True, null=True,choices=transfer_choices)
	rzp_response = JSONField(blank=True, null=True)
	transfer_rzp_response = JSONField(blank=True, null=True)
	amount = models.CharField(max_length=200, blank=True, null=True)
	currency = models.ForeignKey(
		"Configuration.CurrencyMaster",
		on_delete=models.CASCADE,
		blank=True,
		null=True,
		related_name="route_cuurency",
	)
	Order_description = models.CharField(max_length=2000, blank=True, null=True)
	reference_id = models.CharField(max_length=500, null=True, blank=True,unique=True)
	transfer_id = models.CharField(max_length=200, blank=True, null=True)
	Payment_id = models.CharField(max_length=200, blank=True, null=True)
	Payment_link_id= models.CharField(max_length=200, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	customer_details = models.CharField(max_length=2000, blank=True, null=True,)

	def __str__(self):
		return str(self.Payment_link_id)

	class Meta:
		ordering = ['created_at']
