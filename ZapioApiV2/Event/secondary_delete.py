import json
import re
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
from datetime import datetime

#Serializer for api
from rest_framework import serializers
from Event.models import SecondaryEventType



	
class DeleteSecondaryEvent(APIView):

	"""
	Delete POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used for delete of Event data.

		Data Post: {
			"id"                   : "1"
		}

		Response: {

			"success": True, 
			"message": "Event type delete api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			err_message = {}
			err_message["id"] = \
					validation_master_anything(data["id"],"Event Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = SecondaryEventTypeobjects.filter(id=data['id'])
			if record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Provided Event data is not valid to retrieve!!"
				}
				)
			else:
				record.delete()
			return Response({
						"success": True, 
						"message": "Event type delete api worked well!!",
						})
		except Exception as e:
			print("Event retrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})