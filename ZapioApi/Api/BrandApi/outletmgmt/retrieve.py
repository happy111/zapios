from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_201_CREATED, \
	HTTP_406_NOT_ACCEPTABLE, HTTP_200_OK, HTTP_503_SERVICE_UNAVAILABLE
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime


class OutletTimeRetrieval(APIView):
	"""
	Outlet Time retrieval POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of Outlet Time data within brand.

		Data Post: {
			"id"                   : "3"
		}

		Response: {

			"success": True, 
			"message": "Outlet Time retrieval api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			data["id"] = str(data["id"])
			err_message = {}
			err_message["id"] = \
					validation_master_anything(data["id"],
					"Outlet Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = OutletProfile.objects.filter(id=data['id'])
			if record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Required Outlet Time data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				q_dict = {}
				q_dict["id"] = record[0].id
				if record[0].opening_time != None and record[0].closing_time != None:
					q_dict["opening_time"] = record[0].opening_time.strftime("%I:%M %p")
					q_dict["closing_time"] = record[0].closing_time.strftime("%I:%M %p")
				else:
					q_dict["opening_time"] = None
					q_dict["closing_time"] = None
				final_result.append(q_dict)
			return Response({
						"success": True, 
						"message": "Outlet Time retrieval api worked well!!",
						"data": final_result,
						})
		except Exception as e:
			print("Outlet Time retrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})
