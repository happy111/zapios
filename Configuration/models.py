from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField,JSONField
from django.core.validators import MinValueValidator, MaxValueValidator


class BusinessType(models.Model):
	business_type = models.CharField(
		max_length=50, 
		verbose_name='Business Type',
		unique=True)
	description = models.CharField(
		max_length=200, 
		null=True, 
		blank=True, 
		verbose_name='Description')
	active_status = models.BooleanField(
		default=1, 
		verbose_name='Is Active')
	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(
		null=True, 
		blank=True, 
		verbose_name='Updation Date & Time')

	class Meta:
		verbose_name = '    Brand Type'
		verbose_name_plural = '    Brand Types'
		ordering = ['business_type']


	def __str__(self):
		return self.business_type


class CurrencyMaster(models.Model):
	currency = models.CharField(
		max_length=30,blank=True, null=True,
		verbose_name="Currency")
	symbol = models.CharField(
		max_length=20, 
		verbose_name="Symbol",blank=True, null=True)
	hexsymbol = models.CharField(
		max_length=7, 
		verbose_name='Hex Symbol',
		blank=True, null=True)
	active_status = models.BooleanField(
		default=1, 
		verbose_name='Is Active')
	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(
		null=True, 
		blank=True, 
		verbose_name='Updation Date & Time')

	class Meta:
		verbose_name = "   Currency"
		verbose_name_plural = "   Currencies"

	def __str__(self):
		return self.currency



class PaymentDetails(models.Model):
	name = models.CharField(
		max_length=50, 
		null=True, 
		blank=True, 
		verbose_name="Payment Gateway Name")
	company = models.ForeignKey(
		'Brands.Company', 
		related_name='PaymentDetails_Company',
		on_delete=models.CASCADE,
		verbose_name='Company',
		limit_choices_to={'active_status':'1'})
	username = models.CharField(
		max_length=50, 
		null=True, 
		blank=True, 
		verbose_name="User Name")
	keyid = models.CharField(
		max_length=50, 
		null=True, 
		blank=True, 
		verbose_name="keyId")
	keySecret = models.CharField(
		max_length=50, 
		null=True,
		blank=True, 
		verbose_name="keySecret")
	symbol = models.CharField(
		max_length=50, 
		null=True, 
		blank=True, 
		verbose_name="Currency")
	product_method = ArrayField(
		models.CharField(max_length=1000), 
		blank=True,null=True)
	active_status = models.BooleanField(
		default=1, 
		verbose_name='Is Active')
	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(
		null=True, 
		blank=True, 
		verbose_name='Updation Date & Time')

	class Meta:
		verbose_name = "   Payment Credential"
		verbose_name_plural = "   Payment Credential"

	def __str__(self):
		return str(self.company)


class ColorSetting(models.Model):
	accent_color = models.CharField(
		max_length=20, 
		null=True, 
		blank=True, 
		verbose_name="Accent color")
	textColor = models.CharField(
		max_length=20,
		null=True, 
		blank=True, 
		verbose_name="Text color")
	secondaryColor = models.CharField(
		max_length=20, 
		null=True, 
		blank=True, 
		verbose_name="Secondary color")
	company = models.OneToOneField(
		'Brands.Company', 
		related_name='ColorSetting_Company',
		on_delete=models.CASCADE,
		verbose_name='Company',
		limit_choices_to={'active_status':'1'})
	active_status = models.BooleanField(
		default=1, 
		verbose_name='Is Active')
	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(
		null=True, 
		blank=True, 
		verbose_name='Updation Date & Time')

	class Meta:
		verbose_name = "   Accent Color"
		verbose_name_plural = "   Color Setting"

	def __str__(self):
		return str(self.company) 



