from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime, timedelta
from Orders.models import Order,OrderStatusType
from Product.models import Product
from rest_framework import serializers
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import RetrievalCMSData


class BrandOrderRetrieval(APIView):
	"""
	Order retrieval at Brand Level POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of order data within outlet.

		Data Post: {
			"id"                   : "3"
		}

		Response: {

			"success": True, 
			"message": "Order data retrieval api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			ret_check = RetrievalCMSData(data)
			if ret_check !=None:
				return Response(ret_check) 
			else:
				pass
		except Exception as e:
			print("Order data retrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})
