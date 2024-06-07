from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime, timedelta
from django.db.models import Q

#Serializer for api
from rest_framework import serializers
from Product.models import ProductCategory, AddonDetails, Variant
from Orders.models import Order,OrderStatusType,OrderTracking




class TrackOrder(APIView):
	"""
	Order Track by mobile number or by order id

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to track order by mobile nubmer or by order id.

		Data param: {
			"order_id"		   : "34343",
		}

		Response: {

			"success": True, 
			"orderdata":ord_data
		}

	"""
	# permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			order_id = request.query_params["order_id"]
			err_message ={}
			err_message["order_id"] = only_required(order_id,"Order ID")
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			str_data = order_id.find('%20')
			ord_data =[]
			track_data = Order.objects.filter(outlet_order_id=order_id)
			if track_data.count() > 0:
				pass
			else:
				try:
					track_data = Order.objects.filter(id=order_id)
				except Exception as e:
					print(e)
			if track_data.count()!=0:
				i = track_data[0]
				p_list ={}
				add = i.address
				p_list['id'] = i.id
				p_list['order_id'] = i.outlet_order_id
				if 'address' in add:
					p_list['address'] = add['address']
				else:
					pass
				if 'locality' in add:
					p_list['locality'] = add['locality']
				else:
					pass
				if 'address_type' in add:
					p_list['address_type'] = add['address_type']
				else:
					pass
				if 'city' in add:
					p_list['city'] = add['city']
				else:
					pass
				p_list['order_status'] = i.order_status_id
				t = i.order_time+timedelta(hours=5,minutes=30)
				p_list['order_time'] = t.strftime("%d/%b/%y %I:%M %p")
				if  i.payment_mode == '0':
					p_list['payment_mode'] = "Cash on Delivery"
				else:
					p_list['payment_mode'] = "Online"
				p_list['order_status_name'] = i.order_status.Order_staus_name
				cus = i.customer
				if 'name' in cus:
					p_list['name'] = cus['name']
				else:
					pass
				if 'email' in cus:
					p_list['email'] = cus['email']
				else:
					pass

				if 'mobile' in cus:
					p_list['mobile'] = cus['mobile']
				else:
					pass
				p_list['order_description'] = i.order_description
				p_list["log"] = []
				orderlog = OrderTracking.objects.filter(order_id=p_list["id"]).order_by("id")
				if orderlog.count() > 0:
					for j in orderlog:
						r_list = {}
						r_list["id"] = j.id
						r_list["status_name"] = j.Order_staus_name.Order_staus_name
						r_list["status_id"] = j.Order_staus_name_id
						created_at = j.created_at + timedelta(hours=5, minutes=30)
						r_list["created_at"] = created_at.strftime("%d/%b/%y %I:%M %p")
						r_list["key_person"] = j.key_person
						p_list["log"].append(r_list)
				else:
					pass

				ord_data.append(p_list)
			return Response({"status":True,
							"orderdata":ord_data
							})
		except Exception as e:
			print("Track Order Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})