class DeliverySetting(models.Model):
	price_type = models.CharField(
		max_length=50, 
		null=True, 
		blank=True, 
		verbose_name="Price Type")
	is_tax = models.BooleanField(
		default=1,
		verbose_name='Is Tax')
	tax = JSONField(
		blank=True,
		null=True,
		verbose_name='Tax')
	delivery_charge = models.FloatField(
		blank=True,
		null=True,
		default=0,
		verbose_name='Delivery Charge')
	package_charge = models.FloatField(
		blank=True,
		null=True,
		default=0,
		verbose_name='Package Charge')
	company = models.OneToOneField(
		'Brands.Company', 
		related_name='DeliverySetting_Company',
		on_delete=models.CASCADE,
		verbose_name='Company',
		limit_choices_to={'active_status':'1'})
	symbol = models.CharField(
		max_length=50,
		null=True, 
		blank=True, 
		verbose_name="Currency")
	active_status = models.BooleanField(
		default=1, 
		verbose_name='Is Active')
	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(
		null=True, 
		blank=True, 
		verbose_name='Updation Date & Time')

	class Meta:
		verbose_name = "   Delivery Setting"
		verbose_name_plural = "   Delivery Settings"

	def __str__(self):
		return str(self.delivery_charge)

class AnalyticsSetting(models.Model):
	company = models.ForeignKey(
		'Brands.Company', 
		related_name='AnalyticsSetting_Company',
		on_delete=models.CASCADE,
		verbose_name='Company',
		limit_choices_to={'active_status':'1'})
	u_id = models.CharField(
		max_length=255,
		null=True, 
		blank=True, 
		verbose_name="Analytics U Id")
	analytics_snippets = models.TextField(
		null=True, 
		blank=True, 
		verbose_name="Analytics Snippet")
	active_status = models.BooleanField(
		default=1, 
		verbose_name='Is Active')
	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(
		null=True, 
		blank=True, 
		verbose_name='Updation Date & Time')

	class Meta:
		verbose_name = "   Google Analytics Setting"
		verbose_name_plural = "   Google Analytics Settings"

	def __str__(self):
		return str(self.u_id)


class EmailSetting(models.Model):
	company = models.ForeignKey(
		'Brands.Company', 
		related_name='EmailSetting_Company',
		on_delete=models.CASCADE,
		verbose_name='Company',
		limit_choices_to={'active_status':'1'})
	title = models.CharField(
		max_length=255,
		null=True, 
		blank=True, 
		verbose_name="Title")
	image = models.ImageField(
		upload_to='EmailSetting',
		null=True, 
		blank=True, 
		verbose_name='image')
	content = models.CharField(
		max_length=255,
		null=True,
		blank=True,
		verbose_name="Content")
	thank = models.CharField(
		max_length=255,
		null=True, 
		blank=True, 
		verbose_name="thank")
	dis_content = models.CharField(
		max_length=255,
		null=True, 
		blank=True, 
		verbose_name="Discount Content")
	coupon = models.ForeignKey(
		'discount.PercentOffers',
		null=True,
		blank=True, 
		related_name='EmailSetting_coupon',
		on_delete=models.CASCADE,
		verbose_name='Coupon',
		limit_choices_to={'active_status':'1'})
	active_status = models.BooleanField(
		default=1, 
		verbose_name='Is Active')
	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(
		null=True,
		blank=True, 
		verbose_name='Updation Date & Time')

	class Meta:
		verbose_name = " Email Setting"
		verbose_name_plural = " Email Settings"

	def __str__(self):
		return str(self.company)


class Excelimport(models.Model):
	title = models.CharField(
		max_length=255,
		null=True, 
		blank=True, 
		verbose_name="Title")
	image = models.ImageField(
		upload_to='import',
		null=True, 
		blank=True, 
		verbose_name='image')
	types = models.CharField(
		max_length=255,
		null=True, 
		blank=True, 
		verbose_name="Types")
	active_status = models.BooleanField(
		default=1, 
		verbose_name='Is Active')
	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(
		null=True, 
		blank=True, 
		verbose_name='Updation Date & Time')

	class Meta:
		verbose_name = "   Excel Import"
		verbose_name_plural = "   Excel Import"

	def __str__(self):
		return str(self.title)




class TaxSetting(models.Model):
	company = models.ForeignKey(
		'Brands.Company', 
		related_name='TaxSetting_Company',
		on_delete=models.CASCADE,
		verbose_name='Company',
		limit_choices_to={'active_status':'1'})
	tax_name = models.CharField(
		max_length=50, 
		null=True, 
		blank=True, 
		verbose_name="Tax Name")
	tax_percent = models.FloatField(
		verbose_name="Percentage",
		null=True, 
		blank=True)
	active_status = models.BooleanField(
		default=1, 
		verbose_name='Is Active')
	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(
		null=True, 
		blank=True, 
		verbose_name='Updation Date & Time')

	class Meta:
		verbose_name = "   Tax Setting"
		verbose_name_plural = "   Tax Settings"

	def __str__(self):
		return str(self.tax_name)


