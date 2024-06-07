from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
from rest_framework import serializers
from Orders.models import Order
from django.db.models import Q



class RiderDetail(APIView):
	"""
	rider POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to assign rider for order id.

		Data Post: {
			
			"rider_id"   : "1"
		}

		Response: {

			"success" : True,
			"message" : "Rider listing worked well!!",
			"data"    : final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			# order_record = Order.objects.filter(Q(order_time__date=datetime.now().date()),\
			# 	Q(delivery_boy_id=data['rider_id']),Q(order_status_id != 5),Q(order_status_id != 6),\
			# 	Q(order_status_id != 7))
			order_record = Order.objects.filter(Q(order_time__date=datetime.now().date()),\
				Q(delivery_boy_id=data['rider_id']))
			
			final_result = []
			if order_record.count() > 0:
				for index in order_record:
					dic = {}
					dic['order_id'] = index.outlet_order_id
					dic['location'] = index.address[0]['address']
					final_result.append(dic)
			return Response({
   					 "success":True,
					 "data" : final_result
				})
		except Exception as e:
			print("Outletwise category listing Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})