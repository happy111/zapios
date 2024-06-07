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
from Product.models import ProductCategory,Product, Variant
from kitchen.models import StepToprocess
from zapio.settings import Media_Path


class ProductWiseVariant(APIView):
	"""
	Product Wise Variant listing POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of variants with product.

		Data Post: {
			"p_id"                   : "3"
		}

		Response: {

			"success": True, 
			"message": "Product Wise Variant listing api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			data["id"] = str(data["p_id"])
			err_message = {}
			err_message["id"] = \
					validation_master_anything(data["id"],
					"Product Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			auth = request.user.id
			record = \
			Product.objects.filter(id=data["id"],active_status=1)
			if record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Required Product Wise Variant listing data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				q = record[0] 
				v_details = q.variant_deatils
				for v in v_details:
					v_dict = {}
					query = \
					Variant.objects.filter(Company__auth_user=auth,variant__iexact=v['name'],\
											active_status=1)
					if query.count()==0:
						pass
					else:
						v_dict["v_id"] = query[0].id
						v_dict["name"] = v["name"]
					final_result.append(v_dict)
			return Response({
						"success": True, 
						"message": "Product Wise Variant listing api worked well!!",
						"data": final_result,
						})
		except Exception as e:
			print("Product Wise Variant listing Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})