class HeaderFooter(models.Model):
	outlet = models.ForeignKey(
		'Outlet.OutletProfile',
		on_delete=models.CASCADE,
		verbose_name='Outlet',
		limit_choices_to={'active_status':'1'},
		blank=True, 
		null=True)
	company = models.ForeignKey(
		'Brands.Company', 
		related_name='HeaderFooter_Company',
		on_delete=models.CASCADE,
		verbose_name='Company',
		limit_choices_to={'active_status':'1'})
	header_text = models.TextField(
		null=True, 
		blank=True, 
		verbose_name="Header Text")
	footer_text = models.TextField(
		verbose_name="Footer Text",
		null=True, 
		blank=True)
	gst = models.CharField(
		max_length=50, 
		null=True, 
		blank=True, 
		verbose_name="GST")
	active_status = models.BooleanField(
		default=1, 
		verbose_name='Is Active')
	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(
		null=True, 
		blank=True, 
		verbose_name='Updation Date & Time')

	class Meta:
		verbose_name = "   Receipt Configuration"
		verbose_name_plural = "   Receipt Configuration"

	def __str__(self):
		return str(self.gst)

class PaymentMethod(models.Model):
	company = models.ForeignKey('Brands.Company', 
		related_name='PaymentMethod_Company',
		on_delete=models.CASCADE,
		verbose_name='Company',
		limit_choices_to={'active_status':'1'})
	country = models.ForeignKey('Location.CountryMaster',  
		null=True, 
		blank=True,
		on_delete=models.CASCADE,
		related_name='PaymentMethod_country',
		limit_choices_to={
		'active_status': '1'},
		verbose_name='Country')
	symbol = models.CharField(
		max_length=20, 
		verbose_name="Symbol", 
		null=True, 
		blank=True,)
	payment_logo = models.ImageField(
		upload_to='payment_logo',
		null=True, 
		blank=True, 
		verbose_name='payment Logo')
	payment_method = models.CharField(
		max_length=50, 
		null=True, 
		blank=True, 
		verbose_name="Payment Method")
	word_limit = models.CharField(
		max_length=50, 
		null=True, 
		blank=True, 
		verbose_name="Character Limit")
	keyid = models.CharField(
		max_length=50, 
		null=True, 
		blank=True, 
		verbose_name="keyId")
	keySecret = models.CharField(
		max_length=50, 
		null=True, 
		blank=True, 
		verbose_name="keySecret")
	active_status = models.BooleanField(
		default=0, 
		verbose_name='Is Active')
	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(
		null=True, 
		blank=True, 
		verbose_name='Updation Date & Time')

	class Meta:
		verbose_name = "   Payment Method"
		verbose_name_plural = "   Payment Method"

	def __str__(self):
		return str(self.payment_method)


