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
from Product.models import ProductCategory
from Brands.models import Company
from Orders.models import Order,OrderTracking


class OrderSerializer(serializers.ModelSerializer):
	class Meta:
		model = Order
		fields = '__all__'

class EditOrder(APIView):
	"""
	Edit Order POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to edit order post api.

		Data Post: {
			"order_status" : "",
			"payment_mode" : [],
			"order_source" : "",
			"order_id"     : 947
			"transaction"   : "4243243243223"
		}

		Response: {

			"success": True, 
			"message": "Outlet is closed now!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			from django.db.models import Q
			data = request.data
			payment_mode = data['payment_mode']
			record = Order.objects.filter(id=data['order_id'])
			if record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Provided Order data is not valid to retrieve!!"
				}
				)
			else:
				s_details = record[0].settlement_details
				if s_details !=None:
					if len(s_details) > 0:
						final_result = []
						i = 0
						for k in s_details:
							alls = {}
							alls['mode'] = int(payment_mode[i])
							alls['amount'] = k['amount']
							i = i + 1
							final_result.append(alls)
					else:
						final_result = []
						for p in payment_mode:
							alls = {}
							alls['mode'] = int(p)
							alls['amount'] = 0
							final_result.append(alls)
				else:
					final_result = []
					for p in payment_mode:
						alls = {}
						alls['mode'] = int(p)
						alls['amount'] = 0
						final_result.append(alls)


				update_data = \
					record.update(settlement_details=final_result,transaction_id=data['transaction'],\
					order_status=data['order_status'],order_source=data['order_source'])
				if update_data:
					chk_type = OrderTracking.objects.filter(Order_staus_name_id = data['order_status'],order_id=data['order_id'])
					if chk_type.count() > 0:
						pass
					else:
						order_tracking = OrderTracking.objects.create(order_id=data['order_id'], 
						Order_staus_name_id=data['order_status'], created_at=datetime.now())
					record = Order.objects.filter(id=data['order_id'])
					if record[0].order_status_id == 7:
						chk_type = OrderTracking.objects.filter(Order_staus_name = 6,order_id=data['order_id'])
						if chk_type.count() > 0:
							chk_type.delete()
						else:
							pass
					else:
						pass
					if record[0].order_status_id == 6:
						chk_type = OrderTracking.objects.filter(Order_staus_name = 7,order_id=data['order_id'])
						if chk_type.count() > 0:
							chk_type.delete()
						else:
							pass
					else:
						pass
					return Response({
						"success": True, 
						"message": "Order Updated Successfully!!",
						})
		except Exception as e:
			print("Brand Is Open Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})


			# https://github.com/Khan/react-multi-select/blob/master/react-multi-select.gif
