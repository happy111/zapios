from rest_framework import serializers
from django.db.models import Count
from Configuration.models import DeliverySetting



class DeliverySerializer(serializers.ModelSerializer):

	class Meta:
		model = DeliverySetting
		fields = '__all__'
