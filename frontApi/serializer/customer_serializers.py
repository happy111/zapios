from rest_framework import serializers
from django.db.models import Count
from Customers.models import CustomerProfile



class CustomerSignUpSerializer(serializers.ModelSerializer):

	class Meta:
		model = CustomerProfile
		fields = '__all__'
