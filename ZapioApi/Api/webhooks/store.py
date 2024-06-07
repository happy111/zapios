from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime
from rest_framework import serializers
from datetime import datetime, timedelta
from urbanpiper.models import RawApiResponse, APIReference, OutletSync


class StoreSync(APIView):
	"""
	Outlet Hook POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used for handling webhook mechanism for store create/update in urbanpiper.

	"""
	def post(self, request, format=None):
		try:
			data = request.data
			reference_id = data["reference"]
			api_ref = APIReference.objects.filter(ref_id=reference_id)
			if api_ref.count() == 0:
				return Response({
					"success" : False,
					"message" : "Not successful!!"
					})
			else:
				api_ref_id = api_ref[0].id
				company = api_ref[0].company_id
				url = "https://api.urbanpiper.com/external/api/v1/stores/"
			record = RawApiResponse.objects.filter(ref_id=api_ref_id)
			if record.count() == 0:
				raw_create = RawApiResponse.objects.create(company_id=company,\
									api_response=data, url=url, ref_id_id=api_ref_id)
			else:
				raw_update = record.update(company_id=company,\
									api_response=data, url=url, ref_id=api_ref_id)
			record = RawApiResponse.objects.filter(ref_id=api_ref_id)
			q = record[0]
			api_response = q.api_response
			api_stores = api_response["stores"]
			for i in api_stores:
				zapio_id = i["ref_id"]
				upipr_status = i["upipr_status"]
				urban_piper_store_id = upipr_status["id"]
				if upipr_status["action"] == "A":
					urban_event = "created"
				else:
					urban_event = "updated"
				sync_status = "synced"
				ref_id = api_ref_id
				sync_record = OutletSync.objects.filter(outlet_id=zapio_id)
				sync_update = sync_record.update(ref_id=ref_id,is_synced=1,sync_status=sync_status,\
										urban_event=urban_event,action_at=datetime.now(),\
										urbanpiper_store_id=urban_piper_store_id)
			return Response({
						"success": True, 
						"message": "Store webhook mechanism api worked well!!"
						})
		except Exception as e:
			print("Store webhook mechanism Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})
