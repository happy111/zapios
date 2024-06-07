from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime
from rest_framework import serializers
from Configuration.models import (DeliverySetting,
									PaymentDetails,
									ColorSetting,
									AnalyticsSetting)
from UserRole.models import ManagerProfile
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user


class DeliveryConfig(APIView):
	
	"""
	Delivery & Packaging Config GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for delivery & Packaging charge Configuration details.

	"""
	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			from Brands.models import Company
			user = self.request.user.id
			auth_id = user
			Company_id = get_user(auth_id)
			record = DeliverySetting.objects.filter(company=Company_id)
			Final_result = []
			if record.count() > 0:
				price_type  = record[0].price_type
				q_dict = {}
				q_dict['price_type'] = []
				if price_type != None:
					i_dict={}
					i_dict["value"] = price_type
					i_dict["key"] = price_type
					i_dict["label"] = price_type
					q_dict["price_type"].append(i_dict)
				else:
					pass
				q_dict['is_tax'] = record[0].is_tax
				q_dict['delivery_charge'] = record[0].delivery_charge
				q_dict['package_charge'] = record[0].package_charge
				q_dict['delivery_id'] = record[0].id
				q_dict['delivery_status'] = record[0].active_status
				q_dict['tax'] = []
				ps = record[0].tax
				if ps !=None:
					for v in ps:
						pname = Tax.objects.filter(id=str(v))[0]
						dic =  {}
						dic["label"] = str(pname.tax_name)+" | "+str(pname.tax_percent)+"%" 
						dic["value"] = str(v)
						q_dict['tax'].append(dic)
				else:
					pass
			else:
				err_message = {}
				err_message["settings"] = "Please contact to super-admin to set parameters for this!!"
				return Response({
							"success": False, 
							"error" :  err_message
							})
			record = PaymentDetails.objects.filter(company=Company_id)
			if record.count() > 0:
				q_dict['payment_id'] = record[0].id
				q_dict['keyid'] = record[0].keyid
				q_dict['keySecret'] = record[0].keySecret
				q_dict['symbol'] = record[0].symbol
				q_dict['payment_status'] = record[0].active_status
			else:
				pass
			record = ColorSetting.objects.filter(company=Company_id)
			if record.count() > 0:
				q_dict['theme_id'] = record[0].id
				q_dict['accent_color'] = record[0].accent_color
				q_dict['textColor'] = record[0].textColor
				q_dict['secondaryColor'] = record[0].secondaryColor
				q_dict['theme_status'] = record[0].active_status
			else:
				pass
			record = AnalyticsSetting.objects.filter(company=Company_id)
			if record.count() > 0:
				q_dict['google_id'] = record[0].id
				q_dict['u_id'] = record[0].u_id
				q_dict['analytics_snippets'] = record[0].analytics_snippets
				q_dict['google_status'] = record[0].active_status
			else:
				pass
			Final_result.append(q_dict)
			return Response({
						"success"   : True, 
						"data"      : Final_result
							})
		except Exception as e:
			print("Delivery Charge Configuration retrieval Api Stucked into exception!!")
			print(e)
			return Response({
							"success": False, 
							"message": "Error happened!!", 
							"errors": str(e)})