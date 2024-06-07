from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Brands.models import Company
import json
#Serializer for api
from rest_framework import serializers
from django.db.models import Q
from datetime import datetime, timedelta
from Customers.models import CustomerProfile
from Orders.models import Order
from django.db.models import Sum,Count,Max
from Outlet.models import OutletProfile
from ZapioApi.Api.paginate import pagination
import math  
from UserRole.models import ManagerProfile
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user
from Product.models import Product






class ProductDelete(APIView):
	"""
	AddonDetails retrieval POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of Order analysis as per customer data.

		Data Post: {
			"id"                   : "33234"
		}

		Response: {

			"success": True, 
			"message": "Order analysis as per customer retrieval api worked well",
			"data": final_result
		}

	"""
	def post(self, request):
		try:
			data = request.data
			for i in range(25759,39456):
				pdata = CustomerProfile.objects.filter(id=i)
				if pdata.count() > 0:
					pdata.delete()
					print("c")
				else:
					print("a")
					pass
			return Response({
							 "status":True
							 })
		except Exception as e:
			print(e)
			return Response(
						{"error":str(e)}
						)


