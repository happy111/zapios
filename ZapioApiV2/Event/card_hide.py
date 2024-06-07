import os
import re
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
from datetime import datetime
from django.db.models import Max

#Serializer for api
from rest_framework import serializers
from Event.models import PrimaryEventType




class CardHide(APIView):

	"""
	Report card Action POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to hide report card.

		Data Post: {
			"key_name"                  : "today_sale",
		}

		Response: {
			"success": True, 
			"message": "Report Card is hide now!!",
		}

	"""
	
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			from django.db.models import Q
			data = request.data
			user = request.user.id
			cid = get_user(user)
			data['company'] = cid
			record = HistoryEvent.objects.filter(key_name=data["key_name"],company_id=cid)
			if record.count() != 0:
				record.update(is_key=0)
			else:
				return Response(
					{
						"success": False,
						"message": "Key Name is not valid to update!!"
					}
				)
			return Response({
						"success": True, 
						"message": "Report card is hide now!!",
						})
		except Exception as e:
			print("Report Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})