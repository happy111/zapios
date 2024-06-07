import json
import requests
import os
import time
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from ZapioApi.Api.BrandApi.profile.profile import CompanySerializer

#Serializer for api
from rest_framework import serializers
from Orders.models import Order, OrderStatusType
from rest_framework.authtoken.models import Token
from Outlet.models import DeliveryBoy,OutletProfile
from django.db.models import Q
from datetime import datetime
from google_speech import Speech
from _thread import start_new_thread

from zapio.settings import Media_Path, MEDIA_ROOT
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user
from Customers.models import *
from Configuration.models import OrderSource,PaymentMethod

class OrderSerializer(serializers.ModelSerializer):
	class Meta:
		model = Order
		fields = '__all__'

class orderNotificationCount(APIView):

	"""
	Order Notification Count Post API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for count for new Orders within Brand

	"""
	permission_classes = (IsAuthenticated,)
	def get(self, request):
		try:
			user = request.user.id
			cid = get_user(user)
			data = \
			Order.objects.filter(Q(Company=cid),Q(is_seen=0)).order_by('-order_time')
			ord_data =[]
			if data.count() > 0:
				for i in data[:5]:
					p_list ={}
					add = i.address
					p_list['id'] = i.id
					p_list['order_id'] = i.order_id
					cus = i.customer
					if cus !='':
						if "email" in cus:
							p_list['email'] = cus['email']
						else:
							pass
						if "mobile_number" in cus:
							p_list['mobile'] = cus['mobile_number']

						if "mobile" in cus:
							p_list['mobile'] = cus['mobile']
						p_list['name'] = cus['name']
					else:
						pass
					ord_data.append(p_list)
			else:
				ord_data = []
			if data:
				countorders = data.count()
			else:
				countorders = 0
			result = []
			sound_path = Media_Path+"notification_sound.mp3"
			return Response({"status":True,
							"orderdetails" : ord_data,
							"ordercount": countorders,
							"sound" : sound_path
							 })
		except Exception as e:
			return Response({"status":False,
				             "message":"Some Error is occured",
				             })


class orderNotificationAll(APIView):

	"""
	All Order Notification  Post API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for All Order within outlet

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request):
		try:
			user = request.user.id
			cid = get_user(user)
			data = {}
			order_data = Order.objects.filter(Q(Company=cid))
			order_update = order_data.update(is_seen=1)
			orderdata = Order.objects.filter(Q(Company=cid),Q(is_seen=1)).order_by('-order_time')
			ord_data =[]
			for i in orderdata:
				p_list ={}
				add = i.address
				p_list['order_id'] = i.order_id
				if i.order_time != None:
					p_list['order_time'] =  i.order_time.strftime("%d/%b/%y at %I:%M %p")
				else:
					p_list['order_time'] = ''
				if i.users_id != None:
					p_list['customer_name'] = CustomerProfile.objects.filter(id=i.users_id)[0].name
				else:
					p_list['customer_name'] = ''
				if i.order_source_id != None:
					p_list['order_source'] = OrderSource.objects.filter(id=i.order_source_id)[0].source_name
				else:
					p_list['order_source'] = ''
				p_list['total_bill_value'] = i.total_bill_value
				p_list['qty'] = len(i.order_description)
				if i.payment_mode != None:
					p = PaymentMethod.objects.filter(id=i.payment_mode)
					if p.count() > 0:
						p_list['payment_mode'] = p[0].payment_method
					else:
						p_list['payment_mode'] = ''
				else:
					if len(i.settlement_details) > 0:
						for index in i.settlement_details:
							s = PaymentMethod.objects.filter(id=index['mode'])
							if s.count() > 0:
								p_list['payment_mode'] = s[0].payment_method
							else:
								p_list['payment_mode'] = ''
					else:
						p_list['payment_mode'] = ''
				if i.order_status_id != None:
					p_list['order_status_name'] = OrderStatusType.objects.filter(id=i.order_status_id).first().Order_staus_name
					p_list['color_code'] = OrderStatusType.objects.filter(id=i.order_status_id).first().color_code
				else:
					p_list['order_status_name'] = ''
					p_list['color_code'] = ''
				if i.total_items != None:
					p_list['total_items'] = i.total_items
				else:
					p_list['total_items'] = 0
				if i.outlet_id != None:
					p_list['outlet'] = OutletProfile.objects.filter(id=i.outlet_id).first().Outletname
				else:
					p_list['outlet'] = ''
				p_list['id'] = i.id
				p_list['order_description'] = i.order_description
				ord_data.append(p_list)
			return Response({"status":True,
							"orderdata":ord_data,
							})
		except Exception as e:
			print(e)



class orderNotificationSeen(APIView):

	"""
	Seen Notification All POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to Seen All order Notification..

		Data Post: {
			"id"                   : "1"
		}

		Response: {

			"success": True, 
			"message": "Seen Updated Successfully",

		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request):
		try:
			data = request.data
			order_record = Order.objects.filter(id=data['id'])
			if order_record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Order data is not valid to Seen!!"
				}
				)
			else:
				data["updated_at"] = datetime.now()
				data["is_seen"] = 1
				order_serializer = \
				OrderSerializer(order_record[0],data=data,partial=True)
				if order_serializer.is_valid():
					data_info = order_serializer.save()
					return Response(
					{
						"success": True,
	 					"message": "Seen Successfully"
					}
					)
				else:
					return Response(
					{
						"success": False,
	 					"message": order_serializer.errors
					}
					)
		except Exception as e:
			print(e)


