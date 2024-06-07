from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import re
from ZapioApi.api_packages import *
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from _thread import start_new_thread
from datetime import datetime
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from Orders.models import Order, OrderStatusType, OrderTracking
import json
from Outlet.models import OutletProfile,DeliveryBoy
from Brands.models import Company
from rest_framework import serializers
from Outlet.Api.serializers.order_serializers import BoySerializer,OrderTrackSerializer, OrderSerializer

from django.db import transaction
from django.http import Http404
from django.utils.translation import gettext_lazy

class ChangeStatusData(APIView):
	"""
	Order Change status POST API
		Authentication Required		: No
		Service Usage & Description	: This Api is used to save all order status change API.
		Data Post: {
				"order_id" 		   : "1",
				"order_status"     : "2",
				"deliveryboy_id"   : "2",
				"is_deliveryboy"      : "true"
		}
		Response: {
			"success": true,
			"message": "Order Placed successfully"
		}

	"""
	def post(self, request, format=None):
		try:
			data = request.data
			err_message = {}
			order_track = {}
			dboy = {}
			order_dict = {}
			err_message["order_id"] = \
					validation_master_anything(data["order_id"],
					"Order Id",contact_re, 1)

			err_message["order_status"] = \
					validation_master_anything(data["order_status"],
					"Order Status",contact_re, 1)

			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			order_data = Order.objects.filter(id=data['order_id']).first()
			order_dict["order_status"] = data['order_status']
			if data['is_deliveryboy'] == "1":
				err_message["deliver_boy"] = \
					validation_master_anything(data["deliveryboy_id"],
					"Delivery Boy",contact_re, 1)
				if any(err_message.values())==True:
					return Response({
						"success": False,
						"error" : err_message,
						"message" : "Please correct listed errors!!"
						})
				order_dict["delivery_boy"] = data['deliveryboy_id']
				Order_serializer = OrderSerializer(order_data,data=order_dict,partial=True)
				dboy_obj = DeliveryBoy.objects.filter(id=data['deliveryboy_id']).first()
				if Order_serializer.is_valid():
					s=Order_serializer.save()
					order_track["order"] = data['order_id']
					order_track["Order_staus_name"] = data['order_status']
					order_track["delivery_boy"] =     data['deliveryboy_id']
					Order_track_serializer = OrderTrackSerializer(data=order_track)
					if Order_track_serializer.is_valid():
						Order_track_serializer.save()
						dboy['is_assign'] = 1
						boy_serializer = BoySerializer(dboy_obj,data=dboy,partial=True)
						if boy_serializer.is_valid():
							boy_serializer.save()
							return Response({
								"success": True, 
								"message" : "Successfully Order is Out for Delivery",
								})
						else:
							return Response({
								"success": False, 
								"message" : boy_serializer.errors,
								})
					else:
						return Response({
							"success": True, 
							"data": Order_track_serializer.errors,
							})
			else:
				check_dboy = Order.objects.filter(id=data['order_id']).first().delivery_boy
				if check_dboy == None:
					Order_serializer = OrderSerializer(order_data,data=order_dict,partial=True)
					if Order_serializer.is_valid():
						s=Order_serializer.save()
						order_track["order"] = data['order_id']
						order_track["Order_staus_name"] = data['order_status']
						order_track["delivery_boy"] =     data['deliveryboy_id']
						Order_track_serializer = OrderTrackSerializer(data=order_track)
						if Order_track_serializer.is_valid():
							Order_track_serializer.save()
							return Response({
								"success": True, 
								"message" : "Successfully Order Processing" ,
								})
						else:
							return Response({
								"success": True, 
								"message" : Order_track_serializer.errors,
								})
					else:
						return Response({
								"success": False, 
								"message" : Order_serializer.errors,
								})
					
				else:
					Order_serializer = OrderSerializer(order_data,data=order_dict,partial=True)
					if Order_serializer.is_valid():
						s=Order_serializer.save()
						order_track["order"] = data['order_id']
						order_track["Order_staus_name"] = data['order_status']
						Order_track_serializer = OrderTrackSerializer(data=order_track)
						if Order_track_serializer.is_valid():
							Order_track_serializer.save()
							order_data_boy = Order.objects.filter(id=data['order_id']).first().delivery_boy_id
							dboy_obj = DeliveryBoy.objects.filter(id=order_data_boy).first()
							dboy['is_assign'] = 0
							boy_serializer = BoySerializer(dboy_obj,data=dboy,partial=True)
							if boy_serializer.is_valid():
								boy_serializer.save()
								return Response({
									"success": True, 
									"message" : "Successfully Order is delivered",
									})
							else:
								return Response({
									"success": True, 
									"message" : boy_serializer.errors,
									})
						else:
							return Response({
									"success": False, 
									"message" : Order_track_serializer.errors,
									})
					return Response({
								"success": False, 
								"message" : Order_serializer.errors,
								})
		except Exception as e:
			print(e)
