from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime
from ZapioApi.Api.BrandApi.listing.listing import addr_set

#Serializer for api
from rest_framework import serializers
from Product.models import FoodType

class FoodTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = FoodType
		fields = '__all__'


class FoodTypeRetrieval(APIView):
	"""
	FoodType retrieval POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of FoodType data.

		Data Post: {
			"id"                   : "1"
		}

		Response: {

			"success": True, 
			"message": "FoodType retrieval api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			err_message = {}
			err_message["id"] = \
					validation_master_anything(data["id"],
					"FoodType Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = FoodType.objects.filter(id=data['id'])
			if record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Provided FoodType data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				q_dict = {}
				q_dict["id"] = record[0].id
				q_dict["food_type"] = record[0].food_type
				full_path = addr_set()
				q_dict["foodtype_image"] = record[0].foodtype_image
				if q_dict["foodtype_image"] != None and q_dict["foodtype_image"]!="":
					q_dict["foodtype_image"] = full_path+str(q_dict["foodtype_image"])
				else:
					q_dict["foodtype_image"] = None
				q_dict["active_status"] = record[0].active_status
				q_dict["created_at"] = record[0].created_at
				q_dict["updated_at"] = record[0].updated_at
				final_result.append(q_dict)
			return Response({
						"success": True, 
						"message": "FoodType retrieval api worked well!!",
						"data": final_result,
						})
		except Exception as e:
			print("FoodType retrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})