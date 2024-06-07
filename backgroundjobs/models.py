from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.safestring import mark_safe
from zapio.settings import MEDIA_URL
from Brands.models import Company
from django.contrib.postgres.fields import ArrayField,JSONField
from Outlet.models import OutletProfile


class backgroundjobs(models.Model):
	outlet = models.ForeignKey(OutletProfile,on_delete=models.CASCADE,verbose_name='Outlet',
												limit_choices_to={'active_status':'1'},
												blank=True, null=True)
	Company = models.ForeignKey(Company,on_delete=models.CASCADE,verbose_name='Company',
												limit_choices_to={'active_status':'1'},
												blank=True, null=True)
	report = JSONField(blank=True,null=True,verbose_name="Report")
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(blank=True, null=True, verbose_name='Updation Date & Time')

	class Meta:
		verbose_name ="backgroundjobs"
		verbose_name_plural ="  backgroundjobs"

	def __str__(self):
		return str(self.outlet)



class Eventjobs(models.Model):
	outlet = models.ForeignKey(OutletProfile,on_delete=models.CASCADE,verbose_name='Outlet',
												limit_choices_to={'active_status':'1'},
												blank=True, null=True)
	Company = models.ForeignKey(Company,on_delete=models.CASCADE,verbose_name='Company',
												limit_choices_to={'active_status':'1'},
												blank=True, null=True)
	report = JSONField(blank=True,null=True,verbose_name="Report")
	created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation Date & Time')
	updated_at = models.DateTimeField(blank=True, null=True, verbose_name='Updation Date & Time')

	class Meta:
		verbose_name ="backgroundjobs"
		verbose_name_plural ="  backgroundjobs"

	def __str__(self):
		return str(self.outlet)