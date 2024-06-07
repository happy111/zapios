from rest_framework.views import APIView
from rest_framework.response import Response
import json
from datetime import datetime
from datetime import datetime, timedelta
from urbanpiper.models import OutletSync, RiderStatusRawApiResponse, UrbanOrders
from rest_framework_tracking.mixins import LoggingMixin
from rest_framework import serializers
from Orders.models import Order,OrderTracking



class RiderStatusUpdate(LoggingMixin, APIView):
	"""
	Rider Status Update Hook POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used for handling webhook mechanism for rider status update in urbanpiper.

	"""
	def post(self, request, format=None):
		try:
			data = request.data
			order_id = str(data["order_id"])
			order_status = data["delivery_info"]["current_state"]
			rider_detail = {}
			rider_detail["name"] = data["delivery_info"]["delivery_person_details"]["name"]
			rider_detail["email"] = "N/A"
			rider_detail["mobile"] =  data["delivery_info"]["delivery_person_details"]["phone"]
			urban_order = UrbanOrders.objects.filter(order_id=order_id)
			if urban_order.count() == 0:
				return Response({
					"success" : False,
					"message" : "Order is not valid!!"
					})
			else:
				pass
			outlet_id = urban_order[0].outlet_id
			outlet_check = OutletSync.objects.filter(outlet=outlet_id,sync_status="synced")
			if outlet_check.count() == 0:
				return Response({
					"success" : False,
					"message" : "Outlet is not valid!!"
					})
			else:
				pass
			company_id = outlet_check[0].company_id
			sync_outlet_id = outlet_check[0].id
			raw_record_create = \
			RiderStatusRawApiResponse.objects.create(company_id=company_id,sync_outlet_id=sync_outlet_id,\
				api_response=data)
			order_data = Order.objects.filter(urban_order_id=order_id)
			order_data_update = order_data.update(delivery_boy_details=rider_detail,is_rider_assign=1)
			return Response({
						"success": True, 
						"message": "Rider Staus Update webhook mechanism api worked well!!"
						})
		except Exception as e:
			print("Rider Status Update webhook mechanism Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})
