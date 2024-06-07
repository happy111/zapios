from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.sites.shortcuts import get_current_site
from ZapioApi.Api.BrandApi.profile.profile import CompanySerializer
from Brands.models import Company
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user

#Serializer for api
from rest_framework import serializers
from Product.models import Variant, FoodType, AddonDetails, Product, ProductsubCategory,\
FeatureProduct
from Orders.models import Order
from rest_framework.authtoken.models import Token
from Location.models import CityMaster, AreaMaster

def addr_set():
	domain_name = "http://zapio-admin.com:8080/media/"
	return domain_name

class OrderSerializer(serializers.ModelSerializer):
	order_status_name = serializers.ReadOnlyField(source='order_status.Order_staus_name')
	outlet_name = serializers.ReadOnlyField(source='outlet.Outletname')


	def to_representation(self, instance):
		representation = super(OrderSerializer, self).to_representation(instance)
		representation['order_time'] = instance.order_time.strftime("%d/%b/%y %I:%M %p")
		domain_name = addr_set()
		representation['payment_mode'] = instance.get_payment_mode_display()		
		if instance.delivery_time != None:
			representation['delivery_time'] = instance.delivery_time.strftime("%d/%b/%y %I:%M %p")
		else:
			pass
		return representation

	class Meta:
		model = Order
		fields = ['id','order_time','delivery_time','order_id','payment_mode',\
		'outlet_name','order_status_name','total_bill_value','total_items','is_paid']


class Orderlisting(ListAPIView):
	"""
	Order listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for providing the profile details of brand.
	"""
	permission_classes = (IsAuthenticated,)

	def get_queryset(self):
		user = self.request.user
		auth_id = user.id
		Company_id = get_user(auth_id)
		queryset = Order.objects.filter(Company_id=Company_id).order_by('-order_time')
		return queryset

	def list(self, request):
		queryset = self.get_queryset()
		serializer = OrderSerializer(queryset, many=True)
		response_list = serializer.data 
		return Response({
					"success": True,
					"data" : response_list,
					"message" : "Order listing API worked well!!"})