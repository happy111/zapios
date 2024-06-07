from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.safestring import mark_safe
from zapio.settings import MEDIA_URL
from Brands.models import Company
from Product.models import *
from django.contrib.postgres.fields import ArrayField,JSONField


class Coupon(models.Model):
	coupon_type = models.CharField(
		max_length=50, 
		verbose_name='Coupon Type',
		null=True, 
		blank=True)
	coupon_code = models.CharField(
		max_length=50, 
		verbose_name='Coupon Code',
		null=True, blank=True)
	frequency = models.PositiveIntegerField(
		validators=[MinValueValidator(0),MaxValueValidator(10000),], 
		verbose_name='Frequency', 
		null=True, blank=True)
	valid_frm = models.DateTimeField(
		null=True, 
		blank=True,
		verbose_name='Valid From')
	valid_till = models.DateTimeField(
		null=True, 
		blank=True, 
		verbose_name='Valid Till')
	category = models.ForeignKey(
		ProductCategory, 
		related_name='category_Coupon',
		on_delete=models.CASCADE,
		verbose_name='category',
		limit_choices_to={'active_status':'1'},
		null=True, blank=True)
	Company = models.ForeignKey(
		Company, 
		related_name='Coupon_Company',
		on_delete=models.CASCADE,
		verbose_name='Company',
		limit_choices_to={'active_status':'1'})
	product_map = ArrayField(
		models.CharField(max_length=200), 
		blank=True, 
		verbose_name="Product Mapped Ids")
	flat_discount = models.CharField(
		max_length=200,
		verbose_name='Flat Discount', 
		null=True, blank=True)
	flat_percentage = models.CharField(
		max_length=200,
		verbose_name='Percentage Discount', 
		null=True, blank=True)
	user_map = ArrayField(
		models.CharField(max_length=1000), 
		blank=True,null=True)
	outlet_id = ArrayField(
		models.CharField(max_length=1000), 
		blank=True,null=True)
	is_min_shop = models.BooleanField(
		verbose_name='Is Min Shopping Based', 
		blank=True,null=True)
	is_automated = models.BooleanField(
		verbose_name='Is Automated', 
		blank=True,null=True)
	min_shoping = models.FloatField(
		blank=True,
		null=True,
		verbose_name='Minimum Shopping')
	max_shoping = models.FloatField(
		blank=True,
		null=True,
		verbose_name='Maximum Shopping')
	is_banner = models.BooleanField(
		null=True, 
		blank=True, 
		verbose_name='Is Banner')

	image =  models.ImageField(
		upload_to='coupon_image/', 
		verbose_name='Image', 
		null=True,blank=True)
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
		verbose_name = 'Coupon'
		verbose_name_plural = '   Coupons'

	def __str__(self):
		return self.coupon_code


class QuantityCombo(models.Model):
	combo_name =  models.CharField(
		max_length=100, 
		verbose_name='Combo Name',
		null=True,
		blank=True)
	product = models.ForeignKey(
		'Product.Product', 
		related_name='Product_QuantityCombo',
		on_delete=models.CASCADE,
		verbose_name='Main Product',
		limit_choices_to={'active_status':'1'})
	free_product = models.ForeignKey(
		'Product.Product', 
		related_name='F_Product_QuantityCombo',
		on_delete=models.CASCADE,
		verbose_name='Free Product',
		limit_choices_to={'active_status':'1'})
	product_quantity = models.PositiveIntegerField(validators=\
						[MinValueValidator(1),MaxValueValidator(10000),], 
						verbose_name='Product Quantity',
						null=True,
						blank=True)
	free_pro_quantity = models.PositiveIntegerField(validators=\
						[MinValueValidator(1),
						MaxValueValidator(10000),], 
						verbose_name='Free Product Quantity', 
						null=True, blank=True)
	Company = models.ForeignKey(Company, 
		related_name='QuantityCombo_Company',
		on_delete=models.CASCADE,
		verbose_name='Company',
		limit_choices_to={'active_status':'1'})
	valid_frm = models.DateTimeField(
		null=True, 
		blank=True,
		verbose_name='Valid From')
	valid_till = models.DateTimeField(
		null=True, 
		blank=True, 
		verbose_name='Valid Till')
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
		verbose_name = 'Combo'
		verbose_name_plural = '  Quantity Based Combo'

	def __str__(self):
		return self.coupon_code


