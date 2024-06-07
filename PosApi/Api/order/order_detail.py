import re
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from Brands.models import Company
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from ZapioApi.api_packages import *
from datetime import datetime

from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from UserRole.models import ManagerProfile,UserType
from rest_framework import serializers
from Customers.models import CustomerProfile
from Orders.models import Order
from ZapioApi.Api.BrandApi.CustomerMgmt.order_listing import order_history





class OrderDetail(APIView):
	"""
	Order retrieval POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of Order history as per customer.

		Data Post: {
			"mobile"                   : "9910014222"
		}

		Response: {

			"success": True, 
			"message": "Order history as per customer api worked well",
			"data": final_result
		}

	"""
	

	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			user = request.user
			co_id = ManagerProfile.objects.filter(auth_user_id=user.id)[0].Company_id
			err_message = {}
			err_message["mobile"] = \
					validation_master_exact(data["mobile"], "Mobile No.",contact_re, 10)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})

			record = CustomerProfile.objects.filter(company__id=co_id,mobile=data['mobile'])[:10]
			if record.count() == 0:
				return Response(
				{
					"success": True,
 					"message": "Welcome You are first time visitor!!"
				}
				)
			else:
				final_result = []
				q_dict = {}
				q_dict["id"] = record[0].id
				q_dict["company_id"] = record[0].company_id
				q_dict["name"] = record[0].name
				q_dict["email"] = record[0].email
				q_dict["mobile"] = record[0].mobile
				q_dict["address"] = record[0].address1
				q_dict["order_history"] = []
				history = order_history(q_dict)
				final_result.append(history)
			return Response({
						"success": True, 
						"message": "Order history as per customer api worked well!!",
						"data": final_result,
						})
		except Exception as e:
			print("Profile update updation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})