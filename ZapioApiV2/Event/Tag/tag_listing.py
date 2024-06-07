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
from Event.models import PrimaryEventType,EventTag




class listEventTag(APIView):

	"""
	Tag listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of Tag data.

	"""


	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			user = request.user.id
			# Get Company id
			cid = get_user(user)
			alltag = EventTag.objects.filter(company_id=cid)
			final_result = []
			if alltag.count() > 0:
				for i in alltag:
					dict_event = {}
					dict_event['tag_name'] = i.tag_name
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
			print("Tag listing Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})