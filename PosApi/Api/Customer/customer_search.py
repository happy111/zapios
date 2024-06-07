from rest_framework.views import APIView
from rest_framework.response import Response
from Brands.models import Company
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import re
from ZapioApi.api_packages import *
from datetime import datetime

from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from UserRole.models import ManagerProfile,UserType
import os
from rest_framework import serializers
from Customers.models import CustomerProfile
from Orders.models import Order
from ZapioApi.Api.BrandApi.CustomerMgmt.order_listing import order_history





class CustomerList(APIView):
	"""
	Customer list POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of customer searching for mobile number.

		Data Post: {
			"mobile"                   : "9910014222"
		}

		Response: {

			"success": True, 
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
					validation_master_anything(data["mobile"], "Mobile No.",contact_re, 5)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			final_result = []
			record = CustomerProfile.objects.filter(company__id=co_id,mobile__icontains=data['mobile'])[:10]
			if record.count() > 0:
				for i in record:
					q_dict = {}
					q_dict["id"] = i.id
					q_dict["first_name"] = i.first_name
					q_dict["last_name"] = i.last_name
					q_dict["mobile"] = i.mobile
					final_result.append(q_dict)
			else:
				pass
			return Response({
						"success": True, 
						"message": "Customer list api worked well!!",
						"data": final_result,
						})
		except Exception as e:
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})