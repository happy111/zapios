from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.safestring import mark_safe
from zapio.settings import MEDIA_URL
from Brands.models import Company
from django.contrib.postgres.fields import ArrayField,JSONField
from Outlet.models import OutletProfile



class ProductCategory(models.Model):
	category_name = models.CharField(
		max_length=50, 
		verbose_name='Category Name')
	category_code = models.CharField(
		max_length=20, 
		verbose_name='Category Code',
		null=True, 
		blank=True,)
	category_image =  models.ImageField(
		upload_to='category_image/', 
		verbose_name='Image', 
		null=True,blank=True)
	Company = models.ForeignKey(
		Company, 
		related_name='category_Company',
		on_delete=models.CASCADE,verbose_name='Company',
		limit_choices_to={'active_status':'1'})
	outlet_map = ArrayField(
		models.TextField(),
		null=True, 
		blank=True, 
		verbose_name="Outlet Mapped Ids")
	description = models.CharField(max_length=200, 
		null=True, 
		blank=True, 
		verbose_name='Description')
	priority = models.PositiveIntegerField(
		null=True, 
		blank=True, 
		verbose_name='Priority')
	is_hide = models.BooleanField(
		default=0, 
		verbose_name='Is Hide')

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
			verbose_name = 'Category'
			verbose_name_plural = '             Categories'
			unique_together = ('category_name','Company')

	def __str__(self):
			if self.category_name:
					return self.category_name

class ProductsubCategory(models.Model):
	category = models.ForeignKey(
		ProductCategory, 
		related_name='Products_subcategory',
		on_delete=models.CASCADE,
		verbose_name='Category Name')
	subcategory_name = models.CharField(
		max_length=50, 
		verbose_name='Subcategory Name')
	subcategory_image =  models.ImageField(
		upload_to='subcategory_image/', 
		verbose_name='Image', 
		null=True,blank=True)
	
	Company = models.ForeignKey(
		Company, 
		related_name='Productsubcategory_Company',
		on_delete=models.CASCADE,
		verbose_name='Company',
		limit_choices_to={'active_status':'1'})
	priority = models.PositiveIntegerField(
		null=True, 
		blank=True,
		verbose_name='Priority')
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
	is_hide = models.BooleanField(
		default=0, 
		verbose_name='Is Hide')
	class Meta:
			verbose_name = '   Sub-Category'
			verbose_name_plural = '             Sub-Categories'

	def __str__(self):
			if self.subcategory_name:
					return self.subcategory_name


class FoodType(models.Model):
	food_type =  models.CharField(
		max_length=50, 
		verbose_name='Food Type Name',
		unique=True)
	foodtype_image = models.ImageField(
		upload_to='foodtype_images/images',
		verbose_name='Image (Short image)',
		blank=True, null=True,)
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
			verbose_name = 'Food Type'
			verbose_name_plural = ' Food Type'

	def __str__(self):
			return self.food_type

	def food_type_pic(self):
		if self.foodtype_image:
			return mark_safe('<img src='+MEDIA_URL+'%s width="25" height="25" />' %
									(self.foodtype_image))
			logo.allow_tags = True
		else:
			return 'No Image'
	food_type_pic.short_description = 'Food Type Image'


