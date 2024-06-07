import os,re,json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
from datetime import datetime
from django.db.models import Q
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user
from rest_framework import serializers
from Configuration.models import Unit
from django.db import transaction
from django.utils.translation import gettext_lazy


class UnitSerializer(serializers.ModelSerializer):
	class Meta:
		model = Unit
		fields = '__all__'

class UnitCreationUpdation(APIView):

	"""
	Unit Creation & Updation POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create & update Unit
		Data Post: {
			"id"                       : "1"(Send this key in update record case,else it is not required!!)
			"unit_name"		           : "dddddd",
			"short_name"		       : "dddddd",
			"unit_details"              : []
		}

		Response: {

			"success": True, 
			"message": "Unit creation/updation api worked well!!",
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
			err_message["unit_name"] = only_required(data["unit_name"],"Unit Name")
			if len(data['unit_details']) > 0:
				for i in data['unit_details']:
					if i['unitValue'] == '' or i['unitValues'] == 'u=' or i['units'] == '' or i['unit'] == '':
						err_message['unit_detail'] = "Define Conversions is not blank!!"

			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			if "id" in data:
				unique_check = Unit.objects.filter(~Q(id=data["id"]),\
								Q(unit_name=data["unit_name"]),Q(company_id=cid))
			else:
				unique_check = Unit.objects.filter(Q(unit_name=data["unit_name"]),\
					Q(company_id=cid))
			if unique_check.count() != 0:
				err_message["unique_check"] = "Unit Name with this name already exists!!"
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
				unit_record = Unit.objects.filter(id=data['id'])
				if unit_record.count() == 0:
					return Response(
					{
						"success": False,
	 					"message": "Unit data is not valid to update!!"
					}
					)
				else:
					data["updated_at"] = datetime.now()
					unit_serializer = UnitSerializer(unit_record[0],data=data,partial=True)
					if unit_serializer.is_valid():
						data_info = unit_serializer.save()
						info_msg = "Unit Name is updated successfully!!"
						return Response({
						"success": True, 
						"message": info_msg
						})
					else:
						print("something went wrong!!",unit_serializer.errors)
						return Response({
							"success": False, 
							"message": str(unit_serializer.errors),
							})
			else:
				unit_serializer = UnitSerializer(data=data)
				if unit_serializer.is_valid():
					data_info = unit_serializer.save()
					info_msg = gettext_lazy("Unit name is created successfully!!")
				else:
					print("something went wrong!!",unit_serializer.errors)
					return Response({
						"success": False, 
						"message": str(unit_serializer.errors),
						})
			return Response({
						"success": True, 
						"message": info_msg
						})
		except Exception as e:
			print("Unit name creation/updation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})