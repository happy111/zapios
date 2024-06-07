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
from Location.models import CityMaster,AreaMaster

class CitySerializer(serializers.ModelSerializer):
	class Meta:
		model = CityMaster
		fields = '__all__'

class CityLocality(APIView):

	"""
	Locality Creation & Updation POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to listing locallity against by city
		Data Post: {
			"city"		               : [1,2],
		}

		Response: {

			"success": True, 
			"message": "Listing city api worked well!!",
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
			Final_result = []
			if len(data['city']) > 0:
				for index in data['city']:
					areadata = AreaMaster.objects.filter(city_id=index)
					if areadata.count() > 0:
						for k in areadata:
							dic = {}
							dic['id'] = k.id
							dic['area'] = k.area
							Final_result.append(dic)
					else:
						pass
			else:
				pass
			return Response({
						"success": True, 
						"message": Final_result
						})
		except Exception as e:
			print("locallity Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})