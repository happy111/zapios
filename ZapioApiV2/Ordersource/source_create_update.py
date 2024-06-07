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
from Configuration.models import OrderSource

class SourceSerializer(serializers.ModelSerializer):
	class Meta:
		model = OrderSource
		fields = '__all__'

class SourceCreationUpdation(APIView):

	"""
	Order Source Creation & Updation POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create & update Order Source
		Data Post: {
			"id"                       : "1"(Send this key in update record case,else it is not required!!)
			"source_name"		       : "dddddd",
			"image"					   : "",
			"payment"                  : ""
		}

		Response: {

			"success": True, 
			"message": "Order Source creation/updation api worked well!!",
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
			err_message["source_name"] = only_required(data["source_name"],"Order Source")
			data['is_edit'] = 1
			data['payment'] = json.loads(data["payment"])
			if type(data["image"]) != str:
				im_name_path =  data["image"].file.name
				im_size = os.stat(im_name_path).st_size
				if im_size > 100*1024:
					err_message["image_size"] = "Source image can'nt excced the size more than 100kb!!"
			else:
				data["image"] = None
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			if "id" in data:
				unique_check = OrderSource.objects.filter(~Q(id=data["id"]),\
								Q(source_name=data["source_name"]),Q(company_id=cid))
			else:
				unique_check = OrderSource.objects.filter(Q(source_name=data["source_name"]),Q(company_id=cid))
			if unique_check.count() != 0:
				err_message["unique_check"] = "Order Source with this name already exists!!"
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
				source_record = OrderSource.objects.filter(id=data['id'])
				if source_record.count() == 0:
					return Response(
					{
						"success": False,
	 					"message": "Order Source data is not valid to update!!"
					}
					)
				else:
					if data["image"] == None:
						data["image"] = source_record[0].image
					else:
						pass
					data["updated_at"] = datetime.now()
					p_query = source_record.update(
						source_name=data['source_name'],
						image=data['image'],
						payment_method=data['payment']
						)
					if data["image"] != None and data["image"] != "":
						product = OrderSource.objects.get(id=data["id"])
						product.image = data["image"]
						product.save()
					else:
						pass
					if p_query:
						info_msg = "Order Source Name is updated successfully!!"
						return Response({
							"success": True, 
							"message": info_msg
						})
					else:
						return Response({
							"success": False, 
							"message": str(source_serializer.errors),
							})
			else:
				p_query = \
					OrderSource.objects.create(company_id=cid,
						source_name=data['source_name'],
						image=data['image'],
						payment_method=data['payment'],is_edit=1)
				if p_query:
					info_msg = "Source name is created successfully!!"
				else:
					print("something went wrong!!",source_serializer.errors)
					return Response({
						"success": False, 
						"message": str(source_serializer.errors),
						})
			return Response({
						"success": True, 
						"message": info_msg
						})
		except Exception as e:
			print("Source name creation/updation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})