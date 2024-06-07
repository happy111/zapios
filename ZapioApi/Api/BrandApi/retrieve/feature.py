from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime
from ZapioApi.Api.BrandApi.listing.listing import addr_set
#Serializer for api
from rest_framework import serializers
from Product.models import Product, AddonDetails, Tag, FeatureProduct



class FeatureRetrieval(APIView):
	"""
	Features Product retrieval POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of Feature products data.

		Data Post: {
			"id"                   : "60"
		}

		Response: {

			"success": True, 
			"message": "Feature Product retrieval api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			err_message = {}
			err_message["id"] = \
					validation_master_anything(str(data["id"]),
					"Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = FeatureProduct.objects.filter(id=data['id'])
			if record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Provided Feature Product data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				q_dict = {}
				q_dict["id"] = record[0].id
				q_dict["outlet_detail"] = []
				outlet_dict = {}
				outlet_dict["label"] = record[0].outlet.Outletname
				outlet_dict["key"] = record[0].outlet_id
				outlet_dict["value"] = record[0].outlet_id
				q_dict["outlet_detail"].append(outlet_dict)
				feature_detail  = record[0].feature_product
				q_dict["feature_detail"] = []
				if feature_detail != None:
					for i in feature_detail:
						q = Product.objects.filter(id=i)
						feature_dict = {}
						feature_dict["value"] = q[0].id
						feature_dict["key"] = q[0].id
						feature_dict["label"] = q[0].product_name
						q_dict["feature_detail"].append(feature_dict)
				else:
					pass
				final_result.append(q_dict)
			if final_result:
				return Response({
							"success": True, 
							"message": "Feature Product retrieval api worked well!!",
							"data": final_result,
							})
			else:
				return Response({
							"success": True, 
							"message": "No product data found!!"
							})
		except Exception as e:
			print("Feature Product retrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})