class Variant(models.Model):
	variant =  models.CharField(
		max_length=130, 
		verbose_name="Variant Measurement")
	description =  models.CharField(
		max_length=110, 
		null=True, 
		blank=True,
		verbose_name="Description")
	Company = models.ForeignKey(Company, 
		related_name='Variant_Company',
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

	def __str__(self):
			return self.variant

	class Meta:
			verbose_name = 'Variant'
			verbose_name_plural = ' Variants'


class AddonDetails(models.Model):
	addon_gr_name = models.CharField(
		max_length=50, 
		verbose_name='Addon Group Name')
	min_addons = models.PositiveIntegerField(
		validators=[MinValueValidator(0),MaxValueValidator(100)], 
		verbose_name='Minimum No. of Add-Ons', 
		null=True, 
		blank=True)
	max_addons = models.PositiveIntegerField(
		validators=[MinValueValidator(1),MaxValueValidator(100)], 
		verbose_name='Maximum No. of Add-Ons', 
		null=True, 
		blank=True)
	description = models.CharField(
		max_length=200, 
		blank=True, 
		verbose_name='Description')
	addons = ArrayField(
		models.TextField(), 
		null=True, 
		blank=True, 
		verbose_name="Addons"
	)
	active_status = models.BooleanField(
		default=1,
		null=True,
		blank=True,
		verbose_name="Is Active")
	created_at = models.DateTimeField(
		auto_now_add=True, 
		verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(
		blank=True, 
		null=True,
		verbose_name='Updation Date')

	def __str__(self):
		return self.addon_gr_name

	class Meta:
		verbose_name = 'Add-on Group'
		verbose_name_plural = '         Add-on Groups'


class Addons(models.Model):
	name = models.CharField(
		max_length=250, 
		verbose_name='Add-On Name',
		unique=True)
	addon_amount = models.FloatField(
		verbose_name='Add-On Amount')
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
		verbose_name = 'Add-on'
		verbose_name_plural = '  Add-ons'

	def __str__(self):
		return self.name


class Product(models.Model):
	product_categorys = ArrayField(
		models.CharField(max_length=1000), 
		blank=True,null=True)
	product_subcategorys = ArrayField(
		models.CharField(max_length=1000), 
		blank=True,null=True)
	product_name = models.CharField(
		max_length=100, 
		verbose_name='Product Name')
	food_type = models.ForeignKey(
		FoodType,
		on_delete=models.CASCADE, 
		blank=True,null=True,
		verbose_name='Product Type')
	priority = models.PositiveIntegerField(
		validators=[MinValueValidator(0),
		MaxValueValidator(10000),], 
		verbose_name='Priority', 
		null=True, 
		blank=True)
	Company = models.ForeignKey(Company, 
		related_name='Product_Company',
		on_delete=models.CASCADE,
		verbose_name='Company',
		limit_choices_to={'active_status':'1'},
		null=True, 
		blank=True)
	product_code = models.CharField(
		max_length=20, 
		verbose_name='Product Code',
		null=True, 
		blank=True)
	ordering_code = models.CharField(
		max_length=20, 
		verbose_name='Ordering Code',
		null=True, 
		blank=True)
	product_desc = models.CharField(
		max_length=1000, 
		verbose_name='Product Description',
		null=True, blank=True)
	short_desc = models.CharField(
		max_length=1000, 
		verbose_name='Short Description',
		null=True, 
		blank=True)
	allergen_Information = ArrayField(
		models.TextField(),
		null=True, 
		blank=True,\
		verbose_name="Allergen Information")
	spice = models.CharField(
		max_length=100, 
		verbose_name='Spice',
		null=True, 
		blank=True)
	kot_desc = models.CharField(
		max_length=1000, 
		verbose_name='Kot Description',
		null=True, 
		blank=True)
	pvideo =  models.FileField(
		upload_to='video/', 
		verbose_name='Image', 
		null=True,blank=True)
	product_image =  models.ImageField(
		upload_to='product_image/', 
		verbose_name='Image', 
		null=True,blank=True)
	tags = ArrayField(
		models.TextField(),
		blank=True,
		null=True, 
		verbose_name="Mapped Tag Ids")
	has_variant = models.BooleanField(
		default=1, 
		verbose_name='Has Variant')
	price = models.FloatField(
		blank=True,
		null=True,
		verbose_name='Product Price')
	discount_price = models.FloatField(
		blank=True,
		null=True,
		verbose_name='Discount Product Price')
	variant_deatils = JSONField(
		blank=True,
		null=True)
	addpn_grp_association = ArrayField(
		models.TextField(), 
		blank=True,
		null=True)
	tax_association = ArrayField(
		models.TextField(), 
		blank=True,
		null=True, 
		verbose_name="Tax Ids")
	outlet_map = ArrayField(
		models.TextField(),
		blank=True,
		null=True, 
		verbose_name="Outlet Mapped Ids")
	active_status = models.BooleanField(
		default=1, 
		verbose_name='Is Active')
	is_recommended = models.BooleanField(
		default=True, 
		verbose_name='Is Recommended')
	included_platform = ArrayField(
		models.TextField(),
		null=True, 
		blank=True,\
		verbose_name="Included Plateform")
	product_schema = JSONField(
		blank=True,
		null=True)
	delivery_option = JSONField(
		blank=True,
		null=True)
	packing_charge = models.FloatField(
		blank=True,
		null=True,
		verbose_name='Packing Charge')
	is_tax = models.BooleanField(
		default=1,
		verbose_name='Is Tax')
	package_tax = ArrayField(
		models.TextField(), 
		blank=True,
		null=True, 
		verbose_name="Package Tax Ids")
	primaryIngredient_deatils = JSONField(
		blank=True,
		null=True)
	secondary_ingredients = JSONField(
		blank=True,
		null=True)
	
	price_type = models.CharField(
		max_length=100, 
		verbose_name='Price Type',
		null=True, 
		blank=True)

	rating = models.CharField(
		max_length=100, 
		verbose_name='Rating',
		null=True, 
		blank=True)

	video_url = models.CharField(
		max_length=2000, 
		verbose_name='Video Url',
		null=True, 
		blank=True)

	packing_amount = models.FloatField(
		blank=True,
		null=True,
		verbose_name='Package Price')

	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(
		null=True, 
		blank=True, 
		verbose_name='Updation Date & Time')
	is_hide = models.BooleanField(
		default=0, 
		verbose_name='Is Hide')
	def image(self):
		if self.product_image:
			return mark_safe('<img src='+MEDIA_URL+'%s width="50" height="50" />' % (self.product_image))
		return 'No Image'
	image.short_description = 'Product Image'

	class Meta:
		verbose_name = 'Product'
		verbose_name_plural = '       Products'

	def __str__(self):
		return self.product_name+' | '+self.food_type.food_type


class ProductImage(models.Model):
	product = models.ForeignKey(
		Product, 
		related_name='ProductImage_product',
		on_delete=models.CASCADE,
		verbose_name='product',
		limit_choices_to={'active_status':'1'})

	product_image =  models.ImageField(
		upload_to='product_image/', 
		verbose_name='Image', 
		null=True,
		blank=True)
	video_url = models.CharField(
		max_length=2000, 
		verbose_name='Price Type',
		null=True, 
		blank=True)
	primary_image = models.BooleanField(
		default=0, 
		verbose_name='Primary Image')
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

	def _str_(self):
		return str(self.product)

	class Meta:
		verbose_name = 'Product Image'
		verbose_name_plural = '          Product Image'



class FeatureProduct(models.Model):
	company = models.ForeignKey(
		Company, 
		related_name='FeatureProduct_Company',
		on_delete=models.CASCADE,
		verbose_name='Company',
		limit_choices_to={'active_status':'1'})
	feature_product = ArrayField(
		models.TextField(), 
		blank=True, 
		null=True,
		verbose_name="Feature_product ID")
	active_status = models.BooleanField(
		default=1, 
		verbose_name='Is Active')
	outlet = models.ForeignKey(
		OutletProfile,
		on_delete=models.CASCADE,
		verbose_name='Outlet',
		limit_choices_to={'active_status':'1'},
		blank=True, null=True)
	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(
		null=True, 
		blank=True, 
		verbose_name='Updation Date & Time')

	def _str_(self):
		return str(self.Company)

	class Meta:
		verbose_name = 'Feature'
		verbose_name_plural = ' Feature Product'


class Product_availability(models.Model):
	outlet = models.ForeignKey(
		OutletProfile,
		on_delete=models.CASCADE,
		verbose_name='Outlet',
		limit_choices_to={'active_status':'1'},
		blank=True, null=True)
	available_product = ArrayField(
		models.TextField(),
		null=True, 
		blank=True, 
		verbose_name="Available_product ID")
	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(
		null=True, 
		blank=True, 
		verbose_name='Updation Date & Time')


class Category_availability(models.Model):
	outlet = models.ForeignKey(
		OutletProfile,
		on_delete=models.CASCADE,
		verbose_name='Outlet',
		limit_choices_to={'active_status':'1'},
		blank=True, null=True)
	available_cat = ArrayField(
		models.TextField(),
		null=True, 
		blank=True, 
		verbose_name="Available_category ID")
	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(
		null=True, 
		blank=True, 
		verbose_name='Updation Date & Time')



class Tag(models.Model):
	company = models.ForeignKey(
		Company, 
		related_name='Tag_Company',
		on_delete=models.CASCADE,
		verbose_name='Company',
		limit_choices_to={'active_status':'1'})
	tag_name = models.CharField(
		max_length=100,
		blank=True, 
		null=True, 
		verbose_name='Tag Name')
	tag_image =  models.ImageField(
		upload_to='tag_image/', 
		verbose_name='Image', 
		null=True,blank=True)
	food_type = models.ForeignKey(FoodType, 
		related_name='Tag_food',
		on_delete=models.CASCADE,
		verbose_name='Food Type',
		limit_choices_to={'active_status':'1'},
		blank=True, 
		null=True)
	active_status = models.BooleanField(
		default=0, 
		verbose_name='Is Active')
	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(
		blank=True, 
		null=True,
		verbose_name='Updation Date & Time')
	
	class Meta:
		verbose_name = ' Tag'
		verbose_name_plural = ' Tag'

	def __str__(self):
		return self.tag_name

class Menu(models.Model):
	menu_name = models.CharField(
		max_length=100, 
		verbose_name='Menu Name')
	menu_image =  models.FileField(
		upload_to='menu_image/', 
		verbose_name='Image')				
	company = models.ForeignKey(
		Company, 
		related_name='Menu_Company',
		on_delete=models.CASCADE,
		verbose_name='Company',
		limit_choices_to={'active_status':'1'},
		null=True, 
		blank=True)
	barcode_pic = models.CharField(
		max_length=100, 
		blank=True, 
		null=True,
		verbose_name='Barcode Pic')
	barcode_info = models.CharField(
		max_length=100, 
		blank=True, 
		null=True,
		verbose_name='Barcode Info')
	base_code = models.CharField(
		max_length=5000, 
		blank=True, 
		null=True,
		verbose_name="base code")
	is_hide = models.BooleanField(
		default=0, 
		verbose_name='Is Active')

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
			verbose_name = 'Menu'
			verbose_name_plural = '  Menu'

	def __str__(self):
			return self.menu_name



