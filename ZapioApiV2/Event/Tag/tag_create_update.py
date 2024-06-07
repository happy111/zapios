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
from Event.models import PrimaryEventType,EventTag

class TagSerializer(serializers.ModelSerializer):
	class Meta:
		model = EventTag
		fields = '__all__'

class EventTagCreationUpdation(APIView):

	"""
	Tag Creation & Updation POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create & update Tag.
		Data Post: {
			"id"                       : "1"(Send this key in update record case,else it is not required!!)
			"tag_name"		           : "Outlet name",
		}
		Response: {

			"success": True, 
			"message": "Tag creation/updation api worked well!!",
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
			err_message["tag_name"] = only_required(data["tag_name"],"Tag Name")
			if any(err_message.values())==True:
				return Response({
					"success" : False,
					"error"   : err_message,
					"message" : "Please correct listed errors!!"
					})
			if "id" in data:
				unique_check = EventTag.objects.filter(~Q(id=data["id"]),\
								Q(tag_name=data["tag_name"]),Q(company_id=cid))
			else:
				unique_check = EventTag.objects.filter(Q(tag_name=data["tag_name"]),Q(company_id=cid))
			if unique_check.count() != 0:
				err_message["unique_check"] = "Tag Name with this name already exists!!"
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
				tag_record = EventTag.objects.filter(id=data['id'])
				if tag_record.count() == 0:
					return Response(
					{
						"success": False,
	 					"message": "Tag data is not valid to update!!"
					}
					)
				else:
					data["updated_at"] = datetime.now()
					tag_serializer = TagSerializer(tag_record[0],data=data,partial=True)
					if tag_serializer.is_valid():
						data_info = tag_serializer.save()
						info_msg = "Tag Name is updated successfully!!"
						return Response({
							"success": True, 
							"message": info_msg
						})
					else:
						print("something went wrong!!",tag_serializer.errors)
						return Response({
							"success": False, 
							"message": str(tag_serializer.errors),
							})
			else:
				tag_serializer = TagSerializer(data=data)
				if tag_serializer.is_valid():
					data_info = tag_serializer.save()
					info_msg = "Tag is created successfully!!"
				else:
					print("something went wrong!!",tag_serializer.errors)
					return Response({
						"success": False, 
						"message": str(tag_serializer.errors),
						})
			return Response({
						"success": True, 
						"message": info_msg
						})
		except Exception as e:
			print("Tag creation/updation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})