import json
import re
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
from datetime import datetime

#Serializer for api
from rest_framework import serializers
from kitchen.models import RecipeIngredient
from Configuration.models import Unit

	
class RetrievePrimaryIngredient(APIView):

	"""
	Primary Ingredient POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used for retrieval of  primary Ingredient data.

		Data Post: {
			"id"                   : "1"
		}

		Response: {

			"success": True, 
			"message": "Primary ingredient retrieval api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			err_message = {}
			err_message["id"] = \
					validation_master_anything(data["id"],"Recipe Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = RecipeIngredient.objects.filter(id=data['id'])
			if record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Provided Primary Ingredient data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				q_dict = {}
				q_dict["id"] = record[0].id
				q_dict["name"] = record[0].name
				q_dict["ingredient_type"] = []
				i_dict = {}
				if record[0].ingredient_type == 'primary':
					i_dict["label"] = "Primary Ingredient"
					i_dict["value"] = record[0].ingredient_type
				else:
					i_dict["label"] = "Secondary Ingredient"
					i_dict["value"] = record[0].ingredient_type
				q_dict["ingredient_type"].append(i_dict)
				q_dict["foodtype_detail"] = []
				food_dict = {}
				food_dict["label"] = record[0].food_type.food_type
				food_dict["key"] = record[0].food_type_id
				food_dict["value"] = record[0].food_type_id
				q_dict["foodtype_detail"].append(food_dict)
				q_dict['output'] = record[0].output_yield
				q_dict['pin']  = record[0].primary_deatils
				va = q_dict['output']
				if va != None:
					for v in va:
						if 'unit' in v:
							pin = v['unit']
							u =  Unit.objects.filter(id=pin)
							if u.count() > 0:
								pname = u[0]
								v['unit'] = {}
								v['unit']["label"] = pname.unit_name
								v['unit']["value"] = pin
					q_dict['output'] = va
				va = q_dict['pin']
				if va != None:
					for v in va:
						if 'pingredient' in v:
							pin = v['pingredient']
							p = RecipeIngredient.objects.filter(id=pin)
							if p.count() > 0:
								pname = p[0]
								v['primaryIng'] = {}
								v['primaryIng']["label"] = pname.name
								v['primaryIng']["key"] = pin
								v['primaryIng']["value"] = pin
						if 'unit' in v:
							pin = v['unit']
							u =  Unit.objects.filter(id=pin)
							if u.count() > 0:
								pname = u[0]
								v['unit'] = {}
								v['unit']["label"] = pname.unit_name
								v['unit']["key"] = pin
								v['unit']["value"] = pin
						del v["pingredient"]
					q_dict['pin'] = va
				full_path = addr_set()
				q_dict["image"] = record[0].image
				if q_dict["image"] != None and q_dict["image"]!="":
					q_dict["image"] = full_path+str(q_dict["image"])
				else:
					q_dict["image"] = None
				q_dict["active_status"] = record[0].active_status
				q_dict["created_at"] = record[0].created_at
				q_dict["updated_at"] = record[0].updated_at
				
				print("ssssssssssss",q_dict)

				final_result.append(q_dict)
			return Response({
						"success": True, 
						"message": "Primary Ingredient retrieval api worked well!!",
						"data": final_result,
						})
		except Exception as e:
			print("Primary Ingredient retrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})