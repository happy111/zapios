from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime

#Serializer for api
from rest_framework import serializers
from Product.models import ProductCategory

class ProductCategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductCategory
		fields = '__all__'




class CategoryRetrieval(APIView):
	"""
	Category retrieval POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of category data within brand.

		Data Post: {
			"id"                   : "3"
		}

		Response: {

			"success": True, 
			"message": "Category retrieval api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			data["id"] = str(data["id"])
			err_message = {}
			err_message["id"] = \
					validation_master_anything(data["id"],
					"Category Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			category_record = ProductCategory.objects.filter(id=data['id'])
			if category_record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Required Category data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				q_dict = {}
				q_dict["id"] = category_record[0].id
				q_dict["category_name"] = category_record[0].category_name
				q_dict["category_code"] = category_record[0].category_code
				q_dict["description"] = category_record[0].description
				q_dict["priority"] = category_record[0].priority
				q_dict["active_status"] = category_record[0].active_status
				domain_name = addr_set()
				cat_img = str(category_record[0].category_image)
				if cat_img != "" and cat_img != None and cat_img != "null":
					full_path = domain_name + str(cat_img)
					q_dict['category_image'] = full_path
				else:
					q_dict['category_image'] = ''
				final_result.append(q_dict)
			return Response({
						"success": True, 
						"message": "Category retrieval api worked well!!",
						"data": final_result,
						})
		except Exception as e:
			print("Category retrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})
