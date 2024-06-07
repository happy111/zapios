from rest_framework import serializers
from . models import *

class ProductStatus(serializers.ModelSerializer):
	class Meta:
		model = OnlinepaymentStatus
		fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
	class Meta:
		model = PaymentDetails
		fields = '__all__'


class AnalyticsSerializer(serializers.ModelSerializer):
	class Meta:
		model = AnalyticsSetting
		fields = '__all__'

class ColorSerializer(serializers.ModelSerializer):
	class Meta:
		model = DeliverySetting
		fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):

	class Meta:
		model = PaymentDetails
		fields = '__all__'

class ThemeSerializer(serializers.ModelSerializer):

	class Meta:
		model = ColorSetting
		fields = '__all__'
