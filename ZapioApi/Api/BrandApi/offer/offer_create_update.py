from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime
from django.db.models import Q
import os
from django.db.models import Max
from ZapioApi.Api.BrandApi.Validation.category_error_check import *

#Serializer for api
from rest_framework import serializers
from Product.models import ProductCategory
from Brands.models import Company
from discount.models import PercentOffers
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user

class PercentOfferSerializer(serializers.ModelSerializer):
	class Meta:
		model = PercentOffers
		fields = '__all__'


class OfferProduct(APIView):

	"""
	Offer Product Wise POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create & update offer product within brand.

		Data Post: {
			"id"                       : "1"(Send this key in update record case,else it is not required!!)
			"category"		           : "Pizza",
			"discount_percent"		   : "123456",
		}

		Response: {

			"success": True, 
			"message": "Category Added Successfully!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			auth_id = request.user.id
			Company_id = get_user(auth_id)
			data['company'] = Company_id
			err_message = {}
			err_message["discount_percent"] = \
				validation_master_anything(str(data["discount_percent"]),
				"Discount Percentage",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			if "id" in data:
				category_record = PercentOffers.objects.filter(id=data['id'])
				if category_record.count() == 0:
					return Response(
					{
						"success": False,
	 					"message": "Category data is not valid to update!!"
					}
					)
				else:
					data["updated_at"] = datetime.now()
					offer_serializer = \
					PercentOfferSerializer(category_record[0],data=data,partial=True)
					if offer_serializer.is_valid():
						data_info = offer_serializer.save()
					else:
						print("something went wrong!!")
						return Response({
							"success": False, 
							"message": str(offer_serializer.errors),
							})
			else:
				offer_serializer = PercentOfferSerializer(data=data)
				if offer_serializer.is_valid():
					data_info = offer_serializer.save()
				else:
					print("something went wrong!!")
					return Response({
						"success": False, 
						"message": str(offer_serializer.errors),
						})
			final_result = []
			final_result.append(offer_serializer.data)
			return Response({
						"success": True, 
						"message": "Offer discount creation/updation api worked well!!",
						"data": final_result,
						})
		except Exception as e:
			print("Offer discount creation/updation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})

