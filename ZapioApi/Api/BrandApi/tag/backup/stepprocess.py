from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
import json
from datetime import datetime
from rest_framework_tracking.mixins import LoggingMixin
import os
from django.db.models import Max
from ZapioApi.Api.BrandApi.kitchen.process_error_check import *
from Brands.models import Company

#Serializer for api
from rest_framework import serializers
from Product.models import FoodType, Product, ProductCategory, ProductsubCategory,\
	AddonDetails,Variant
from kitchen.models import Ingredient,StepToprocess

class StepprocessCreateUpdate(APIView):

	"""
	Stepprocess Creation & Updation POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create & update Stepprocess.

		Data Post: {
			"id"                           : "1"(Send this key in update record case,else it is not required!!)
			"product"		               : "3",
			"varient"                      : "1",
			"step"       	       		   : "1",
			"process"                      : "www",
			"description"                  : "sadsadsa",
			"time_of_process"              : "20",
			"image"                        : "pizza.jpg",
 			"ingrediate"                   : [
				{
					"name"           : "Large",
					"unit"           : "gms",
					"id"             : "1",
					"quantitiy"      : "4"
			    }],
		}

		Response: {

			"success": True, 
			"message": "Step process creation/updation api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			data["company_auth_id"] = request.user.id
			data2 = json.loads(data["ingrediate"])
			data['ingrediate'] = data2
			validation_check = err_check(data)
			if validation_check != None:
				return Response(validation_check) 
			unique_check = unique_record_check(data,data["company_auth_id"])
			if unique_check != None:
				return Response(unique_check)
			pro_query = Product.objects.filter(id=data["product"])
			Company_id = Company.objects.filter(auth_user=data["company_auth_id"])[0].id
			if pro_query.count() != 0:
				pass
			else:
				return Response(
					{
						"success": False,
						"message": "Product is not valid!!"
					}
					)
			if data["varient"] != "":
				sucat_query = Variant.objects.filter(id=data["varient"])
				if sucat_query.count() != 0:
					pass
				else:
					return Response(
						{
							"success": False,
							"message": "Varient id is not valid to update!!"
						}
						)
			else:
				pass
			data["active_status"] = 1
			if "id" in data:
				record = StepToprocess.objects.filter(id=data['id'])
				if record.count() == 0:
					return Response(
					{
						"success": False,
						"message": "Product process data is not valid to update!!"
					}
					)
				else:
					data["updated_at"] = datetime.now()
					update_data = \
					record.update(company_id=Company_id,\
					product_id=data["product"],varient_id=data["varient"],\
					step=int(data["step"]),process=data["process"],description=data["description"],\
					time_of_process=int(data["time_of_process"]),\
					ingredient=data["ingrediate"],\
					active_status=data["active_status"],\
					updated_at=datetime.now())
					if data["image"] != None and data["image"] != "":
						product = StepToprocess.objects.get(id=data["id"])
						product.image = data["image"]
						product.save()
					else:
						pass
					if update_data:
						info_msg = "Product process is updated successfully!!"
					else:
						return Response({
							"success": False, 
							"message": str(serializer.errors),
							})
			else:
				p_query = \
					StepToprocess.objects.create(company_id=Company_id,\
					product_id=data["product"],varient_id=data["varient"],\
					step=int(data["step"]),process=data["process"],description=data["description"],\
					time_of_process=int(data["time_of_process"]),image=data["image"],\
					ingredient=data["ingrediate"],\
					active_status=data["active_status"],created_at=datetime.now(),\
					)
				if p_query:
					data_info=p_query
					info_msg = "Product process is created successfully!!"
				else:
					print("something went wrong!!")
					return Response({
						"success": False, 
						"message": str(serializer.errors),
						})
			return Response({
						"success": True, 
						"message": info_msg
						})
		except Exception as e:
			print("Step process creation/updation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})