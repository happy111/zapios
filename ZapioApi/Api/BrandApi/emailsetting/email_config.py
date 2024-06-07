from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime
from rest_framework import serializers
from Configuration.models import EmailSetting
from discount.models import PercentOffers
from UserRole.models import ManagerProfile
from Brands.models import Company
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user


def addr_set():
	domain_name = "https://zapio-admin.com/media/"
	return domain_name



class EmailConfig(APIView):
	
	"""
	Email Config GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for Email Config details.

	"""
	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			from Brands.models import Company
			auth_id = request.user.id
			Company_id = get_user(auth_id)
			record = EmailSetting.objects.filter(company=Company_id)
			data = []
			if record.count() > 0:
				data_dict = {}
				domain_name = addr_set()
				if record[0].image != "" and record[0].image != None:
					full_path = domain_name + str(record[0].image)
				else:
					full_path =''
				data_dict['title']  = record[0].title
				data_dict['content']  = record[0].content
				data_dict['id']  = record[0].id
				data_dict['dis_content']  = record[0].dis_content
				data_dict['active_status']  = record[0].active_status
				data_dict['subcontent']  = record[0].thank
				data_dict['image']  = full_path
				data_dict["coupon"] = []
				food_dict = {}
				if record[0].coupon_id !=None:
					food_dict["label"] = PercentOffers.objects.filter(id=record[0].coupon_id)[0].offer_name
					food_dict["key"] =   record[0].coupon_id
					food_dict["value"] = record[0].coupon_id
					data_dict["coupon"].append(food_dict)
				else:
					pass
				data.append(data_dict)
				return Response({
							"success"               : True, 
							"data"					: data
 							})
			else:
				err_message = {}
				err_message["settings"] = "Please contact to super-admin to set parameters for this!!"
				return Response({
							"success": False, 
							"error" :  err_message
							})
		except Exception as e:
			print("Email retrieval Api Stucked into exception!!")
			print(e)
			return Response({
							"success": False, 
							"message": "Error happened!!", 
							"errors": str(e)})