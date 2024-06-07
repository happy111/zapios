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
from Configuration.models import *

class TaxSerializer(serializers.ModelSerializer):
	class Meta:
		model = TaxSetting
		fields = '__all__'

class TaxCreationUpdation(APIView):

	"""
	Tax Creation & Updation POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create & update Tax
		Data Post: {
			"id"                       : "1"(Send this key in update record case,else it is not required!!)
			"tax_name"		           : "dddddd",
			"tax_percent"              : []
		}

		Response: {

			"success": True, 
			"message": "Tax creation/updation api worked well!!",
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
			err_message["tax_name"] = only_required(data["tax_name"],"Tax Name")
			err_message["tax_percent"] = only_required(data["tax_percent"],"Tax Percent")
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			if "id" in data:
				unique_check = Tax.objects.filter(~Q(id=data["id"]),\
								Q(tax_name=data["tax_name"]),Q(company_id=cid))
			else:
				unique_check = Tax.objects.filter(Q(tax_name=data["tax_name"]),Q(company_id=cid))
			if unique_check.count() != 0:
				err_message["unique_check"] = "Tax Name with this name already exists!!"
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
				tax_record = Tax.objects.filter(id=data['id'])
				if tax_record.count() == 0:
					return Response(
					{
						"success": False,
	 					"message": "Tax data is not valid to update!!"
					}
					)
				else:
					data["updated_at"] = datetime.now()
					tax_serializer = TaxSerializer(tax_record[0],data=data,partial=True)
					if tax_serializer.is_valid():
						data_info = tax_serializer.save()
						info_msg = "Tax Name is updated successfully!!"
						return Response({
						"success": True, 
						"message": info_msg
						})
					else:
						print("something went wrong!!",tax_serializer.errors)
						return Response({
							"success": False, 
							"message": str(tax_serializer.errors),
							})
			else:
				tax_serializer = TaxSerializer(data=data)
				if tax_serializer.is_valid():
					data_info = tax_serializer.save()
					info_msg = "Tax name is created successfully!!"
				else:
					print("something went wrong!!",tax_serializer.errors)
					return Response({
						"success": False, 
						"message": str(tax_serializer.errors),
						})
			return Response({
						"success": True, 
						"message": info_msg
						})
		except Exception as e:
			print("Tax name creation/updation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})