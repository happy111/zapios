from rest_framework.views import APIView
from rest_framework.response import Response
import json
from datetime import datetime
from datetime import datetime, timedelta
from urbanpiper.models import RawApiResponse, APIReference, OutletSync, ActionSync
from rest_framework_tracking.mixins import LoggingMixin


class StoreAction(LoggingMixin, APIView):
	"""
	Outlet Action Hook POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used for handling webhook mechanism for store enable/disable in urbanpiper.

	"""
	def post(self, request, format=None):
		try:
			data = request.data
			reference_id = data["reference_id"]
			api_ref = APIReference.objects.filter(ref_id=reference_id)
			if api_ref.count() == 0:
				return Response({
					"success" : False,
					"message" : "Not successful!!"
					})
			else:
				api_ref_id = api_ref[0].id
				company = api_ref[0].company_id
				url = "https://api.urbanpiper.com/hub/api/v1/location/"
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
			if "action" in api_response:
				outlet_id = api_response["location_ref_id"]
				sync_record = OutletSync.objects.filter(outlet_id=outlet_id)
				sync_id = sync_record[0].id
				company = sync_record[0].company_id
				updated_at = datetime.now()
				ref_id = api_ref_id
				if api_response["action"] == "enable":
					is_enabled = 1
					urban_event = 'enabled'
				else:
					is_enabled = 0
					urban_event = 'disabled'
				action_record = ActionSync.objects.filter(sync_outlet=sync_id) 
				if action_record.count() == 0:
					action_create = ActionSync.objects.create(company_id = company,\
							 sync_outlet_id = sync_id, ref_id_id=ref_id, is_enabled=is_enabled,\
							 urban_event=urban_event)
				else:
					action_update = action_record.update(company_id = company,\
							 sync_outlet_id = sync_id, ref_id_id=ref_id, is_enabled=is_enabled,\
							 urban_event=urban_event, updated_at = updated_at)
			else:
				return Response({
						"success": False, 
						"message": "Not successful!!"
					})
			return Response({
						"success": True, 
						"message": "Store action webhook mechanism api worked well!!"
						})
		except Exception as e:
			print("Store action webhook mechanism Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})
