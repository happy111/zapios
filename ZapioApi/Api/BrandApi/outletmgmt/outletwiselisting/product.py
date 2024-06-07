from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from Product.models import Product, Product_availability
from Outlet.models import OutletProfile
from Brands.models import Company
import re
import os
from ZapioApi.api_packages import *
from ZapioApi.Api.BrandApi.outletmgmt.outletwiselisting.available import *
from UserRole.models import ManagerProfile



class OutletProductlist(APIView):
	"""
	Product listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to retrieve listing of Products associated with outlet.

		Data Post: {
			
			"outlet"     : "1"
		}

		Response: {

			"success" : True,
			"message" : "Outletwise product listing worked well!!",
			"data"    : final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			user = request.user
			pro_check = ProductAvailableList(data,user)
			if pro_check !=None:
				return Response(pro_check) 
			else:
				return Response ({
           					 "success":True,
							 "message":"No Data Found!!",
							 "data":[]
						})
		except Exception as e:
			print("Outletwise product listing Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})