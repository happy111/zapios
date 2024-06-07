from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_201_CREATED, \
	HTTP_406_NOT_ACCEPTABLE, HTTP_200_OK, HTTP_503_SERVICE_UNAVAILABLE
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime

#Serializer for api
from rest_framework import serializers
from Product.models import Product
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user

class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = '__all__'


class ProductListFilter(APIView):
	"""
	Active Product retrieval POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of all active product data within 
		category if category id is provided else this service lists out all active products..

		Data Post: {
			"cat_id"                   : "3"(Optional Key)
		}

		Response: {

			"success": True, 
			"message": "Active product data retrieval api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			auth_id = request.user.id
			cid = get_user(auth_id)

			if "cat_id" in data and data["cat_id"] != "":
				data["cat_id"] = str(data["cat_id"])
				err_message = {}
				err_message["cat_id"] = \
						validation_master_anything(data["cat_id"],
						"Category Id",contact_re, 1)
				if any(err_message.values())==True:
					return Response({
						"success": False,
						"error" : err_message,
						"message" : "Please correct listed errors!!"
						})
			else:
				pass
			record = Product.objects.filter(active_status=1,Company_id=cid)
			if "cat_id" in data and data["cat_id"] != "":
				record = record.filter(product_categorys__exact=[str(data['cat_id'])])
			else:
				pass
			if record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Required Active product data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				for q in record:
					q_dict = {}
					q_dict["id"] =  q.id
					# q_dict["cat_id"] = q.product_category_id
					q_dict["product_name"] = q.product_name
					# q_dict["product_with_cat"] = \
					# str(q.product_name)+" | "+str(q.product_category.category_name) 
					final_result.append(q_dict)
			return Response({
						"success": True, 
						"message": "Active product data retrieval api worked well!!",
						"data": final_result,
						})
		except Exception as e:
			print("Active product data retrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})
