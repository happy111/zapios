from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Brands.models import Company
#Serializer for api
from rest_framework import serializers
from django.db.models import Q
from datetime import datetime, timedelta
from urbanpiper.models import OutletSync, UrbanCred, APIReference, EventTypes
from Outlet.models import OutletProfile
from datetime import datetime, timedelta
from ZapioApi.Api.urbanpiper.Validation.outletsync_error_check import *
import requests
import json
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user


def urban_slot_converter(open_time,close_time):
	timings = []
	for i in range(1,8):
		if i == 1:
			day = "monday"
		elif i == 2:
			day = "tuesday"
		elif i == 3:
			day = "wednesday"
		elif i == 4:
			day = "thursday"
		elif i == 5:
			day = "friday"
		elif i == 6:
			day = "saturday"
		else:
			day = "sunday"
		slot_data = {}
		slot_data["day"] = day
		slot_data["slots"] = []
		timimg = {}
		timimg["start_time"] = open_time
		timimg["end_time"] = close_time
		slot_data["slots"].append(timimg)
		timings.append(slot_data)
	return timings


def store_sync(data,company_id):
	url = "https://api.urbanpiper.com/external/api/v1/stores/"
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
		event_type_q = EventTypes.objects.filter(company=company_id,event_type="store_creation")
		if event_type_q.count() == 0:
			return None
		else:
			event_type_id = event_type_q[0].id
		if response_data["status"] != "error":
			record_create = \
			APIReference.objects.create(company_id=company_id,event_type_id=event_type_id,\
											ref_id=response_data["reference"],
											api_response=response_data)
		else:
			record_create = \
			APIReference.objects.create(company_id=company_id,event_type_id=event_type_id,\
											ref_id=response_data["reference"],
											error_api_response=response_data)
		return response_data





class OutletToSync(APIView):
	"""
	Outlet Syncing POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for syncing outlets with UrbanPiper.

		Data Post: {
			"outlet_ids"                   : ["1","2"]
		}

		Response: {

			"success": True, 
			"message": "Syncing of outlet is initiated successfully!!"
		}
	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request):
		try:
			auth_id = request.user.id
			Company_id = get_user(auth_id)
			record = OutletSync.objects.filter(company=Company_id)
			if record.count() == 0:
				return ({
					"status" : True,
					"message" : "No outlet to sync!!"
					})
			else:
				company_id = record[0].company_id
			data = request.data
			validation_check = err_check(data)
			if validation_check != None:
				return Response(validation_check) 
			record_check = integrity_check(data,company_id)
			if record_check != None:
				return Response(record_check)
			sync_data = {}
			sync_data["stores"] = []
			for i in data["outlet_ids"]:
				data_dict = {}
				outlet_record = OutletProfile.objects.filter(id=i)
				q = outlet_record[0]
				data_dict["city"] = q.city.city
				data_dict["name"] = q.Outletname
				data_dict["min_pickup_time"] = 900
				data_dict["min_delivery_time"] = 1800
				data_dict["contact_phone"] = q.Company.support_person_mobileno
				data_dict["notification_phones"] = []
				data_dict["notification_phones"].append(data_dict["contact_phone"])
				data_dict["ref_id"] = str(q.id)
				data_dict["min_order_value"] = 100
				data_dict["hide_from_ui"] = False
				data_dict["address"] = q.address
				data_dict["notification_emails"] = []
				data_dict["notification_emails"].append(q.Company.support_person_email_id)
				data_dict["zip_codes"] = []
				data_dict["geo_longitude"] = q.longitude
				data_dict["active"] = q.active_status
				data_dict["geo_latitude"] = q.latitude
				data_dict["ordering_enabled"] = True
				data_dict["translations"] = []
				data_dict["excluded_platforms"] = []
				data_dict["included_platforms"] = ["swiggy","zomato"]
				HMS = "%H:%M:%S"
				open_time = q.opening_time.strftime(HMS)
				close_time = q.closing_time.strftime(HMS)
				data_dict["timings"] = urban_slot_converter(open_time,close_time)
				sync_data["stores"].append(data_dict)
				record_update = record.filter(outlet=i).update(sync_status="in_progress")
			urban_sync = store_sync(sync_data,company_id)
			if urban_sync == None:
				revert = record.update(sync_status='not_intiated')
				return Response({
							"status":False,
							"message" : "Syncing of outlet is not initiated successfully!!"
							})
			else:
				pass
			return Response({
							"status":True,
							"message" : "Syncing of outlet is initiated successfully!!"
							})
		except Exception as e:
			return Response(
						{"error":str(e)}
						)



