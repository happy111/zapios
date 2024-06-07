from django.db import models
from Brands.models import Company
from django.contrib.postgres.fields import ArrayField,JSONField


class PrimaryEventType(models.Model):
	event_type = models.CharField(
		max_length=100,
		verbose_name='Event Type')
	company = models.ForeignKey(
		Company, 
		related_name='PrimaryEvent_Company',
		on_delete=models.CASCADE,
		verbose_name='Company',
		limit_choices_to={'active_status':'1'})
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
		verbose_name='    Event Type'
		verbose_name_plural='    Event Type'

	def __str__(self):
		return self.event_type


class HistoryEvent(models.Model):
	key_name = models.CharField(
		max_length=100,
		verbose_name='Event Name')
	event_time = models.TimeField(
		auto_now=False, 
		auto_now_add=False, 
		null=True,blank=True,
		verbose_name="Event Time")
	company = models.ForeignKey(
		Company, 
		related_name='HistoryEvent_Company',
		on_delete=models.CASCADE,
		verbose_name='Company',
		limit_choices_to={'active_status':'1'})
	active_status = models.BooleanField(
		default=0,
		verbose_name='Is Active')
	is_key = models.BooleanField(
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
		verbose_name='    HistoryEvent'
		verbose_name_plural='  HistoryEvent'

	def __str__(self):
		return self.key_name


class Trigger(models.Model):
	trigger_type = models.CharField(
		max_length=100,
		null=True,
		blank=True,
		verbose_name='Trigger Type')
	trigger_importance = models.CharField(
		max_length=100,
		null=True,
		blank=True,
		verbose_name='Trigger Type')
	trigger_name = models.ForeignKey(
		PrimaryEventType, 
		related_name='Trigger_trigger_name',
		null=True,blank=True,
		on_delete=models.CASCADE,
		verbose_name='Trigger name',
		limit_choices_to={'active_status':'1'})
	outlet = ArrayField(
		models.TextField(),
		null=True, blank=True, 
		verbose_name="Outlet Mapped Ids")
	company = models.ForeignKey(
		Company, 
		related_name='Trigger_Company',
		on_delete=models.CASCADE,
		verbose_name='Company',
		limit_choices_to={'active_status':'1'})

	send = ArrayField(
		models.TextField(),
		null=True, 
		blank=True, 
		verbose_name="Send")
	to = ArrayField(
		models.TextField(),
		null=True, 
		blank=True, 
		verbose_name="To")
	content = models.CharField(
		max_length=1000, 
		verbose_name='Trigger Content',
		null=True, blank=True)
	day = models.CharField(
		max_length=100,
		null=True,
		blank=True,
		verbose_name='Trigger day')
	event_time = models.TimeField(
		auto_now=False, 
		auto_now_add=False, 
		null=True,blank=True,
		verbose_name="Event Time")
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
		verbose_name='    Trigger'
		verbose_name_plural='  Trigger'

	def __str__(self):
		return self.trigger_type


class EventTag(models.Model):
	tag_name = models.CharField(
		max_length=100,
		verbose_name='Event Type')
	company = models.ForeignKey(
		Company, 
		related_name='EventTag_Company',
		on_delete=models.CASCADE,
		verbose_name='Company',
		limit_choices_to={'active_status':'1'})
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
		verbose_name='    Event Tag'
		verbose_name_plural='    Event Tag'

	def __str__(self):
		return self.tag_name
