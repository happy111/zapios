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
from Configuration.models import *


	
class RetrieveTax(APIView):

	"""
	Tax POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used for retrieval of tax data.

		Data Post: {
			"id"                   : "1"
		}

		Response: {

			"success": True, 
			"message": "tax retrieval api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			err_message = {}
			err_message["id"] = \
					validation_master_anything(data["id"],"Tax Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})

			record = Tax.objects.filter(id=data['id'])
			if record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Provided Tax data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				q_dict = {}
				q_dict["id"] = record[0].id
				q_dict["tax_name"] = record[0].tax_name				
				q_dict["tax_percent"] = record[0].tax_percent
				q_dict["active_status"] = record[0].active_status
				q_dict["created_at"] = record[0].created_at
				q_dict["updated_at"] = record[0].updated_at
				final_result.append(q_dict)
			return Response({
						"success": True, 
						"message": "Tax retrieval api worked well!!",
						"data": final_result,
						})
		except Exception as e:
			print("Tax retrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})