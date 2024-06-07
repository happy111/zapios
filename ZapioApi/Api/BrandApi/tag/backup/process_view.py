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
from kitchen.models import StepToprocess
from Product.models import Product,Variant


def addr_set():
	domain_name = "https://zapio-admin.com/media/"
	return domain_name

class ProductCategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductCategory
		fields = '__all__'


class StepprocessView(APIView):

	"""
	Stepprocess retrieval POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for view of Product Step Process data within brand.

		Data Post: {
			"p_id"                   : "21",
			"v_id"                   : "43"
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
			data = request.data
			data["p_id"] = str(data["p_id"])
			data["v_id"] = str(data["v_id"])
			err_message = {}
			err_message["p_id"] = \
					validation_master_anything(data["id"],
					"Product Id",contact_re, 1)
			if data['v_id'] != "None":
				err_message["v_id"] = \
						validation_master_anything(data["v_id"],
						"Variant Id",contact_re, 1)
			else:
				pass
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			process_data = StepToprocess.objects.filter(product=data['p_id'])
			if data['v_id'] == 'None':
				pass
			else:
				process_data = process_data.filter(varient=data['v_id'])
			if process_data.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Required Process data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				if process_data.count() > 0:
					for i in process_data:
						q_dict = {}
						q_dict["id"] = i.id
						q_dict["processName"] = i.process
						q_dict["time_of_process"] = i.time_of_process
						q_dict["active_status"] = i.active_status
						q_dict["description"] = i.description
						q_dict["image"] = str(i.image)
						domain_name = addr_set()
						if q_dict["image"]  != "" and q_dict["image"]  != None and q_dict["image"]  != "null":
							full_path = domain_name + str(i.image)
							q_dict['image'] = full_path
						else:
							q_dict['image'] =''
						q_dict["product"] = Product.objects.filter(id=i.product_id).first().product_name
						if data['v_id'] == 'None':
							q_dict["variant"] = None
						else:
							q_dict["variant"] = \
							Variant.objects.filter(id=i.varient_id).first().variant
						q_dict["step"] = i.step
						q_dict["ingredient"] = []
						va = i.ingredient
						if va != None:
							for v in va:
								v_addon_dict = {}
								v_addon_dict["value"] = v['name']
								v_addon_dict["key"] = v['quantity']
								v_addon_dict["unit"] = v['unit']
								q_dict["ingredient"].append(v_addon_dict)
						final_result.append(q_dict)
				else:
					pass
			return Response({
						"success": True, 
						"message": "All Product Steps retrieval api worked well!!",
						"data": final_result
						})

		except Exception as e:
			print("Process retrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, 
							"message": "Error happened!!", 
							"errors": str(e)})
