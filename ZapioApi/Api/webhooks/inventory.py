from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from rest_framework import serializers
from datetime import datetime, timedelta
from urbanpiper.models import RawApiResponse, APIReference, OutletSync, CatSync, ProductSync,\
ProductOutletWise, CatOutletWise


class InventorySync(APIView):
	"""
	Inventory Hook POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used for handling webhook mechanism for store inventory in urbanpiper.

	"""
	def post(self, request, format=None):
		try:
			data = request.data
			now = datetime.now()
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
				outlet = api_ref[0].outlet_id
				url = "https://api.urbanpiper.com/external/api/v1/inventory/locations/"+str(outlet)+"/"
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
			cat_record = CatOutletWise.objects.filter(sync_outlet__outlet_id=outlet)
			product_record = ProductOutletWise.objects.filter(sync_outlet__outlet_id=outlet)
			if cat_record.count() != 0 and product_record.count() != 0:
				cat_update = cat_record.update(urban_event='created',sync_status='synced',\
									is_enabled=1,is_available=1,updated_at=now)
				product_update =  product_record.update(urban_event='created',sync_status='synced',\
									is_enabled=1,is_available=1,updated_at=now)
			else:
				return Response({
						"success": True, 
						"message": "Inventory webhook mechanism api does not work well!!"
						})
			return Response({
						"success": True, 
						"message": "Inventory webhook mechanism api worked well!!"
						})
		except Exception as e:
			print("Inventory webhook mechanism Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})
