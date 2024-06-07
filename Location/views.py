import re
import json
import os
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
from datetime import datetime
from django.db.models import Q
from django.db.models import Max
from Location.models import CountryMaster
from Configuration.models import *


class CountryList(APIView):
	"""
	Category Creation & Updation POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create & update product category within brand.

		Data Post: {
			"id"                   : "1"(Send this key in update record case,else it is not required!!)
			"category_name"		   : "Pizza",
			"category_code"		   : "123456",
			"company_auth_id" 	   : "3",
			"category_image"       : "a.jpg"
			"priority"             : "1"
			"description"		   : ""
		}

		Response: {

			"success": True, 
			"message": "Category Added Successfully!!",
			"data": final_result
		}

	"""
	def get(self, request, format=None):
		try:
			data = requests.get('https://restcountries.eu/rest/v2/all')	
			for i in data.json():
				name = i['name']
				alpha3Code = i['alpha3Code']
				callingCodes = i['callingCodes'][0]
				if len(i['currencies']) > 0:
					code = i['currencies'][0]['code']
					symbol = i['currencies'][0]['symbol']
					cur_data = CurrencyMaster.objects.filter(currency=code)
					if cur_data.count() > 0:
						currency_id = cur_data[0].id
					else:
						cur_data1 = CurrencyMaster.objects.create(currency=code,symbol=symbol)
						if cur_data1:
							currency_id = cur_data1.id
				country_data = CountryMaster.objects.filter(country=name)
				if country_data.count() > 0:
					country_data.update(currency_id=currency_id,iso=alpha3Code,isd=callingCodes)
				else:
					CountryMaster.objects.create(country=name,currency_id=currency_id,iso=alpha3Code,isd=callingCodes)
			return Response({
						"success": True, 
						})
		except Exception as e:
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})

