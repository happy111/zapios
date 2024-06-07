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
from ZapioApi.Api.urbanpiper.Validation.outletaction_error_check import *
import requests
import json
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user

def store_action(data,company_id,outlet_id):
	url = "https://api.urbanpiper.com/hub/api/v1/location/"
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
		event_type_q = EventTypes.objects.filter(company=company_id,event_type="store_action")
		if event_type_q.count() == 0:
			return None
		else:
			event_type_id = event_type_q[0].id
		if response_data["status"] != "error":
			record_create = \
			APIReference.objects.create(company_id=company_id,event_type_id=event_type_id,\
											ref_id=response_data["reference_id"],
											api_response=response_data,outlet_id=outlet_id)
		else:
			record_create = \
			APIReference.objects.create(company_id=company_id,event_type_id=event_type_id,\
											ref_id=response_data["reference_id"],
											error_api_response=response_data,outlet_id=outlet_id)
		return response_data





class OutletAction(APIView):
	permission_classes = (IsAuthenticated,)
	"""
	Outlet Syncing POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for enabling/disabling outlets with UrbanPiper.

		Data Post: {
			"outlet_id"                    : "1",
			"store_status"                 : "true"
		}

		Response: {

			"success": True, 
			"message": "Store is enabled successfully!!"
		}
	"""
	
	def post(self, request):
		try:
			auth_id = request.user.id
			Company_id = get_user(auth_id)
			record = OutletSync.objects.filter(company_id=Company_id)
			if record.count() == 0:
				return ({
					"status" : True,
					"message" : "No outlets!!"
					})
			else:
				company_id = Company_id
			data = request.data
			validation_check = err_check(data)
			if validation_check != None:
				return Response(validation_check) 
			record_check = integrity_check(data,company_id)
			if record_check != None:
				return Response(record_check)
			record = record.filter(id=data["outlet_id"])
			q = record[0]
			action_data = {}
			action_data["location_ref_id"] = str(q.outlet_id)
			action_data["platforms"] = ["urbanpiper"]
			if data["store_status"] == "true":
				msg_info = "Store is enabled successfully!!"
				action_data["action"] = "enable"
			else:
				msg_info = "Store is disabled successfully!!"
				action_data["action"] = "disable"
			urban_action = store_action(action_data,company_id,action_data["location_ref_id"])
			if urban_action == None:
				return Response({
							"status":False,
							"message" : "Store action is not successful!!"
							})
			else:
				pass
			return Response({
							"status":True,
							"message" : msg_info
							})
		except Exception as e:
			print(e)
			return Response(
						{"error":str(e)}
						)



