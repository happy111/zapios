from rest_framework.views import APIView
from rest_framework.response import Response
import json
from datetime import datetime
from datetime import datetime, timedelta
from urbanpiper.models import OutletSync, OrderStatusRawApiResponse, UrbanOrders, RawApiResponse,\
ProductOutletWise
from rest_framework_tracking.mixins import LoggingMixin
from rest_framework import serializers



class ItemToggle(LoggingMixin, APIView):
	"""
	Item Toggle Hook POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used for handling webhook mechanism for item toggle in urbanpiper.

	"""
	def post(self, request, format=None):
		try:
			data = request.data
			url = "https://api.urbanpiper.com/hub/api/v1/items/"
			api_response = data
			for i in data['status']:
				outlet_id = i['location']['ref_id']
			updated_at = datetime.now()
			company_id = ProductOutletWise.objects.\
					filter(sync_outlet__outlet=outlet_id)[0].sync_outlet.company_id
			rawapi_create = \
			RawApiResponse.objects.create(company_id=company_id, api_response=api_response,\
										url=url,created_at=updated_at)
			if data['action'] == 'stock-in':
				product_status = 'enabled'
				is_available = True
			else:
				product_status = 'disabled'
				is_available = False
			for i in data['status']:
				outlet_id = i['location']['ref_id']
				for j in i['items']:
					product_id = j['ref_id']
					final_product_id = product_id.replace('I-','')
					record = \
					ProductOutletWise.objects.filter(sync_product=final_product_id,\
								sync_outlet__outlet=outlet_id, product_status='in_progress')
					record_update = \
					record.update(product_status=product_status, is_available=is_available,\
									updated_at=updated_at)
			return Response({
				"success" : True,
				"message" : "Item Toggle webhook mechanism api worked well!!"
				})
		except Exception as e:
			print("Item Toggle webhook mechanism Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})
