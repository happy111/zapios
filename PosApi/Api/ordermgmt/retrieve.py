import re,json
from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
from datetime import datetime, timedelta
from Orders.models import Order,OrderStatusType
from Product.models import Product
from rest_framework import serializers
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import RetrievalData
from UserRole.models import * 


class BrandOrderRetrieval(APIView):
	"""
	Order retrieval at POS Level POST API

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
			user = request.user
			co_id = ManagerProfile.objects.filter(auth_user_id=user.id)[0].Company_id
			data['cid'] = co_id
			ret_check = RetrievalData(data)
			if ret_check !=None:
				return Response(ret_check) 
			else:
				pass
		except Exception as e:
			print("Order data retrieval adasdas Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})

