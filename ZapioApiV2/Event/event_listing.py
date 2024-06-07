import re
import json
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
from datetime import datetime
from django.db.models import Q
from Brands.models import Company
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user
from Event.models import PrimaryEventType




class listEvent(APIView):

	"""
	Event listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of Event data.

	"""


	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			user = request.user.id
			# Get Company id
			cid = get_user(user)
			allevent = PrimaryEventType.objects.filter(active_status=1)
			final_result = []
			if allevent.count() > 0:
				for i in allevent:
					dict_event = {}
					dict_event['event_type'] = i.event_type
					dict_event['id'] = i.id
					dict_event['active_status'] = i.active_status
					final_result.append(dict_event)
				return Response({
								"success": True, 
								"data": final_result
						})
			else:
				return Response({
						"success": True, 
						"data": []})
		except Exception as e:
			print("Event listing Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})