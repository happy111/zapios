from rest_framework import serializers
from Orders.models import Order, OrderStatusType, OrderTracking

from Outlet.models import OutletProfile, DeliveryBoy

 
class OrderSerializer(serializers.ModelSerializer):
	class Meta:
		model = Order
		fields = '__all__' 

class OrderTrackSerializer(serializers.ModelSerializer):
	class Meta:
		model = OrderTracking
		fields = '__all__' 

class BoySerializer(serializers.ModelSerializer):
	class Meta:
		model = DeliveryBoy
		fields = '__all__' 



