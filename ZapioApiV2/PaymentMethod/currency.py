from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *

from rest_framework import serializers
from Location.models import CountryMaster
from Configuration.models import CurrencyMaster
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user
from django.db.models import Q




class GetCurrency(APIView):
	"""
	CountryWise currency listing Configuration POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to provide currency maped with Country.

		Data Post: {

			"id" 	    : "1"
		}

		Response: {

			"success": True,
			"data" :  serializer,
			"message": "Countrywuse country listing api worked well!!"
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			err_message = {}
			err_message["id"] = \
					validation_master_anything(data["id"],
					"Country ID",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			query = CountryMaster.objects.filter(id=data["id"],active_status=1)
			if query.count()==0:
				return Response(
					{
						"success": False,
	 					"message": "Country id is not valid!!"
					}
					) 
			else:
				serializer = []
				q_dict = {}
				q_dict["id"] = query[0].id
				q_dict["currency"] = query[0].currency.currency
				serializer.append(q_dict)
			return Response(
					{
						"success": True,
						"data" : serializer,
	 					"message": "CountryWise currency listing api worked well!!"
					}
					)
		except Exception as e:
			print("CountryWise currency listing api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})