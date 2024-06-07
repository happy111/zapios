import re
import json
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
from datetime import datetime
from django.db.models import Q
from Brands.models import Company
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user
from kitchen.models import RecipeIngredient
from Product.models import FoodType
from Configuration.models import Unit

class listPrimaryIngredient(APIView):

	"""
	 listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of primary ingredient data.

	"""

	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			user = request.user.id
			user = request.user.id
			status = request.GET.get('status')
			cid = get_user(user)
			if status == 'true':
				allunit = RecipeIngredient.objects.filter(company_id=cid,
									active_status=1).order_by('name')
			else:
				allunit = RecipeIngredient.objects.filter(company_id=cid).order_by('name')
			final_result = []
			if allunit.count() > 0:
				for i in allunit:
					allunit = {}
					allunit['name'] = i.name
					allunit['food_type'] = i.food_type.food_type
					if i.ingredient_type == 'primary':
						allunit['ingredient_type'] = 'Primary Ingredient'
					else:
						allunit['ingredient_type'] = 'Recipe Ingredient'
					if i.food_type_id != None:
						domain_name = addr_set()
						f = FoodType.objects.filter(id=i.food_type_id)
						if f.count() > 0:
							allunit["FoodType_name"] = f[0].food_type
							allunit["FoodType_image"] = domain_name + str(f[0].foodtype_image) 
					else:
						allunit["FoodType_image"] = ''
					allunit['id'] = i.id
					allunit['active_status'] = i.active_status
					domain_name = addr_set()
					if i.image != "" and i.image != None and i.image != "null":
						full_path = domain_name + str(i.image)
						allunit['image'] = full_path
					else:
						allunit['image'] = ''
					final_result.append(allunit)
				return Response({
						"success": True, 
						"data": final_result})
			else:
				return Response({
						"success": True, 
						"data": []})
		except Exception as e:
			print("Primary ingredient listing Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})



