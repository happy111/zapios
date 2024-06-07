from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_201_CREATED, \
	HTTP_406_NOT_ACCEPTABLE, HTTP_200_OK, HTTP_503_SERVICE_UNAVAILABLE
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime
from rest_framework import serializers
from Configuration.models import PaymentDetails


class PaymentConfig(APIView):
	
	"""
	Percent Combo retrieval POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used for payment Configuration.

		Data Post: {
			"company"                   : "1"
		}

		Response: {
			    "success": true,
			    "keyid": "rzp_live_xcgVtA1lIkJ",
			    "keySecret": "dgwbqAGqDcFXNRBYkXaP",
			    "symbol": "INR",
			    "brand_name" :  "InstaPizza"
		}

	"""
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			err_message = {}
			err_message["company"] = \
					validation_master_anything(data["company"],
					"Company Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = PaymentDetails.objects.filter(company=data['company'])
			if record.count() > 0:
				return Response({
							"success"   : True, 
							"keyid" 	: record[0].keyid,
							"keySecret"	: record[0].keySecret,
							"symbol"    : record[0].symbol,
							"brand_name" : record[0].company.company_name
 							})
			else:
				return Response({
							"success": False, 
							"message": "No Data Found"
							})
		except Exception as e:
			print("Payment Configuration retrieval Api Stucked into exception!!")
			print(e)
			return Response({
							"success": False, 
							"message": "Error happened!!", 
							"errors": str(e)})