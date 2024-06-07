import re
import json
import calendar
import calendar
from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
from datetime import datetime
from django.db.models import Q
from django.db.models.functions import ExtractYear, ExtractMonth,ExtractWeek, ExtractWeekDay
from django.db.models.functions import Extract


#Serializer for api
from rest_framework import serializers
from Product.models import ProductCategory, AddonDetails, Variant
from Orders.models import Order
from django.db.models import Count, Sum, Max, Avg, Case, When, Value, IntegerField, BooleanField
from django.db.models.functions import ExtractYear, ExtractMonth,ExtractWeek, ExtractWeekDay
from django.db.models.functions import Extract
from datetime import datetime, timedelta
from backgroundjobs.models import backgroundjobs


class dashboardOutlet(APIView):
	"""
	Outlet Dashboard retrieval GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of Outlet Dashboard data within brand.

		Data Post: {
		}

		Response: {

			"success": True, 
			"message": "Outlet Dashboard data anaysis api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			from Brands.models import Company
			user = request.user.id
			order_record = Order.objects.filter(outlet__auth_user=user)
			if order_record.count() == 0:
				return Response(
				{
					"success": True,
 					"message": "Required Dashboard data is not valid to retrieve!!"
				}
				)
			else:
				all_report = backgroundjobs.objects.filter(outlet__auth_user=user)
				if all_report.count() == 0:
					final_result = []
				else:
					final_result =  all_report[0].report
				return Response({
							"success": True, 
							"message": "Outlet Dashboard data anaysis api worked well!!",
							"data" : final_result
							})
		except Exception as e:
			print("Dashboard Api for Outlet Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})