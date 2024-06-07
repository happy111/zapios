import os
import re
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
from datetime import datetime
from django.db.models import Q
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user
from rest_framework import serializers
from kitchen.models import *


class PrimaryIngredientCreationUpdation(APIView):

	"""
	Primary Ingredient Creation & Updation POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create & update Primary Ingredient.
		Data Post: {
			"id"                   : "1"(Send this key in update record case,else it is not required!!)
			"ingredient_type"      : 
			"name"                 :
			"food_type"            : "veg",
			"image"                : "",
			"primary_deatils"      : [],
			"output_yield"         : [],


		}

		Response: {

			"success": True, 
			"message": "Primary Ingredient creation/updation api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			user = request.user.id
			cid = get_user(user)
			data['company'] = cid
			err_message = {}
			datas = {}
			err_message["ingredient_type"] = only_required(data["ingredient_type"],"Ingredient Type")
			err_message["name"]      = only_required(data["name"],"Primary Ingredient")
			err_message["food_type"] = validation_master_anything(str(data["food_type"]),
				                       "Food Type",contact_re, 1)
			if type(data["image"]) != str:
				im_name_path =  data["image"].file.name
				im_size = os.stat(im_name_path).st_size
				if im_size > 100*1024:
					err_message["image_size"] = "Ingredient image can'nt excced the size more than 100kb!!"
			else:
				data["image"] = None
			parient_unique_list = []
			if data['ingredient_type'] == 'secondary':
				data2 = json.loads(data["primary_deatils"])
				data['primary_deatils'] = data2
				data3 = json.loads(data["output_yield"])
				data['output_yield'] = data3
				if len(data['output_yield']) > 0:
					for index in data['output_yield']:
						if 'unit' in index and 'value' in index:
							if index['value'] == '':
								err_message['value'] = "Please Enter a Output yield value"
							if 'value' in index and index['value'] != '':
								if index['unit'] == '':
									err_message['unit'] = "Please Enter a Output yield unit"
								else:
									pass
						if 'value' in index and index['value'] != '':
							if 'unit' not in index:
								err_message['Output yield Unit'] = "Please Enter a Output yield unit"
						if 'value' in index and index['value'] == '' and 'unit' not in index:
							data['output_yield'] = []

				if len(data2) != 0:
					for i in data2:
						if "unit" in i and  "unitValue" in i and "pingredient" in i:
							pass
						else:
							err_message["parient_detail"] = \
							"PrimaryIngredient,unit and unit value is not set!!"
							break	
						if i["pingredient"] not in parient_unique_list:
							parient_unique_list.append(i["pingredient"])
						else:
							err_message["duplicate_ingredient"] = "PrimaryIngredient are duplicate!!"
							break
						err_message["unit"] = validation_master_anything(i["unitValue"],"Primary Ingredient Unit",contact_re, 1)
				
						err_message["unit"] = 	only_required(i["unitValue"],"Unit Value")
						ch_v = i['unitValue'].find('.')
						if ch_v == 1:
							st = i['unitValue'].split('.')
							if len(st[1]) > 3:
								err_message["unit"] = 	"Only upto 3 decimal unit value allow!!"
						else:
							pass
				else:
					err_message["primary_detail"] = \
							"PrimaryIngredient,unit and unit value is not set!!"
			else:
				pass
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			if "id" in data:
				unique_check = RecipeIngredient.objects.filter(~Q(id=data["id"]),\
								Q(name=data["name"]),Q(company_id=cid),\
								Q(ingredient_type=data['ingredient_type']))
			else:
				unique_check = RecipeIngredient.objects.filter(Q(name=data["name"]),\
					Q(company_id=cid),Q(ingredient_type=data['ingredient_type']))
			if unique_check.count() != 0:
				err_message["unique_check"] = "Ingredient with this name already exists!!"
			else:
				pass
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			if "id" in data:
				primary_record = RecipeIngredient.objects.filter(id=data['id'])
				if primary_record.count() == 0:
					return Response(
					{
						"success": False,
	 					"message": "Ingredient data is not valid to update!!"
					}
					)
				else:
					if data["image"] == None:
						data["image"] = primary_record[0].image
					else:
						pass
					data["updated_at"] = datetime.now()
					if data['ingredient_type'] == 'primary':
						primary_serializer = primary_record.update(
							ingredient_type=data['ingredient_type'],
							food_type_id=data['food_type'],
							name=data['name'],
							updated_at=data['updated_at'])
						if data["image"] != None and data["image"] != "":
							pdata = RecipeIngredient.objects.get(id=data["id"])
							pdata.image = data["image"]
							pdata.save()
						else:
							pass
					else:
						primary_serializer = primary_record.update(
							ingredient_type=data['ingredient_type'],
							food_type_id=data['food_type'],
							name=data['name'],
							output_yield=data['output_yield'],
							primary_deatils=data['primary_deatils'],
							updated_at=data['updated_at'])
						if data["image"] != None and data["image"] != "":
							pdata = RecipeIngredient.objects.get(id=data["id"])
							pdata.image = data["image"]
							pdata.save()
						else:
							pass
					info_msg = "Recipe is updated successfully!!"
					return Response({
							"success": True, 
							"message": info_msg
					})
			else:
				if data['ingredient_type'] == 'primary':
					data['output_yield'] = []
					data['primary_deatils'] = []
					primary_serializer = RecipeIngredient.objects.create(
						ingredient_type=data['ingredient_type'],
						company_id=cid,
						name=data['name'],\
						food_type_id=data['food_type'],
						image=data['image'],
						active_status=1,
						output_yield=data['output_yield'],
						primary_deatils=data['primary_deatils'])
				else:
					primary_serializer = RecipeIngredient.objects.create(
						ingredient_type=data['ingredient_type'],
						company_id=cid,
						name=data['name'],\
						food_type_id=data['food_type'],
						image=data['image'],
						active_status=1,
						output_yield=data['output_yield'],
						primary_deatils=data['primary_deatils'],)
				info_msg = "Recipe is created successfully!!"
				return Response({
							"success": True, 
							"message": info_msg
							})
		except Exception as e:
			print("Recipe creation/updation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})