from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Brands.models import Company
#Serializer for api
from rest_framework import serializers
from django.db.models import Q
from datetime import datetime, timedelta
from urbanpiper.models import UrbanCred, APIReference, ProductSync
from Outlet.models import OutletProfile
from datetime import datetime, timedelta
import requests
import json
from zapio.settings import Media_Path
from Product.models import Variant, AddonDetails, Addons
from Configuration.models import DeliverySetting
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user

def action_sync(data,company_id, outlet_id):
	url = "https://api.urbanpiper.com/hub/api/v1/items/"
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
		response = requests.request("POST", url, data=json.dumps(data), headers=headers)
		response_data = response.json()
		event_type_q = EventTypes.objects.filter(company=company_id,event_type="item_state_toggle")
		if event_type_q.count() == 0:
			return None
		else:
			event_type_id = event_type_q[0].id
		ref_q = APIReference.objects.all()
		if ref_q.count() == 0:
			last_id = "001"
		else:
			last_id = str(ref_q.last().id+1)
		if response_data["status"] != "error":
			if "reference" not in response_data:
				response_data["reference"] = "unknown-"+last_id
			else:
				pass
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





def ItemAction(product_id, outlet_id, is_available):
	data = {}
	outlet_product_q = \
	ProductOutletWise.objects.filter(sync_product__product=product_id,sync_outlet__outlet=outlet_id)
	if is_available == True:
		data["action"] = "enable"
	else:
		data["action"] = "disable"
	data["option_ref_ids"] = []
	data["item_ref_ids"] = []
	product_q = ProductSync.objects.filter(product=product_id)
	for i in product_q:
		p_id = "I-"+str(i.id)
		data["item_ref_ids"].append(p_id)
	data["location_ref_id"] = str(outlet_id)
	company_id = product_q[0].company_id
	urban_action = action_sync(data, company_id, outlet_id)
	if urban_action != None:
		outlet_product_update = outlet_product_q.update(product_status='in_progress')
		return "Action done successfully!!"
	else:
		return None





