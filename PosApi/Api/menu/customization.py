from rest_framework.views import APIView
from rest_framework.response import Response
from Product.models import ProductCategory, Product_availability, Category_availability, Product,\
Variant,AddonDetails
from Outlet.models import OutletProfile
from Brands.models import Company
import re
from django.conf import settings
from ZapioApi.api_packages import *
from datetime import datetime
from django.db.models import Q
import random
from zapio.settings import Media_Path
from frontApi.menu.customize_fun import CustomizeProduct
from rest_framework.permissions import IsAuthenticated


class CustomeMgmt(APIView):
	"""
	Product Customization POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used to get all information reagrding product
		customization.

		Data Post: {

			"p_id" : 25
		}

		Response: {

			"success": True,
			"credential" : True,
			"customize_data" : InstaCustomize_serializer
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			menu_check = CustomizeProduct(data)
			if menu_check !=None:
				return Response(menu_check) 
			else:
				pass
		except Exception as e:
			print("Customize Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})