class PercentCombo(models.Model):
	pcombo_name =  models.CharField(
		max_length=100, 
		verbose_name='Combo Name',
		null=True, 
		blank=True)
	product = models.ForeignKey(
		'Product.Product', 
		related_name='Product_PercentCombo',
		on_delete=models.CASCADE,
		verbose_name='Main Product',
		limit_choices_to={'active_status':'1'})
	discount_product = models.ForeignKey(
		'Product.Product', 
		related_name='D_Product_PercentCombo',
		on_delete=models.CASCADE,
		verbose_name='Discounted Product',
		limit_choices_to={'active_status':'1'})
	discount_percent = models.PositiveIntegerField(validators=\
						[MinValueValidator(1),MaxValueValidator(100),], 
						verbose_name='Discount Percentage', 
						null=True, blank=True)
	valid_frm = models.DateTimeField(
		null=True, 
		blank=True,
		verbose_name='Valid From')
	valid_till = models.DateTimeField(
		null=True, 
		blank=True, 
		verbose_name='Valid Till')
	Company = models.ForeignKey(Company, 
		related_name='PercentCombo_Company',
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
		verbose_name = 'Combo'
		verbose_name_plural = ' Percentage Based Combo'

	def __str__(self):
		return self.combo_name


class PercentOffers(models.Model):
	offer_name =  models.CharField(
		max_length=100, 
		verbose_name='Coupon Code',
		null=True, 
		blank=True)
	category = models.ForeignKey(
		ProductCategory, 
		related_name='PercentOffer_Category',
		null=True, 
		blank=True,
		on_delete=models.CASCADE,
		verbose_name='Category',
		limit_choices_to={'active_status':'1'})
	discount_percent = models.PositiveIntegerField(validators=\
						[MinValueValidator(1),MaxValueValidator(100),], 
						verbose_name='Discount Percentage', 
						null=True, 
						blank=True)
	company = models.ForeignKey(
		'Brands.Company', 
		related_name='PercentOffer_Company',
		on_delete=models.CASCADE,
		verbose_name='Company',
		limit_choices_to={'active_status':'1'})
	valid_till = models.DateTimeField(
		null=True, 
		blank=True, 
		verbose_name='Valid Till')

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
		verbose_name = 'PercentageOffer'
		verbose_name_plural = ' PercentageOffer'

	def __str__(self):
		return str(self.offer_name)




class Discount(models.Model):

	discount_name =  models.CharField(
		max_length=150, 
		verbose_name='Discount Name',
		null=True, 
		blank=True)
	discount_type = models.CharField(
		choices=(('Flat', 'Flat'), 
			('Percentage', 'Percentage')
		),
		max_length=20,
		verbose_name="Coupon Type",
		null=True,
		blank=True)
	user_roll = ArrayField(
		models.CharField(max_length=200), 
		blank=True, 
		null=True,
		verbose_name="User Roll")
	valid_frm = models.DateTimeField(
		null=True, 
		blank=True,
		verbose_name='Valid From')
	valid_till = models.DateTimeField(
		null=True,
		 blank=True, 
		 verbose_name='Valid Till')
	Company = models.ForeignKey(Company, 
		related_name='Discount_Company',
		on_delete=models.CASCADE,
		verbose_name='Company',
		limit_choices_to={'active_status':'1'})
	category_map = ArrayField(models.CharField(
		max_length=200),
		blank=True, 
		null=True, 
		verbose_name="Category")
	product_map = ArrayField(
		models.CharField(max_length=200), 
		blank=True, 
		verbose_name="Product Mapped Ids")
	flat_discount = models.CharField(
		max_length=200,
		verbose_name='Flat Discount', 
		null=True, 
		blank=True)
	flat_percentage = models.CharField(
		max_length=200,
		verbose_name='Percentage Discount', 
		null=True,
		blank=True)
	outlet_id = ArrayField(
		models.CharField(max_length=1000), 
		blank=True,
		null=True)
	is_min_shop = models.BooleanField(
		verbose_name='Is Min Shopping Based', 
		blank=True,
		null=True)
	is_reason_required = models.BooleanField(
		verbose_name='Is Reason Required', 
		blank=True,
		null=True)
	min_shoping = models.FloatField(
		blank=True,
		null=True,
		verbose_name='Minimum Shopping')
	max_shoping = models.FloatField(
		blank=True,
		null=True,
		verbose_name='Maximum Shopping')
	active_status = models.BooleanField(
		default=1, 
		verbose_name='Is Active')
	is_all_category = models.BooleanField(
		null=True, 
		blank=True, 
		verbose_name='Is All Category')
	is_all_product = models.BooleanField(
		null=True, 
		blank=True, 
		verbose_name='Is All Product')
	
	is_banner = models.BooleanField(
		null=True, 
		blank=True, 
		verbose_name='Is Banner')

	image =  models.ImageField(
		upload_to='discount_image/', 
		verbose_name='Image', 
		null=True,blank=True)

	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(
		null=True, 
		blank=True, 
		verbose_name='Updation Date & Time')

	class Meta:
		verbose_name = 'discount_name'
		verbose_name_plural = '   discount_name'

	def __str__(self):
		return self.discount_name


class DiscountReason(models.Model):
	reason =  models.TextField(
		max_length=100, 
		verbose_name='Reason',
		null=True, 
		blank=True)
	Company = models.ForeignKey(
		Company, 
		related_name='DiscountReason_Company',
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
		verbose_name = 'Discount '
		verbose_name_plural = '   Discount Reason'

	def __str__(self):
		return self.reason
