import os
import re
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
from datetime import datetime
from django.db.models import Q
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user
from rest_framework import serializers
from Location.models import CityMaster

class CitySerializer(serializers.ModelSerializer):
	class Meta:
		model = CityMaster
		fields = '__all__'

class CityCreationUpdation(APIView):

	"""
	City Creation & Updation POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create & update City
		Data Post: {
			"id"                       : "1"(Send this key in update record case,else it is not required!!)
			"city"		               : "New Delhi",
		}

		Response: {

			"success": True, 
			"message": "City creation/updation api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			user = request.user.id
			cid = get_user(user)
			data['company'] = cid
			err_message = {}
			err_message["city"] = only_required(data["city"],"City")
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			data['state'] = 1
			if "id" in data:
				unique_check = CityMaster.objects.filter(~Q(id=data["id"]),\
								Q(city=data["city"]),Q(company_id=cid))
			else:
				unique_check = CityMaster.objects.filter(Q(city=data["city"]),Q(company_id=cid))
			if unique_check.count() != 0:
				err_message["unique_check"] = "City with this name already exists!!"
			else:
				pass
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			data["active_status"] = 1
			if "id" in data:
				city_record = CityMaster.objects.filter(id=data['id'])
				if city_record.count() == 0:
					return Response(
					{
						"success": False,
	 					"message": "City data is not valid to update!!"
					}
					)
				else:
					data["updated_at"] = datetime.now()
					city_serializer = CitySerializer(city_record[0],data=data,partial=True)
					if city_serializer.is_valid():
						data_info = city_serializer.save()
						info_msg = "City Name is updated successfully!!"
						return Response({
							"success": True, 
							"message": info_msg
						})
					else:
						print("something went wrong!!",city_serializer.errors)
						return Response({
							"success": False, 
							"message": str(city_serializer.errors),
							})
			else:
				city_serializer = CitySerializer(data=data)
				if city_serializer.is_valid():
					data_info = city_serializer.save()
					info_msg = "City name is created successfully!!"
				else:
					print("something went wrong!!",city_serializer.errors)
					return Response({
						"success": False, 
						"message": str(city_serializer.errors),
						})
			return Response({
						"success": True, 
						"message": info_msg
						})
		except Exception as e:
			print("City creation/updation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})