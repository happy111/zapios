from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime
from django.db.models import Q
import os
from django.db.models import Max
from ZapioApi.Api.BrandApi.Validation.category_error_check import *

#Serializer for api
from rest_framework import serializers
from Product.models import ProductCategory
from UserRole.models import RollPermission
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user

class PermissionSerializer(serializers.ModelSerializer):
	class Meta:
		model = RollPermission
		fields = '__all__'


class SavePermission(APIView):
	"""
	User Permission Creation & Updation POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create & update user permission within brand.

		Data Post: {
			Hints : 0 = edit 1 = view 2 = None

			"user_type"		       : "1",
			"main_route"		   : "1",
			"label"	               : 0,

		}

		Response: {

			"success": True, 
			"message": "Category Added Successfully!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			sdata = RollPermission.objects.filter(user_type_id=11)
			auth_id = request.user.id
			cid = get_user(auth_id)
			data['Company'] = cid
			per_data = {}
			user_type = data['user_type']
			main_module = data['main_route']
			per_label = data['label']
			roll_count = RollPermission.objects.filter(Q(user_type_id=user_type),Q(company_id=cid),Q(main_route_id=main_module))
			if roll_count.count() > 0:
				data['label'] = int(data['label'])
				per_serializer = PermissionSerializer(roll_count[0],data=data,partial=True)
				if per_serializer.is_valid():
					data_info = per_serializer.save()
			else:
				per_serializer = PermissionSerializer(data=data)
				if per_serializer.is_valid():
					data_info = per_serializer.save()
				else:
					print("something went wrong!!",per_serializer.errors)
					return Response({
						"success": False, 
						"message": str(per_serializer.errors),
						})
			return Response({
						"success": True, 
						"message": "User Role api worked well!!",
						})
		except Exception as e:
			print("User Roll Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})
