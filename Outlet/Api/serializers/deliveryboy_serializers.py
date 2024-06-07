from rest_framework import serializers

from Outlet.models import OutletProfile, DeliveryBoy


class DeliverySerializer(serializers.ModelSerializer):
	class Meta:
		model = DeliveryBoy
		fields = '__all__' 
