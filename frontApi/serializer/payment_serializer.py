from rest_framework import serializers
from django.db.models import Count
from Configuration.models import PaymentDetails



class PaymentSerializer(serializers.ModelSerializer):

	class Meta:
		model = PaymentDetails
		fields = '__all__'
