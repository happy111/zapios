from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_201_CREATED, \
	HTTP_406_NOT_ACCEPTABLE, HTTP_200_OK, HTTP_503_SERVICE_UNAVAILABLE
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime
from Orders.models import Order,OrderStatusType

#Serializer for api
from rest_framework import serializers
from Outlet.models import DeliveryBoy


class OrderRetrieval(APIView):
	"""
	Order retrieval POST API

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
			data["id"] = str(data["id"])
			err_message = {}
			err_message["id"] = \
					validation_master_anything(data["id"],
					"Order Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			order_record = Order.objects.filter(id=data['id'])
			if order_record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Required Order data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				p_list = {}
				p_list["id"] = order_record[0].id
				add = order_record[0].address
				p_list['order_id'] = order_record[0].order_id
				p_list['longitude'] = add['longitude']
				p_list['latitude'] = add['latitude']
				p_list['address'] = add['address']
				p_list['locality'] = add['locality']
				p_list['city'] = add['city']
				p_list['order_status'] = order_record[0].order_status_id
				if  order_record[0].payment_mode == '0':
					p_list['payment_mode'] = "Cash on Delivery"
				else:
					p_list['payment_mode'] = "Online"
				p_list['order_status_name'] = OrderStatusType.objects.filter(id=order_record[0].order_status_id).first().Order_staus_name
				p_list['color_code'] = OrderStatusType.objects.filter(id=order_record[0].order_status_id).first().color_code
				cus = order_record[0].customer
				p_list['name'] = cus['name']
				p_list['mobile_number'] = cus['mobile_number']
				p_list['email'] = cus['email']
				p_list['order_description'] = order_record[0].order_description
				p_list['order_time'] = order_record[0].order_time.strftime("%d/%b/%y %I:%M %p")
				if order_record[0].delivery_time != None:
					p_list['delivery_time'] = order_record[0].delivery_time.strftime("%d/%b/%y %I:%M %p")
				else:
					p_list['delivery_time'] = None
				p_list['taxes'] = order_record[0].taxes
				p_list['sub_total'] = order_record[0].sub_total
				p_list['discount_value'] = order_record[0].discount_value
				p_list['total_bill_value'] = order_record[0].total_bill_value
				deb_id = order_record[0].delivery_boy_id
				if deb_id:
					p_list['boyname']  = DeliveryBoy.objects.filter(id=deb_id).first().name
					p_list['boyemail']  = DeliveryBoy.objects.filter(id=deb_id).first().email
					p_list['boymobile']  = DeliveryBoy.objects.filter(id=deb_id).first().mobile
				else:
					pass
				final_result.append(p_list)

			return Response({
						"success": True, 
						"message": "Order data retrieval api worked well!!",
						"data": final_result,
						})
		except Exception as e:
			print("Order data retrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})
