from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from zapio.settings import MEDIA_URL
from Brands.models import Company
from Product.models import FoodType,Product,Variant
from django.contrib.postgres.fields import ArrayField,JSONField
from django.core.validators import MinValueValidator, MaxValueValidator
from Orders.models import Order
from Configuration.models import Unit


class RecipeIngredient(models.Model):
	status_choice = (
		("primary", "Primary Ingredient"),
		("secondary", "Secondary Ingredient"),
	)
	ingredient_type = models.CharField(
		choices=status_choice,
		max_length=50,
		null=True,
		blank=True,
		verbose_name="Ingredient Type",
	)
	name = models.CharField(max_length=100, verbose_name='Ingredient name')
	company = models.ForeignKey(
		Company, 
		related_name='RecipeIngredient_Company',
		on_delete=models.CASCADE,
		verbose_name='Company',
		limit_choices_to={'active_status':'1'})
	food_type = models.ForeignKey(
		FoodType, 
		blank=True, 
		null=True,
		related_name='ReceipeIngredient_food',
		on_delete=models.CASCADE,
		verbose_name='Food Type',
		limit_choices_to={'active_status':'1'})
	image = models.ImageField(
		upload_to='Ingredient',
		null=True, 
		blank=True, 
		verbose_name='Ingredient Image')
	primary_deatils = JSONField(blank=True,null=True)
	output_yield =  JSONField(blank=True,null=True)
	active_status = models.BooleanField(
		default=1, 
		verbose_name='Is Active')
	created_at = models.DateTimeField(
		auto_now_add=True,
		verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(
		blank=True, 
		null=True,
		verbose_name='Updation Date & Time')

	class Meta:
		verbose_name = 'Receipe'
		verbose_name_plural = ' Receipe'

	def __str__(self):
		return self.name


class Ingredient(models.Model):
	company = models.ForeignKey(Company, related_name='Ingredient_Company',
												on_delete=models.CASCADE,verbose_name='Company',
												limit_choices_to={'active_status':'1'})
	name = models.CharField(max_length=100, verbose_name='Ingredient name', unique=True)
	food_type = models.ForeignKey(FoodType, related_name='Ingredient_food',
												on_delete=models.CASCADE,verbose_name='Food Type',
												limit_choices_to={'active_status':'1'})
	image = models.ImageField(upload_to='Ingredient',
								null=True, blank=True, verbose_name='Ingredient Image')
	active_status = models.BooleanField(default=0, verbose_name='Is Active')
	# unit = model.BooleanField()
	created_at = models.DateTimeField(auto_now_add=True,
														verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(blank=True, null=True,
														verbose_name='Updation Date & Time')
	class Meta:
		verbose_name = 'Ingredient'
		verbose_name_plural = ' Ingredient'

	def __str__(self):
		return self.name


class StepToprocess(models.Model):
	company = models.ForeignKey(Company, related_name='StepToprocess_Company',
												on_delete=models.CASCADE,verbose_name='Company',
												limit_choices_to={'active_status':'1'})
	product = models.ForeignKey(Product, related_name='StepToprocess_product',
												on_delete=models.CASCADE,verbose_name='Product',
												limit_choices_to={'active_status':'1'})
	varient = models.ForeignKey(Variant, related_name='StepToprocess_varient',
									on_delete=models.CASCADE,verbose_name='Variant',
									limit_choices_to={'active_status':'1'},null=True, blank=True,)
	step = models.PositiveIntegerField(validators=[MaxValueValidator(10),MinValueValidator(1)
			  ],verbose_name='Step', null=True, blank=True,)
	process = models.CharField(max_length=100,blank=True, null=True, verbose_name='Name Of Process')
	description = models.CharField(max_length=100,blank=True, null=True, verbose_name='Description')
	time_of_process = \
	models.PositiveIntegerField(validators=[MaxValueValidator(100),MinValueValidator(1)
			  ],blank=True, null=True,verbose_name='Time Of Process')
	image = models.ImageField(upload_to='Stepprocess',
								null=True, blank=True, verbose_name='Image Of Process')
	ingredient = JSONField(blank=True,null=True)
	active_status = models.BooleanField(default=0, verbose_name='Is Active')
	created_at = models.DateTimeField(auto_now_add=True,
														verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(blank=True, null=True,
														verbose_name='Updation Date & Time')
	class Meta:
		verbose_name = 'Step To process'
		verbose_name_plural = ' Steps To Process'

	def __str__(self):
		return self.process



class ProcessTrack(models.Model):
	company = models.ForeignKey(Company, related_name='ProcessTrack_Company',
												on_delete=models.CASCADE,verbose_name='Company',
												limit_choices_to={'active_status':'1'})
	Step = models.ForeignKey(StepToprocess, related_name='ProcessTrack_step',
												on_delete=models.CASCADE,verbose_name='Step',
												limit_choices_to={'active_status':'1'})
	Order = models.ForeignKey(Order, related_name='ProcessTrack_Order',
												on_delete=models.CASCADE,verbose_name='Order',
											)
	product = models.ForeignKey(Product, related_name='ProcessTrack_product',
										on_delete=models.CASCADE,verbose_name='Product',
										limit_choices_to={'active_status':'1'})
	Variant = models.ForeignKey(Variant, related_name='ProcessTrack_Variant',
										on_delete=models.CASCADE,verbose_name='Variant',
							limit_choices_to={'active_status':'1'},blank=True,null=True)
	process_status = models.CharField(choices=(
							 ("0", "Completed"),	
							 ("1", "In Progress"),
							 ("2", "Not Started"),
						),max_length=100,blank=True,null=True,
						verbose_name='Process Status')
	started_at = \
	models.TimeField(blank=True, null=True,verbose_name='Start Time')
	completed_at = \
	models.TimeField(blank=True, null=True,verbose_name='Completion Time')

	
	class Meta:
		verbose_name = 'Process Track'
		verbose_name_plural = ' Process Track'

	def __str__(self):
		return str(self.Step)