from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime

from rest_framework import serializers
from discount.models import DiscountReason



	
class ReasonRetrieve(APIView):

	"""
	Discount Reason POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used for retrieval of Discount Reason data.

		Data Post: {
			"id"                   : "1"
		}

		Response: {

			"success": True, 
			"message": "Discount Reason retrieval api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			err_message = {}
			err_message["id"] = \
					validation_master_anything(data["id"],
					"Discount Reason Id",contact_re, 1)

			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})

			record = DiscountReason.objects.filter(id=data['id'])
			if record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Provided Discount reason data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				q_dict = {}
				q_dict["id"] = record[0].id
				q_dict["reason"] = record[0].reason
				q_dict["active_status"] = record[0].active_status
				q_dict["created_at"] = record[0].created_at
				q_dict["updated_at"] = record[0].updated_at
				final_result.append(q_dict)
			return Response({
						"success": True, 
						"message": "Discount Reason retrieval api worked well!!",
						"data": final_result,
						})
		except Exception as e:
			print("Discount Reason retrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})