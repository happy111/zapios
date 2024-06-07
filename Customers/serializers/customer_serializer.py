from rest_framework import serializers
from Customers.models import CustomerProfile,customer_otp



class CustomerSignUpSerializer(serializers.ModelSerializer):
	class Meta:
		model = CustomerProfile
		fields = '__all__'

class CustomerOTPSerializer(serializers.ModelSerializer):
	class Meta:
		model = customer_otp
		fields = '__all__'