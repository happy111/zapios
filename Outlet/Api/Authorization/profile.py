import re,os,json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_201_CREATED, \
	HTTP_406_NOT_ACCEPTABLE, HTTP_200_OK, HTTP_503_SERVICE_UNAVAILABLE
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
from datetime import datetime
from django.db.models import Max
from Outlet.models import OutletProfile
from Location.models import *
#Serializer for api
from rest_framework import serializers
from Product.models import FoodType, Product, ProductCategory, ProductsubCategory,\
AddonDetails

def addr_set():
	domain_name = "http://virtualkitchen.eoraa.com/media/"
	return domain_name



class OutletRetrieve(APIView):
	"""
	Outlet retrieval POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of profile data for outlet.

		Data Post: {
			
		}

		Response: {

			"success": True, 
			"message": "Order data retrieval api worked well!!",
			"data": final_result
		}

	"""

	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			user = request.user.id
			order_record = OutletProfile.objects.filter(auth_user=user)
			if order_record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Required Order data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				p_list = {}
				p_list["id"] = order_record[0].id
				p_list["username"] = order_record[0].username
				p_list["Outletname"] = order_record[0].Outletname
				p_list["mobile_with_isd"] = order_record[0].mobile_with_isd
				p_list["email"] = order_record[0].email
				p_list["password"] = order_record[0].password
				p_list["address"] = order_record[0].address
				p_list["city"] = order_record[0].city
				p_list["prefecture"] = order_record[0].prefecture
				p_list["opening_time"] = order_record[0].opening_time
				p_list["closing_time"] = order_record[0].closing_time
				p_list['profile_pic'] = str(order_record[0].om_pic)
				p_list["ip_address"] = order_record[0].ip_address
				domain_name = addr_set()
				if order_record[0].om_pic != "" and order_record[0].om_pic != None:
					full_path = domain_name + str(order_record[0].om_pic)
					p_list['om_pic'] = full_path
		
				final_result.append(p_list)
			return Response({
						"success": True, 
						"message": "Outlet data retrieval api worked well!!",
						"data": final_result,
						})
		except Exception as e:
			print("Outlet data retrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})