class PaymentStatus(models.Model):
	payment_id = models.CharField(
		max_length=250, 
		blank=True, 
		null=True)
	is_success = models.BooleanField(default=0)
	created_at = models.DateTimeField(
		auto_now_add=True, 
		verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(
		auto_now=True, 
		null=True, 
		blank=True, 
		verbose_name='Updation Date & Time')


class Unit(models.Model):
	unit_name = models.CharField(
		max_length=50, 
		null=True, 
		blank=True, 
		verbose_name='Unit Name')
	short_name = models.CharField(
		max_length=50, 
		null=True, 
		blank=True, 
		verbose_name='Short Name')
	unit_details = JSONField(
		blank=True,
		null=True)
	company = models.ForeignKey(
		'Brands.Company', 
		related_name='Unit_Company',
		on_delete=models.CASCADE,
		verbose_name='Company',
		limit_choices_to={'active_status':'1'})
	active_status = models.BooleanField(
		default=1, 
		verbose_name='Is Active')
	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(
		null=True, 
		blank=True, 
		verbose_name='Updation Date & Time')

	class Meta:
		verbose_name = '    Unit'
		verbose_name_plural = '    Unit'



	def __str__(self):
		return self.unit_name




class OrderSource(models.Model):
	company = models.ForeignKey(
		'Brands.Company', 
		related_name='OrderSource_Company',
		on_delete=models.CASCADE,
		verbose_name='Company',
		limit_choices_to={'active_status':'1'}
		)
	source_name = models.CharField(
		max_length=50, 
		null=True, 
		blank=True,
		verbose_name="Source Name")
	image = models.ImageField(
		upload_to='source',
		null=True, 
		blank=True, 
		verbose_name='image')
	priority = models.PositiveIntegerField(
		validators=[MinValueValidator(1),MaxValueValidator(100),], 
		verbose_name='Priority', 
		null=True, 
		blank=True)
	payment_method = ArrayField(
		models.TextField(), 
		blank=True,null=True, 
		verbose_name="Payment Method")
	active_status = models.BooleanField(
		default=1, 
		verbose_name='Is Active')
	is_edit = models.BooleanField(
		default=0, 
		verbose_name='Is Status')
	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(
		null=True, 
		blank=True, 
		verbose_name='Updation Date & Time')

	class Meta:
		verbose_name = "   OrderSource"
		verbose_name_plural = "   OrderSource"

	def __str__(self):
		return str(self.source_name)


class ProductWeightage(models.Model):
	company = models.ForeignKey(
		'Brands.Company', 
		related_name='ProductWeightage_Company',
		on_delete=models.CASCADE,
		verbose_name='Company',
		limit_choices_to={'active_status':'1'})
	product_category = models.PositiveIntegerField(
		validators=[MinValueValidator(0),
		MaxValueValidator(50),], 
		verbose_name='Product Category', 
		default=0,null=True, 
		blank=True)
	product_subcategory = models.PositiveIntegerField(
		validators=[MinValueValidator(0),
		MaxValueValidator(50),], 
		verbose_name='Product Subcategory',
		default=0, null=True, 
		blank=True)
	product_name = models.PositiveIntegerField(
		validators=[MinValueValidator(0),
		MaxValueValidator(50),], 
		verbose_name='Product Name',
		default=0, null=True, 
		blank=True)
	food_type = models.PositiveIntegerField(
		validators=[MinValueValidator(0),
		MaxValueValidator(50),], 
		verbose_name='Food Type', 
		default=0,null=True, blank=True)
	priority = models.PositiveIntegerField(
		validators=[MinValueValidator(0),MaxValueValidator(50),], 
		verbose_name='Priority',
		default=0, 
		null=True,
		 blank=True)
	product_code = models.PositiveIntegerField(
		validators=[MinValueValidator(0),MaxValueValidator(50),], 
		verbose_name='Product Code', 
		default=0,
		null=True, 
		blank=True)
	product_desc = models.PositiveIntegerField(
		validators=[MinValueValidator(0),MaxValueValidator(50),], 
		verbose_name='Product Description',
		default=0,
		null=True,
		blank=True)
	allergen_Information = models.PositiveIntegerField(
		validators=[MinValueValidator(0),MaxValueValidator(50),], 
		verbose_name='Allergen Information',
		default=0,
		null=True, 
		blank=True)
	spice = models.PositiveIntegerField(
		validators=[MinValueValidator(0),MaxValueValidator(50),], 
		verbose_name='Spice', 
		null=True,
		default=0, 
		blank=True)
	kot_desc = models.PositiveIntegerField(
		validators=[MinValueValidator(0),MaxValueValidator(50),], 
		verbose_name='Kot Description',
		default=0, 
		null=True,
		blank=True)
	pvideo = models.PositiveIntegerField(
		validators=[MinValueValidator(0),MaxValueValidator(50),], 
		verbose_name='Product Video', 
		default=0,
		null=True, 
		blank=True)
	product_image = models.PositiveIntegerField(
		validators=[MinValueValidator(0),MaxValueValidator(50),], 
		verbose_name='Product Image',
		default=0, 
		null=True, 
		blank=True)
	tags = models.PositiveIntegerField(
		validators=[MinValueValidator(0),MaxValueValidator(50),], 
		verbose_name='Tags', 
		null=True,
		default=0, 
		blank=True)
	variant = models.PositiveIntegerField(
		validators=[MinValueValidator(0),MaxValueValidator(50),], 
		verbose_name='Variant', 
		null=True,
		default=0, 
		blank=True)
	price = models.PositiveIntegerField(
		validators=[MinValueValidator(0),MaxValueValidator(50),], 
		verbose_name='Price', 
		null=True,
		default=0, 
		blank=True)
	discount_price = models.PositiveIntegerField(
		validators=[MinValueValidator(0),MaxValueValidator(50),], 
		verbose_name='Compare at price',
		default=0, 
		null=True, 
		blank=True)
	discount_price = models.PositiveIntegerField(
		validators=[MinValueValidator(0),MaxValueValidator(50),], 
		verbose_name='Compare at price',
		default=0, 
		null=True,
		blank=True)
	variant_deatils = models.PositiveIntegerField(
		validators=[MinValueValidator(0),MaxValueValidator(50),], 
		verbose_name='Variant Details',
		default=0,
		null=True, 
		blank=True)
	addpn_grp_association = models.PositiveIntegerField(
		validators=[MinValueValidator(0),MaxValueValidator(50),], 
		verbose_name='Addon Group Association',
		default=0,
		null=True, 
		blank=True)
	tax_association = models.PositiveIntegerField(
		validators=[MinValueValidator(0),MaxValueValidator(50),], 
		verbose_name='Tax', 
		null=True, 
		default=0,
		blank=True)
	outlet_map = models.PositiveIntegerField(
		validators=[MinValueValidator(0),MaxValueValidator(50),], 
		verbose_name='Outlet', 
		null=True,
		default=0, 
		blank=True)
	is_recommended = models.PositiveIntegerField(
		validators=[MinValueValidator(0),MaxValueValidator(50),], 
		verbose_name='Recommended', 
		null=True,
		default=0, 
		blank=True)
	included_platform = models.PositiveIntegerField(
		validators=[MinValueValidator(0),MaxValueValidator(50),], 
		verbose_name='Included PlatForm',
		default=0, 
		null=True, 
		blank=True)
	product_schema = models.PositiveIntegerField(
		validators=[MinValueValidator(0),MaxValueValidator(50),], 
		verbose_name='Nutritional Information',
		default=0, 
		null=True, 
		blank=True)
	primaryIngredient_deatils = models.PositiveIntegerField(
		validators=[MinValueValidator(0),MaxValueValidator(50),], 
		verbose_name='PrimaryIngredient Details', 
		default=0,
		null=True, 
		blank=True)
	active_status = models.BooleanField(
		default=1, 
		verbose_name='Is Active')
	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(
		null=True, 
		blank=True, 
		verbose_name='Updation Date & Time')

	class Meta:
		verbose_name = "   ProductWeightage"
		verbose_name_plural = "   ProductWeightage"
		unique_together = ('company',)

	def __str__(self):
		return str(self.company)

class WebsiteStatistic(models.Model):
	name = models.CharField(
		max_length=50, 
		null=True, 
		blank=True, 
		verbose_name='No Of visitors')
	visitors = models.CharField(
		max_length=50, 
		null=True, 
		blank=True, 
		verbose_name='No Of visitors')
	menu_views = models.CharField(
		max_length=50, 
		null=True, 
		blank=True,
		verbose_name='No Of Menu Views')
	checkout = models.CharField(
		max_length=50, 
		null=True, 
		blank=True,
		verbose_name='checkout')
	online_order = models.CharField(
		max_length=50, 
		null=True, 
		blank=True,
		verbose_name='Online Orders')
	company = models.ForeignKey(
		'Brands.Company', 
		related_name='Company',
		on_delete=models.CASCADE,
		verbose_name='Company',
		limit_choices_to={'active_status':'1'})
	active_status = models.BooleanField(
		default=1, 
		verbose_name='Is Active')
	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(
		null=True, 
		blank=True, 
		verbose_name='Updation Date & Time')

	class Meta:
		verbose_name = '    name'
		verbose_name_plural = '    name'


	def __str__(self):
		return self.name


class AttendanceConfig(models.Model):
	fullday = models.TimeField(
		auto_now=False, 
		auto_now_add=False,
		verbose_name='Full Day')
	halfday = models.TimeField(
		auto_now=False, 
		auto_now_add=False,
		verbose_name='Half Day')
	company = models.ForeignKey(
		'Brands.Company', 
		related_name='AttendanceConfig',
		on_delete=models.CASCADE,
		verbose_name='Company',
		limit_choices_to={'active_status':'1'})

	active_status = models.BooleanField(
		default=1, 
		verbose_name='Is Active')
	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(
		null=True, 
		blank=True, 
		verbose_name='Updation Date & Time')

	class Meta:
		verbose_name = "   AttendanceConfig"
		verbose_name_plural = "   AttendanceConfig"

	def __str__(self):
		return str(self.company)

class TokenExpire(models.Model):
	url = models.CharField(
		max_length=500, 
		null=True, 
		blank=True,
		verbose_name='url')
	token_creation_time = models.DateTimeField(
		blank=True, 
		null=True,
		verbose_name='Creation Date')
	token_use_time = models.DateTimeField(
		blank=True, 
		null=True,
		verbose_name='Token Use time')
	active_status = models.BooleanField(
		default=0, 
		verbose_name='Is Active')

	class Meta:
		verbose_name = 'Token Expire Manager'
		verbose_name_plural = 'Token Expire Manager'

	def __str__(self):
		return str(self.url)


class UserExperience(models.Model):
	email = models.CharField(
		max_length=500, 
		null=True, 
		blank=True,
		verbose_name='url')
	mobile = models.CharField(
		max_length=20,
		verbose_name='Mobile No',
		null=True,
		blank=True)
	rating = models.CharField(
		max_length=20,
		verbose_name='Rating',
		null=True,
		blank=True)
	company = models.ForeignKey(
		'Brands.Company', 
		related_name='UserExperience_comppany',
		on_delete=models.CASCADE,
		verbose_name='Company',
		limit_choices_to={'active_status':'1'})


	active_status = models.BooleanField(
		default=0, 
		verbose_name='Is Active')

	class Meta:
		verbose_name = 'UserExperience'
		verbose_name_plural = 'UserExperience'

	def __str__(self):
		return str(self.email)



class Common(models.Model):
	active_status = models.BooleanField(
		default=True, 
		verbose_name='Is Active')
	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(
		null=True, 
		blank=True, 
		verbose_name='Updation Date & Time')

	class Meta:
	  abstract = True

class OnlinepaymentStatus(Common):
	status_choice = (
		("delivery", "delivery"),
		("pickup", "pickup"),

	)
	types = models.CharField(
		choices=status_choice,
		max_length=50,
		verbose_name="Type",
	)
	payment = models.ForeignKey(
		PaymentMethod, 
		on_delete=models.CASCADE,
		related_name='OnlinepaymentStatus_payment', 
		null=True,
		blank=True)
	company = models.ForeignKey(
		'Brands.Company', 
		related_name='OnlinepaymentStatus_comppany',
		on_delete=models.CASCADE,
		verbose_name='Company',
		limit_choices_to={'active_status':'1'})
	is_hide = models.BooleanField(
		default=False, 
		verbose_name='Is Hide')

	class Meta:
		verbose_name = 'OnlinepaymentStatus'
		verbose_name_plural = '  OnlinepaymentStatus'
		unique_together = ('company', 'types','payment')

	def __str__(self):
		return str(self.types)
	


# Create your models here.
class Address(models.Model):
	pincode = models.CharField(
		max_length=150, 
		null=True, 
		blank=True,
		verbose_name='Pincode')

	prefecture = models.CharField(
		max_length=150, 
		null=True, 
		blank=True,
		verbose_name='Prefecture')

	city = models.CharField(
		max_length=150, 
		null=True, 
		blank=True,
		verbose_name='City')

	address = models.CharField(
		max_length=150, 
		null=True, 
		blank=True,
		verbose_name='Address')

	class Meta:
		verbose_name = 'Address'
		verbose_name_plural = '  Address'


	def __str__(self):
		return str(self.pincode)

