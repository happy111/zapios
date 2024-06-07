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

class CitySave(APIView):

	"""
	City Creation & Updation POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create & update City
		Data Post: {
			"id"                       : "1"(Send this key in update record case,else it is not required!!)
			"city"		               : "New Delhi",
		}

		Response: {

			"success": True, 
			"message": "City creation/updation api worked well!!",
			"data": final_result
		}

	"""
	#permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			import numpy as np
			import pandas as pd
			df = pd.read_excel(r"/home/umesh/Downloads/Delivery Locations Total.xlsx")
			s = df.shape
			for i in range(s[0]):
				if df['City'][i] == 'Delhi':
					data = AreaMaster.objects.create(area=df['Locality'][i],city_id=8,company_id=11)
				else:
					pass
				if df['City'][i] == 'Faridabad':
					data = AreaMaster.objects.create(area=df['Locality'][i],city_id=9,company_id=11)
				else:
					pass
				if df['City'][i] == 'Ghaziabad':
					data = AreaMaster.objects.create(area=df['Locality'][i],city_id=10,company_id=11)
				else:
					pass
				if df['City'][i] == 'Greater Noida':
					data = AreaMaster.objects.create(area=df['Locality'][i],city_id=11,company_id=11)
				else:
					pass
				if df['City'][i] == 'Noida':
					data = AreaMaster.objects.create(area=df['Locality'][i],city_id=12,company_id=11)
				else:
					pass
				if df['City'][i] == 'Gurugram':
					data = AreaMaster.objects.create(area=df['Locality'][i],city_id=1,company_id=11)
				else:
					pass
			return Response({
						"success": True, 
						"message": df
						})
		except Exception as e:
			print("City creation/updation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})