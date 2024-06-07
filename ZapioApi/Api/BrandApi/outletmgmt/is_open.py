from rest_framework.views import APIView
from rest_framework.response import Response
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
from Product.models import ProductCategory


class OutletMgmtSerializer(serializers.ModelSerializer):
	class Meta:
		model = OutletProfile
		fields = '__all__'

class OutletIsOpen(APIView):
	"""
	Outlet Is Open POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to close or open Outlet.

		Data Post: {
			"id"                   		: "2",
			"is_open"             		: "false"
		}

		Response: {

			"success": True, 
			"message": "Outlet is closed now!!",
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
			if data["is_open"] == True:
				pass
			elif data["is_open"] == False:
				pass
			else:
				err_message["is_open"] = "Is Open data is not valid!!"
			err_message["id"] = \
						validation_master_anything(data["id"],
						"Outlet",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = OutletProfile.objects.filter(id=data["id"])
			if record.count() != 0:
				data["updated_at"] = datetime.now()
				if data["is_open"] == True:
					info_msg = "Outlet is open now!!"
				else:
					info_msg = "Outlet is closed now!!"
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
			final_result = []
			final_result.append(serializer.data)
			return Response({
						"success": True, 
						"message": info_msg,
						"data": final_result,
						})
		except Exception as e:
			print("Outlet Is Open Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})