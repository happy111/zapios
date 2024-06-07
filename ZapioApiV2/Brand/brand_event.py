import re
import json
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
from backgroundjobs.models import backgroundjobs,Eventjobs
from UserRole.models import ManagerProfile
from Customers.models import CustomerProfile
from Event.models import HistoryEvent
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user


class dashboardEvent(APIView):
	"""
	Brand Dashboard retrieval GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of Brand Dashboard data within brand.

		Data Post: {
		}

		Response: {

			"success": True, 
			"message": "Brand Dashboard analysis api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			from Brands.models import Company
			user = request.user.id
			nuser = get_user(user)
			order_record = Order.objects.filter(Company=nuser)
			if order_record.count() == 0:
				final_result = []
				return Response(
				{
						"success": True, 
						"message": "Brand Dashboard analysis api worked well!!",
						"data" : final_result
				}
				)
			else:
				all_report = Eventjobs.objects.filter(Company=nuser)
				if all_report.count() == 0:
					final_result = []
				else:
					final_result =  all_report[0].report
				historydata = HistoryEvent.objects.filter(company_id=nuser)
				final_res = []
				if historydata.count() > 0:
					final_res = []
					for index in historydata:
						cart_dict = {}
						cart_dict['key_name'] = index.key_name
						cart_dict['is_key'] = index.is_key
						final_res.append(cart_dict)
				else:
					pass
				return Response({
							"success": True, 
							"message": "Brand Dashboard analysis api worked well!!",
							"data" : final_result,
							"hidedata" : final_res
							})
		except Exception as e:
			print("Dashboard Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})