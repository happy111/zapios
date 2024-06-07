from rest_framework import serializers
from discount.models import DiscountReason



class ReasonSerializer(serializers.ModelSerializer):

	class Meta:
		model = DiscountReason
		fields = '__all__'
