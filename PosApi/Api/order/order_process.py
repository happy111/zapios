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
from Orders.models import OrderStatusType




class ProcessList(APIView):
	"""
	Order Process List get API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of order process.

	"""
	

	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			user = request.user
			alldata = OrderStatusType.objects.filter(active_status=1).order_by('priority')
			final_result = []
			for i in alldata:
				dicts = {}
				dicts['id'] = i.id
				dicts['Order_staus_name'] = i.Order_staus_name
				dicts['color_code'] = i.color_code
				dicts['priority'] = i.priority
				dicts['active_status'] = i.active_status
				final_result.append(dicts)
			return Response({
						"success": True, 
						"message": "All Order Process Type api worked well!!",
						"data": final_result,
						})
		except Exception as e:
			print("Order Process Type Api Stucked into exception!!")
			print(e)
			return Response({"success": False, 
							"message": "Error happened!!", 
							"errors": str(e)})