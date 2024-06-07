from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime
from django.db.models import Max
import dateutil.parser

#Serializer for api
from rest_framework import serializers
from .is_open import OutletMgmtSerializer

class OutletTiming(APIView):
	"""
	Outlet Set Timing POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to set opening and closing time of Outlet.

		Data Post: {
			"id"                   		: "2",
			"opening_time"		   		: "15:00:00.835531",
			"closing_time"		   		: "19:39:39.835531"
		}

		Response: {

			"success": True, 
			"message": "Outlet timing is changed now!!"
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			err_message = {}
			err_message["id"] = \
						validation_master_anything(data["id"],
						"Outlet",contact_re, 1)
			if data["opening_time"] != "" and data["closing_time"] != "":
				try:
					open_time = dateutil.parser.parse(data["opening_time"]).time()
					close_time = dateutil.parser.parse(data["closing_time"]).time()
				except Exception as e:
					err_message["time"] = \
						"Please provide meaningfull opening & closing time!!" 
				# if open_time > close_time:
				# 	err_message["time"] = \
				# 		"Please provide meaningfull opening & closing time!!" 
				# # else:
				# # 	pass
			else:
				err_message["time"] = \
						"Please set reporting time!!"
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			data["opening_time"] = open_time
			data["closing_time"] = close_time
			record = OutletProfile.objects.filter(id=data["id"])
			if record.count() != 0:
				data["updated_at"] = datetime.now()
				serializer = \
				OutletMgmtSerializer(record[0],data=data,partial=True)
				if serializer.is_valid():
					data_info = serializer.save()
				else:
					print("something went wrong!!")
					return Response({
						"success": False, 
						"message": str(serializer.errors),
						})
			else:
				return Response(
					{
						"success": False,
						"message": "Outlet id is not valid to update!!"
					}
					)
			return Response({
						"success": True, 
						"message": "Outlet timing is changed now!!"
						})
		except Exception as e:
			print("Outlet timing Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})