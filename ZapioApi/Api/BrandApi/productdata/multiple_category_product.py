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
from Product.models import Product

from ZapioApi.Api.BrandApi.productdata.category_error_check import *


class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = '__all__'


class MultipleCategoryFilter(APIView):
	"""
	Active Product retrieval POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of all active product data within 
		category if category id is provided else this service lists out all active products..

		Data Post: {
			"cat_id"                   : "[1,2]"(Optional Key)
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
			data = request.data
			validation_check = err_check(data)
			if validation_check != None:
				return Response(validation_check)
			if len(data["cat_id"]) > 0: 
				main_routes = data["cat_id"]
				final_result = []
				for i in main_routes:
					q = Product.objects.filter(active_status=1,product_categorys__exact=[str(i)])
					if q.count() != 0:
						for j in q:
							record_dict = {}
							record_dict['id'] = j.id
							record_dict['product'] = j.product_name
							final_result.append(record_dict)
					else:
						pass
			else:
				final_result = []
				q = Product.objects.filter(active_status=1)
				if q.count() != 0:
					for j in q:
						record_dict = {}
						record_dict['id'] = j.id
						record_dict['product'] = j.product_name
						final_result.append(record_dict)
				else:
					pass
			return Response({
					"success": True, 
					"data": final_result})
		except Exception as e:
			print("Route listing Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})