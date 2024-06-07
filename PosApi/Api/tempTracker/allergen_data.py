import re
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
from Outlet.models import TempTracking, OutletProfile
from UserRole.models import ManagerProfile
from datetime import datetime, timedelta
from .latest_temp import secret_token 
from Brands.models import Company
from Product.models import FoodType,Tag

class AllergenInformation(APIView):
	"""
	Allergen Information data get API

		Authentication Required		 	: 		Yes
		Service Usage & Description	 	: 		This Api is used to provide Allergen data.

		Data Get: {
		}

		Response: {

			"success"	: 	True,
			"data"		:	result, 

		}

	"""
	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			final_result = []
			di = {}
			di['allergen'] = []
			dic = {}
			dic['label'] = "ビーガン"
			dic['value'] = "Vegan"
			di['allergen'].append(dic)
			dic1 = {}
			dic1['label'] = "グルテンフリー"
			dic1['value'] = "Gluten-Free"
			di['allergen'].append(dic1)
			dic2 = {}
			dic2['label'] = "卵フリー"
			dic2['value'] = "Eggs Free"
			di['allergen'].append(dic2)
			dic3 = {}
			dic3['label'] = "ラクトースフリー"
			dic3['value'] = "Lactose-Free"
			di['allergen'].append(dic3)
			dic4 = {}
			dic4['label'] = "ナッツフリー"
			dic4['value'] = "Nuts Free"
			di['allergen'].append(dic4)
			dic5 = {}
			dic5['label'] = "貝類"
			dic5['value'] = "Contains Shellfish"
			di['allergen'].append(dic5)
			dic6 = {}
			dic6['label'] = "小麦フリー"
			dic6['value'] = "Wheat-Free"
			di['allergen'].append(dic6)
			dic7 = {}
			dic7['label'] = "大豆フリー"
			dic7['value'] = "Soy Free"
			di['allergen'].append(dic7)
			di['spice'] = []
			dic9 = {}
			dic9['label'] = "あっさり"
			dic9['value'] = "Plain"
			di['spice'].append(dic9)
			dic10 = {}
			dic10['label'] = "マイルド"
			dic10['value'] = "Mild"
			di['spice'].append(dic10)
			dic11 = {}
			dic11['label'] = "ミディアム"
			dic11['value'] = "Medium"
			di['spice'].append(dic11)
			dic12 = {}
			dic12['label'] = "辛い"
			dic12['value'] = "Spicy"
			di['spice'].append(dic12)
			dic13 = {}
			dic13['label'] = "とても辛い"
			dic13['value'] = "Very Spicy"
			di['spice'].append(dic13)
			dic14 = {}
			dic14['label'] = "なし"
			dic14['value'] = "None"
			di['spice'].append(dic14)
			fdata = FoodType.objects.filter(active_status=1)
			di['food_type'] = []
			for index in fdata:
				dt = {}
				dt['id'] = index.id
				dt['food_type'] = index.food_type
				di['food_type'].append(dt)
			di['tag'] = []
			tagdata = Tag.objects.filter(active_status=1)
			if tagdata.count() > 0:
				for k in tagdata:
					temp = {}
					temp['id'] = k.id
					temp['tag_name'] = k.tag_name
					di['tag'].append(temp)
			

			final_result.append(di)
			return Response({
				"success"	: 	True, 
				"data"	: 	final_result
				})
		except Exception as e:
			return Response({
				"success"	: 	False, 
				"message"	: 	"Error happened!!", 
				"errors"	: 	str(e)
				})



			



