import os,re,json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
from datetime import datetime
from django.db.models import Q
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user
from rest_framework import serializers
from Location.models import AreaMaster
from django.db import transaction
from django.utils.translation import gettext_lazy

class AreaSerializer(serializers.ModelSerializer):
	class Meta:
		model = AreaMaster
		fields = '__all__'

class LocalityCreationUpdation(APIView):

	"""
	Locality Creation & Updation POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create & update Locality
		Data Post: {
			"id"                       : "1"(Send this key in update record case,else it is not required!!)
			"city"		               : "4",
			"area"					   : "South Ex"
		}

		Response: {

			"success"  : True, 
			"message"  : "Locality creation/updation api worked well!!",
			"data"     : final_result
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
			err_message["area"] = only_required(data["area"],"Area")
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			if "id" in data:
				unique_check = AreaMaster.objects.filter(~Q(id=data["id"]),\
								Q(area=data["area"]),Q(city_id=data['city']),Q(company_id=cid))
			else:
				unique_check = AreaMaster.objects.filter(Q(area=data['area']),\
										Q(city_id=data["city"]),Q(company_id=cid))
			if unique_check.count() != 0:
				err_message["unique_check"] = "Area with this name already exists!!"
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
				area_record = AreaMaster.objects.filter(id=data['id'])
				if area_record.count() == 0:
					return Response(
					{
						"success": False,
	 					"message": "City data is not valid to update!!"
					}
					)
				else:
					data["updated_at"] = datetime.now()
					area_serializer = AreaSerializer(area_record[0],data=data,partial=True)
					if area_serializer.is_valid():
						data_info = area_serializer.save()
						info_msg = "Area Name is updated successfully!!"
						return Response({
							"success": True, 
							"message": info_msg
						})
					else:
						print("something went wrong!!",area_serializer.errors)
						return Response({
							"success": False, 
							"message": str(area_serializer.errors),
							})
			else:
				area_serializer = AreaSerializer(data=data)
				if area_serializer.is_valid():
					data_info = area_serializer.save()
					info_msg = gettext_lazy("Area name is created successfully!!")
				else:
					print("something went wrong!!",area_serializer.errors)
					return Response({
						"success": False, 
						"message": str(area_serializer.errors),
						})
			return Response({
						"success": True, 
						"message": info_msg
						})
		except Exception as e:
			print("Locality creation/updation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})