from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from Product.models import Product, Product_availability, Category_availability, ProductCategory
from ZapioApi.api_packages import *
from Outlet.models import OutletProfile
import re
from _thread import start_new_thread
from ZapioApi.Api.BrandApi.outletmgmt.availability.available import *



class PosLevelCategory(APIView):
	"""
	Category availability Post API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to make Category available or unavailable within pos.

		Data Post: {
			"is_available"  : "false",
			"id"            : "1",
			"outlet"        : "21"
		}

		Response: {

			"success": True, 
			"message": "Category is unavailable now!!",

		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			user = request.user
			cat_check = CategoryAvailable(data,user)
			print("dddddddddddddd",cat_check)

			if cat_check !=None:
				return Response(cat_check) 
			else:
				if data['is_available'] ==False:
					msg = "Category is already unavailable!!"
				else:
					msg = "Category is already available!!"
				return Response({
					"success" : False,
					"message" : msg
					})
		except Exception as e:
			print("Outletwise Category availability Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})