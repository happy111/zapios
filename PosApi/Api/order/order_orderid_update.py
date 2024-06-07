import json
import math
import requests 
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from _thread import start_new_thread
from datetime import datetime
from django.db.models import Q
from Orders.models import Order, OrderStatusType, OrderTracking

from Brands.models import Company
from discount.models import Coupon
from frontApi.serializer.customer_serializers import CustomerSignUpSerializer
from rest_framework_tracking.mixins import LoggingMixin

#Serializer for api
from rest_framework import serializers
from google_speech import Speech
from Product.models import Product
from rest_framework.permissions import IsAuthenticated
from UserRole.models import ManagerProfile,UserType
from ZapioApi.api_packages import *
from History.models import CouponUsed
from Outlet.models import OutletProfile
from Location.models import *

class OrderSerializer(serializers.ModelSerializer):
	class Meta:
		model = Order
		fields = '__all__'

class CouponUsedSerializer(serializers.ModelSerializer):
	class Meta:
		model = CouponUsed
		fields = '__all__' 

class OrderIDUpdate(LoggingMixin,APIView):
	def post(self, request, format=None):
		try:
			data = Order.objects.filter(Company_id=1)
			user = Company.objects.filter(id=1)[0].username
			k =1
			orderdata = {}
			for i in data:
				orderdata['user'] = user
				a = Order.objects.filter(id=i.id)
				order_serializer = OrderSerializer(a[0],data=orderdata,partial=True)
				if order_serializer.is_valid():
					order_serializer.save()
				else:
					pass
				if i.outlet_id != None:
					outlet_id = i.outlet_id
					last_oid_q = Order.objects.filter(outlet_id=outlet_id).last()
					city = OutletProfile.objects.filter(id=outlet_id)[0].city_id
					state = CityMaster.objects.filter(id=city)[0].state_id
					sn = StateMaster.objects.filter(id=state)[0].short_name
					out_id = outlet_id
					finalorderid = str(sn)+'-'+str(out_id)+'-'+str(2021)+'-'+str(k)
					k = int(k) + 1
					orderdata['outlet_order_id'] = finalorderid
					orderdata['user'] = user
					a = Order.objects.filter(id=i.id)
					order_serializer = OrderSerializer(a[0],data=orderdata,partial=True)
					if order_serializer.is_valid():
						order_serializer.save()
					else:
						pass
			return Response({
								"success":True,
								"message":"Order Received successfully"
								})
		except Exception as e:
			print(e)
			return Response({"success": False,
							"message":"Order place api stucked into exception!!"})