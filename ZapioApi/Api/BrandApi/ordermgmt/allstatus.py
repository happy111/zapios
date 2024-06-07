from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime
import os
from django.db.models import Max

from rest_framework import serializers
from Brands.models import Company
from Orders.models import Order,OrderStatusType



class OrderStatus(APIView):
	"""
	All Order Status listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of all Order Status.

	"""
	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			record = OrderStatusType.objects.filter()
			if record.count() != 0:
				final_result = []
				for index in record:
					alls = {}
					alls['id'] = index.id
					alls['type'] = index.Order_staus_name
					final_result.append(alls)
			return Response({
						"success": True, 
						"data": final_result,
						})
		except Exception as e:
			print("Order Status Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})