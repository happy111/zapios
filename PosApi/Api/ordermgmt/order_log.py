import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from ZapioApi.Api.BrandApi.profile.profile import CompanySerializer
from Brands.models import Company


from rest_framework import serializers
from Product.models import (Variant, 
							FoodType, 
							AddonDetails, 
							Product, 
							ProductsubCategory,
							FeatureProduct)
from Orders.models import Order,OrderStatusType, OrderTracking
from rest_framework.authtoken.models import Token
from django.db.models import Q
from datetime import datetime, timedelta
from UserRole.models import * 
from ZapioApi.api_packages import *


class OrderLogData(APIView):
	"""
	Order Log POS Level POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for order log for pos lable.

		Data Post: {
			"order_id"                   : "3"
		}

		Response: {

			"success": True, 
			"message": "Order log data  api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			data["id"] = str(data["order_id"])
			err_message = {}
			err_message["order_id"] = \
					validation_master_anything(data["id"],
					"Order Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			order_record = Order.objects.filter(id=data['order_id'])
			if order_record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Required Order data is not valid to retrieve!!"
				}
				)
			else:
				orderdata = OrderTracking.objects.filter(order_id=data['order_id']).order_by('id')
				ord_data =[]
				for i in orderdata:
					p_list ={}
					p_list['id'] = i.id
					p_list['status_name'] = i.Order_staus_name.Order_staus_name
					p_list["created_at"] = i.created_at.isoformat()
					ord_data.append(p_list)
			return Response({"status":True,
							"orderdata":ord_data,
							"customer":order_record[0].customer,
							"address":order_record[0].address,
							"order_desp":order_record[0].order_description})
		except Exception as e:
			print(e)
			return Response(
						{"error":str(e)}
						)


