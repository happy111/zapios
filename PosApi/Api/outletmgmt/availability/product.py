from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from Product.models import Product, Product_availability, Category_availability, ProductCategory
from ZapioApi.api_packages import *
import re
from ZapioApi.Api.BrandApi.outletmgmt.availability.available import *
from rest_framework_tracking.mixins import LoggingMixin


class PosLevelProductavail(LoggingMixin,APIView):
	"""
	Product availability Post API

		Authentication Required		: Yes
		
		Service Usage & Description	: This Api is used to make products available or unavailable within pos.

		Data Post: {
			"is_available"  : False,
			"id"            : "1",
			"outlet"        : "21",
			"is_aggregator" : "1"
		}

		Response: {

			"success": True, 
			"message": "Product is unavailable now!!",

		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			user = request.user
			try:
				data["is_aggregator"] = int(data["is_aggregator"])
			except Exception as e:
				return Response({
					"success" : False,
					"message" : "Is Aggregator value is not valid!!"
					})

			# Functionality for urbanpiper implemented here
			if data["is_aggregator"] == 1:
				item_action_data = {}
				item_action_data["id"] = data["id"]
				item_action_data["availability"] = data["is_available"]
				item_action_data["outlet"] = data["outlet"]
				urban = ItemAction(item_action_data)
				if urban == False:
					return Response({
						"success" : False,
						"message" : "Item toggling is not performed well!!"
						})
				else:
					if data["is_available"] == False:
						return Response({
							"success" : True,
							"message" : "Item is disbled at Aggregator!!"
							})
					else:
						return Response({
							"success" : True,
							"message" : "Item is enabled at Aggregator!!"
							})
				# functionality ends here
			else:
				product_check = ProductAvailable(data,user)
				if product_check != None:
					return Response(product_check) 
				else:
					if data['is_available'] == False:
						msg = "Product is already unavailable!!"
					else:
						msg = "Product is already available!!"
					return Response({
						"success" : False,
						"message" : msg
						})
		except Exception as e:
			print("Outletwise Product availability Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})