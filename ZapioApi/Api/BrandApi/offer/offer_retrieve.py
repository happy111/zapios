from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_201_CREATED, \
	HTTP_406_NOT_ACCEPTABLE, HTTP_200_OK, HTTP_503_SERVICE_UNAVAILABLE
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime

#Serializer for api
from rest_framework import serializers
from Product.models import ProductCategory
from discount.models import PercentOffers

class PercentOfferSerializer(serializers.ModelSerializer):
	class Meta:
		model = PercentOffers
		fields = '__all__'


class OfferRetrieve(APIView):
	"""
	Offer retrieval POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of offer product category data within brand.

		Data Post: {
			"id"                   : "3"
		}

		Response: {

			"success": True, 
			"message": "Offer Product Category retrieval api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			data["id"] = str(data["id"])
			err_message = {}
			err_message["id"] = \
					validation_master_anything(data["id"],
					"Category Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			category_record = PercentOffers.objects.filter(id=data['id'])
			if category_record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Required Percent Offer Category data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				q_dict = {}
				q_dict["id"] = category_record[0].id
				q_dict["category_name"] = category_record[0].category
				q_dict["discount_percent"] = category_record[0].discount_percent
				q_dict["active_status"] = category_record[0].active_status
				final_result.append(q_dict)
			return Response({
						"success": True, 
						"message": "Offer Product category retrieval api worked well!!",
						"data": final_result,
						})
		except Exception as e:
			print("Offer Product Category retrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})
