from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Brands.models import Company
#Serializer for api
from rest_framework import serializers
from django.db.models import Q
from datetime import datetime, timedelta
from urbanpiper.models import OutletSync, UrbanCred, APIReference, EventTypes, \
CatSync, ProductSync, ProductOutletWise, UrbanOrders
from Outlet.models import OutletProfile
from datetime import datetime, timedelta
import requests
import json
from Orders.models import Order, OrderTracking

def order_sync_update(data,company_id, outlet_id,urban_order_id):
	url = "https://api.urbanpiper.com/external/api/v1/orders/"+str(urban_order_id)+"/status/"
	data = data
	q = UrbanCred.objects.filter(company_id=company_id,active_status=1)
	if q.count() == 0:
		return None
	else:
		apikey = q[0].apikey
		username = q[0].username
		headers = {}
		headers["Authorization"] = "apikey "+ username +":"+apikey
		headers["Content-Type"] = "application/json"
		response = requests.request("PUT", url, data=json.dumps(data), headers=headers)
		response_data = response.json()
		event_type_q = EventTypes.objects.filter(company=company_id,event_type="order_status_update")
		if event_type_q.count() == 0:
			return None
		else:
			event_type_id = event_type_q[0].id
		ref_q = APIReference.objects.all()
		if ref_q.count() == 0:
			last_id = "001"
		else:
			last_id = str(ref_q.last().id+1)
		if "reference" not in response_data:
			response_data["reference"] = "unknown-"+last_id
		else:
			pass
		if response_data["status"] != "error":
			record_create = \
			APIReference.objects.create(company_id=company_id,event_type_id=event_type_id,\
											ref_id=response_data["reference"],
											api_response=response_data,outlet_id=outlet_id)
		else:
			record_create = \
			APIReference.objects.create(company_id=company_id,event_type_id=event_type_id,\
											ref_id=response_data["reference"],
											error_api_response=response_data,outlet_id=outlet_id)
		return response_data





def Order_status_update(urban_order_id, status_change):
	data = {}
	data["new_status"] = status_change
	data["message"] = "Order status changed successfully!!"
	if data["new_status"] == "Acknowledged":
		order_status_id = 2
	else:
		order_status_id = 3
	action_time = datetime.now()
	Urbanorder_record = \
	UrbanOrders.objects.filter(order_id=urban_order_id)
	company_id = Urbanorder_record[0].Company_id
	outlet_id = Urbanorder_record[0].outlet_id
	urban_action = order_sync_update(data, company_id, outlet_id, urban_order_id)
	if urban_action != None:
		urban_order_update = Urbanorder_record.update(order_state=data["new_status"])
		main_order = Order.objects.filter(urban_order_id = urban_order_id)
		main_order_update = \
		main_order.update(Aggregator_order_status=data["new_status"],\
			order_status=order_status_id,is_accepted=1)
		order_id = main_order[0].id
		order_track = \
		OrderTracking.objects.create(order_id=order_id, Order_staus_name_id=order_status_id)
		return "Action done successfully!!"
	else:
		return None






