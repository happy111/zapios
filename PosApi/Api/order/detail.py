import json
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
from History.models import CouponUsed
from frontApi.serializer.customer_serializers import CustomerSignUpSerializer
from rest_framework_tracking.mixins import LoggingMixin

#Serializer for api
from rest_framework import serializers
import math
from google_speech import Speech
from Product.models import Product
from rest_framework.permissions import IsAuthenticated
from UserRole.models import ManagerProfile,UserType
from ZapioApi.api_packages import *
from History.models import CouponUsed
from Outlet.models import OutletProfile
from Location.models import *
from zapio.settings import  Media_Path
from Customers.models import CustomerProfile
from django.template.loader import render_to_string



class UserDetail(LoggingMixin,APIView):
	"""
	Customer Order POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to save all order related
		data to store it in database for future reference.

		Data Post:  {
			"customer": {
						"name": "umesh",
						"mobile": "8423845784",
						"email" : "umeshsamal3@gmail.com"
						"locality": "adadasd"
						},

			"address1": [
							{
							"locality": "3.142542",
							"address": "3.236542",
							},
							{
							    "locality": "3.142542",
								"address": "Mayur Vihar",
							}
						],

			settlement_details:[
						{"mode":"0","amount":250},
						{"mode":"1","amount":150,"trannsaction_id":"razr_012365478uytre"}
						],

			"order_description": [
									{
							"name": "Margreeta Pizza",
							"id": "12",
							"price": "229",
							"size": "N/A",
							"customization_details": []
						
							},
							{
							"name": "Margreeta Pizza",
							"id": "12",
							"price": "229",
							"size": "N/A",
							"customization_details": []
						
							}
						],
			
			"payment_mode": "1",
			"payment_id" : "Razor1539587456980",
			"Payment_status" : "1",
			"discount_value": 0,
			"total_bill_value": 309,
			"total_items": 2,
			"sub_total": 294,
			"cart_discount": 0,
			"discount_name": "",
			"discount_reason": "",
			"Delivery_Charge": 309,
			"Packing_Charge": 0,
			"Order_Type": "takeaway",
			"Payment_source":"paytm",
			"Order_Source" : "call",
			"delivery_instructions": "asdsadsa",
			"special_instructions": "dasdsadsa",
			"outlet_id" : 3,
			"taxes": 15,
		}

		Response: {

			"success": true,
			"message": "Order Received successfully"
		}

	"""
	def post(self, request, format=None):
		try:
			orderdata = Order.objects.filter()
			print(orderdata.count())
			finaldata = []
			for index in orderdata:
				alls = {}
				alls['customer'] = index.customer
				finaldata.append(alls)
			return Response({"success": False,
							"message":finaldata})
		except Exception as e:
			print(e)
			return Response({"success": False,
							"message":"Order place api stucked into exception!!"})
