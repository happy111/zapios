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
import os
from django.db.models import Max

#Serializer for api
from rest_framework import serializers
from kitchen.models import StepToprocess


class ProcessAction(APIView):
	"""
	Process Action POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to activate or deactivate all product process.

		Data Post: {
			"p_id"                   	: "21",
			"v_id"						: "43",
			"active_status"             : "0"
		}

		Response: {

			"success": True, 
			"message": "Product Process is deactivated now!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			from django.db.models import Q
			data = request.data
			err_message = {}
			if str(data["active_status"]) == "0":
				pass
			elif str(data["active_status"]) == "1":
				pass
			else:
				err_message["active_status"] = "Active status data is not valid!!"
			err_message["p_id"] = \
						validation_master_anything(data["p_id"],
						"Product Id",contact_re, 1)
			err_message["v_id"] = \
						validation_master_anything(data["v_id"],
						"Variant Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			data["active_status"] = int(data["active_status"]) 
			record = StepToprocess.objects.filter(product=data["p_id"],varient=data["v_id"])
			if record.count() != 0:
				data["updated_at"] = datetime.now()
				if data["active_status"] == 1:
					info_msg = "Product process is activated successfully!!"
				else:
					info_msg = "Product process is deactivated successfully!!"
				record.update(active_status=data['active_status'],updated_at=data['updated_at'])
			else:
				return Response(
					{
						"success": False,
						"message": "Product process id is not valid to update!!"
					}
					)
			return Response({
						"success": True, 
						"message": info_msg
						})
		except Exception as e:
			print("Product process action Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})