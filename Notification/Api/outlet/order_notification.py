from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_201_CREATED, \
	HTTP_406_NOT_ACCEPTABLE, HTTP_200_OK, HTTP_503_SERVICE_UNAVAILABLE
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.sites.shortcuts import get_current_site
from ZapioApi.Api.BrandApi.profile.profile import CompanySerializer
import json
#Serializer for api
from rest_framework import serializers

from Orders.models import Order, OrderStatusType
from rest_framework.authtoken.models import Token
from Outlet.models import DeliveryBoy,OutletProfile
from django.db.models import Q
from datetime import datetime

class OrderSerializer(serializers.ModelSerializer):
	class Meta:
		model = Order
		fields = '__all__'

class orderNotificationCount(APIView):
	"""
	Order Notification Count Post API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for count for Order within outlet

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request):
		try:
			user = request.user.id
			orderdata = Order.objects.filter(Q(outlet__auth_user=user) & Q(is_seen=0)).order_by('-order_time')[:3]
			ord_data =[]
			for i in orderdata:
				p_list ={}
				add = i.address
				p_list['id'] = i.id
				p_list['order_id'] = i.order_id
				cus = i.customer
				p_list['name'] = cus['name']
				p_list['mobile_number'] = cus['mobile_number']
				p_list['email'] = cus['email']
				ord_data.append(p_list)
			orderdata = Order.objects.filter(Q(outlet__auth_user=user) & Q(is_seen=0)).order_by('-order_time')
			if orderdata:
				countorders = orderdata.count()
			else:
				countorders = 0
			return Response({"status":True,
							"orderdetails" : ord_data,
							"ordercount": countorders })
		except Exception as e:
			print(e)
			return Response({"status":False,
				             "message":ord_data,
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
			orderdata = Order.objects.filter(Q(outlet__auth_user=user) & Q(is_seen=0)).order_by('-order_time')
			ord_data =[]
			for i in orderdata:
				p_list ={}
				add = i.address
				p_list['id'] = i.id
				p_list['order_id'] = i.order_id
				p_list['longitude'] = add['longitude']
				p_list['latitude'] = add['latitude']
				p_list['address'] = add['address']
				p_list['locality'] = add['locality']
				p_list['city'] = add['city']
				p_list['order_status'] = i.order_status_id
				p_list['discount_value'] = i.discount_value
				p_list['sub_total'] = i.sub_total
				p_list['total_bill_value'] = i.total_bill_value
				p_list['order_time'] = i.order_time.strftime("%d/%b/%y %I:%M %p")
				if  i.payment_mode == '0':
					p_list['payment_mode'] = "Cash on Delivery"
				else:
					p_list['payment_mode'] = "Online"
				p_list['order_status_name'] = OrderStatusType.objects.filter(id=i.order_status_id).first().Order_staus_name
				p_list['color_code'] = OrderStatusType.objects.filter(id=i.order_status_id).first().color_code
				cus = i.customer
				p_list['name'] = cus['name']
				p_list['mobile_number'] = cus['mobile_number']
				p_list['email'] = cus['email']
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
				data["has_been_here"] = 1
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


