from rest_framework.views import APIView
from rest_framework.response import Response
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime
import os
from django.db.models import Q
from Product.models import Tag
from ZapioApi.Api.BrandApi.tag.serializer import TagSerializer
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user


class TagCreationUpdation(APIView):

	"""
	Tag Creation & Updation POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create & update Tag.

		Data Post: {
			"id"                       : "1"(Send this key in update record case,else it is not required!!)
			"tag_name"		           : "dddddd",
			"tag_image"                 : "a.jpg"
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
			if type(data["tag_image"]) != str:
				im_name_path =  data["tag_image"].file.name
				im_size = os.stat(im_name_path).st_size
				if im_size > 50*1024:
					err_message["image_size"] = "Tag Icon can'nt excced the size more than 50kb!!"
				else:
					pass
			else:
				data["tag_image"] = None
			# err_message["tag_name"] = \
			# 		validation_master_anything(data["tag_name"],
			# 		"Tag Name",alpha_re, 2)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			if "id" in data:
				unique_check = Tag.objects.filter(~Q(id=data["id"]),\
								Q(tag_name=data["tag_name"]))
			else:
				unique_check = Tag.objects.filter(Q(tag_name=data["tag_name"]))
			if unique_check.count() != 0:
				err_message["unique_check"] = "Tag with this name already exists!!"
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
				tag_record = Tag.objects.filter(id=data['id'])
				if tag_record.count() == 0:
					return Response(
					{
						"success": False,
	 					"message": "Tag data is not valid to update!!"
					}
					)
				else:
					if data["tag_image"] == None:
						data["tag_image"] = tag_record[0].tag_image
					else:
						pass
					data["updated_at"] = datetime.now()
					tag_serializer = TagSerializer(tag_record[0],data=data,partial=True)
					if tag_serializer.is_valid():
						data_info = tag_serializer.save()
						info_msg = "Product tag is updated successfully!!"
						return Response({
						"success": True, 
						"message": info_msg
						})
					else:
						print("something went wrong!!",tag_serializer.errors)
						return Response({
							"success": False, 
							"message": str(tag.errors),
							})
			else:
				tag_serializer = TagSerializer(data=data)
				if tag_serializer.is_valid():
					data_info = tag_serializer.save()
					info_msg = "Product tag is created successfully!!"
				else:
					print("something went wrong!!")
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