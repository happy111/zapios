import re
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from ZapioApi.api_packages import *
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from _thread import start_new_thread
from datetime import datetime
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from Orders.models import Order
from Brands.models import Company
from rest_framework import serializers

class OrderSerializer(serializers.ModelSerializer):
	class Meta:
		model = Order
		fields = '__all__'


class OrderSettle(APIView):
	"""
	Order Settle POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to order settle for POS.

		Data Post: {
				"order_id" 		   : "1",
				"transaction_id"   : "rewrerwerewr3453543534534"
 		}

		Response: {
			"success": True, 
			"message" : "Order Settle is successfully!!",
		}

	"""
	def post(self, request, format=None):
		try:
			data = request.data
			datas = {}
			chk_order = Order.objects.filter(id=data['order_id'])
			if chk_order.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Order id is not valid to update!!"
				})
			else:
				order_mode = chk_order[0].payment_mode
				if order_mode == 0:
					pass
				else:
					err_message = {}
					err_message["id"] = only_required(data["transaction_id"],"Transaction Id")
					if any(err_message.values())==True:
						return Response({
									"success": False,
									"error" : err_message,
									"message" : "Please correct listed errors!!"
								})
					datas['transaction_id'] = data['transaction_id']
					datas['order_status'] = str(5)
					order_serializer = \
					OrderSerializer(chk_order[0],data=datas,partial=True)
					if order_serializer.is_valid():
						data_info = order_serializer.save()
					else:
						print("something went wrong!!")
						return Response({
							"success": False, 
							"message": str(order_serializer.errors),
							})
				return Response({
							"success": True, 
							"message": "Order Settle is successfully",
							})
		except Exception as e:
			print(e)
			return Response({
						"success": False,
						"error" : str(e),
						"message" : "Please correct listed errors!!"
						})