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
from django.db.models import Sum,Count
#Serializer for api
from rest_framework import serializers
from Product.models import ProductCategory
from kitchen.models import StepToprocess
from Product.models import Product,Variant


def addr_set():
	domain_name = "https://zapio-admin.com/media/"
	return domain_name

class ProductCategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductCategory
		fields = '__all__'


class StepprocessRetrieve(APIView):

	"""
	Stepprocess retrieval POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for view of Product Step Process data within brand.

		Data Post: {
			"id"                   : "3"
		}

		Response: {

			"success": True, 
			"message": "Process retrieval api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
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
			process_record = StepToprocess.objects.filter(id=data['id'])
			if process_record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Required Process data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				q_dict = {}
				q_dict["id"] = process_record[0].id
				q_dict["processName"] = process_record[0].process
				q_dict["time_of_process"] = process_record[0].time_of_process
				q_dict["description"] = process_record[0].description
				q_dict["product"] = process_record[0].product_id
				q_dict["step"] = process_record[0].step
				a = str(process_record[0].image)
				domain_name = addr_set()
				if a != "" and a!= None and a!= "null":
					full_path = domain_name + str(process_record[0].image)
					q_dict['image'] = full_path
				else:
					q_dict['image'] =''
				q_dict["pro_detail"] = []
				pro_dict = {}
				pro_dict["label"] = process_record[0].product.product_name
				pro_dict["key"] = process_record[0].product_id
				pro_dict["value"] = process_record[0].product_id
				q_dict["pro_detail"].append(pro_dict)
				q_dict["var_detail"] = []
				v_dict = {}
				if process_record[0].varient != None:
					v_dict["label"] = process_record[0].varient.variant
					v_dict["key"] = process_record[0].varient_id
					v_dict["value"] = process_record[0].varient_id
				else:
					v_dict["label"] = ""
					v_dict["key"] = ""
					v_dict["value"] = ""
				q_dict["var_detail"].append(v_dict)
				q_dict["ingredient_detail"] = process_record[0].ingredient
				if v_dict["key"] == "":
					total_q = \
					StepToprocess.objects.filter(product=q_dict["product"])
				else:
					total_q = \
					StepToprocess.objects.filter(product=q_dict["product"],varient=v_dict["key"])
				total_time = total_q.aggregate(Sum('time_of_process'))
				total_step = total_q.aggregate(Count('id'))
				q_dict["total_time"] = total_time['time_of_process__sum']
				q_dict["total_steps"] = total_step['id__count']
				va = q_dict["ingredient_detail"] 
				if va != None:
					for v in va:
						if "name" in v:
							v["ingredients"] = {}
							v["ingredients"]["value"] = v['id']
							v["ingredients"]["label"] = v["name"]
							v["ingredients"]["key"] = v["id"]
							# v["dis"] = v["discount_price"]
						else:
							pass
					q_dict["ingredient_detail"] = va
				else:
					pass

				final_result.append(q_dict)
			return Response({
						"success": True, 
						"message": "Process retrieval api worked well!!",
						"data": final_result,
						})

		except Exception as e:
			print("Process retrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, 
							"message": "Error happened!!", 
							"errors": str(e)})
