from rest_framework.views import APIView
from rest_framework.response import Response
import json
from django.db.models import Q
from datetime import datetime, timedelta
from urbanpiper.models import OutletSync, OrderStatusRawApiResponse, UrbanOrders
from rest_framework_tracking.mixins import LoggingMixin
from rest_framework import serializers
from Orders.models import Order
from datetime import datetime, timedelta
from Orders.models import Order,OrderStatusType,OrderTracking

li = ["Acknowledged", "Food Ready", "Dispatched", "Completed", "Cancelled"]

class OrderStatusUpdate(LoggingMixin, APIView):
	"""
	Order Status Update Hook POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used for handling webhook mechanism for order status update in urbanpiper.

	"""
	def post(self, request, format=None):
		try:
			data = request.data
			urban_order_id = data["order_id"]
			order_id = str(data["order_id"])
			aggre_order_status = data["new_state"]
			urban_order = UrbanOrders.objects.filter(Q(order_state=aggre_order_status),\
											Q(order_id=order_id))
			if urban_order.count() == 1:
				return Response({
					"success" : False,
					"message" : "Order is processed already for "+aggre_order_status+"status!!"
					}) 
			else:
				pass
			if aggre_order_status != "Acknowledged" and aggre_order_status != "Food Ready" and\
				aggre_order_status != "Placed":
				pass
			else:
				return Response({
					"success" : False,
					"message" : "Order is processed for '"+aggre_order_status+"' staus at POS level already !!"
					})
			urban_order = UrbanOrders.objects.filter(~Q(order_state__icontains="Complet"),\
											Q(order_id=order_id))
			if urban_order.count() == 0:
				return Response({
					"success" : False,
					"message" : "Order is not valid or already completed!!"
					})
			else:
				pass
			outlet_id = urban_order[0].outlet_id
			outlet_check = OutletSync.objects.filter(outlet=outlet_id,sync_status="synced")
			# api_ref = APIReference.objects.filter(ref_id=reference_id)
			if outlet_check.count() == 0:
				return Response({
					"success" : False,
					"message" : "Outlet is not valid!!"
					})
			else:
				pass
			if urban_order[0].order_state == "Completed":
				return Response({
					"success" : False,
					"message" : "Already processed!!"
					})
			else:
				pass
			company_id = outlet_check[0].company_id
			sync_outlet_id = outlet_check[0].id
			raw_record_create = \
			OrderStatusRawApiResponse.objects.create(company_id=company_id,
																	sync_outlet_id=sync_outlet_id,\
																	api_response=data)
			updated_at = datetime.now()
			status_update = urban_order.update(order_state=data["new_state"],updated_at=updated_at)
			main_order = Order.objects.filter(urban_order_id=order_id)
			main_order_id = main_order[0].id
			if aggre_order_status == "Dispatched":
				order_status_id = 4
			elif aggre_order_status == "Completed":
				order_status_id = 5
			elif aggre_order_status == "Cancelled":
				order_status_id = 7
			else:
				order_status_id = 1
			if order_status_id == 5:
				is_completed =  True
			else:
				is_completed = False
			if is_completed == True:
				is_paid = True
			else:
				is_paid = False
			if order_status_id == 5:
				delivery_time = updated_at
			else:
				delivery_time = None
			main_order_update = \
			main_order.update(Aggregator_order_status=aggre_order_status, order_status=order_status_id,\
										is_completed=is_completed,is_paid=is_paid,\
									 delivery_time=delivery_time)
			order_track = \
			OrderTracking.objects.create(order_id=main_order_id, Order_staus_name_id=order_status_id)
			return Response({
						"success": True, 
						"message": "Order Staus Update webhook mechanism api worked well!!"
						})
		except Exception as e:
			print("Order Status Update webhook mechanism Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})


