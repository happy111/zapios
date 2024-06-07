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
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user

#Serializer for api
from rest_framework import serializers
from Product.models import ProductCategory


class GetSubcategory(APIView):
	"""
	Sub-Catagory listing Configuration POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to provide all Sub-Catagory within catagory.

		Data Post: {

			"cat_id" 	    : [1,2]
		}

		Response: {

			"success": True,
			"data" : subcatagory_conf_data_serializer,
			"message": "Sub-Catagory fetching successful!!"
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			subcatagory_conf_data_serializer = []
			for index in data['cat_id']:
				query = ProductsubCategory.objects.filter(category=index).order_by('-created_at')
				if query.count() > 0:
					for q in query:
						q_dict = {}
						q_dict["key"] = q.id
						q_dict["value"] = q.id 
						q_dict["label"] = q.subcategory_name
						subcatagory_conf_data_serializer.append(q_dict)
			return Response(
					{
						"success": True,
						"data" : subcatagory_conf_data_serializer,
	 					"message": "Sub-Catagory fetching successful!!"
					}
					)
		except Exception as e:
			print("Sub-Catagory listing configuration Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})


