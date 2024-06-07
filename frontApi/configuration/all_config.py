import re
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from Brands.models import Company
from _thread import start_new_thread
from datetime import datetime
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from Configuration.models import *
from discount.models import PercentOffers
from Product.models import ProductCategory
from ZapioApi.api_packages import *


class ConfigDataView(APIView):
	"""
	Configuration data listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for providing config data of brand.


		Data Post: {
  			"company"                          : "1"
		}

		Response: {

			"success"  : True, 
			"message"  : "Theme api worked well!!",
			"data"     : final_result
		}

	"""
	def post(self, request, format=None):
		try:
			data = request.data
			alldelivery = DeliverySetting.objects.filter(company=data['company'])
			if alldelivery.count() > 0:
				deliverycharge = alldelivery[0].delivery_charge
				packagecharge = alldelivery[0].package_charge
				tax = alldelivery[0].tax_percent
				CGST = alldelivery[0].CGST
			else:
				pass
			offerdata = PercentOffers.objects.filter(company=data['company'])
			offers = []
			if offerdata.count() > 0:
				for i in offerdata:
					offer = {}
					offer['category'] = i.category_id
					offer['categoryname'] = ProductCategory.objects.filter(id =i.category_id).first().category_name
					offer['discount'] = i.discount_percent
					offers.append(offer)
			else:
				pass
			return Response({"success": True,
						     "deliverycharge":deliverycharge,
						     "packagecharge":packagecharge,
						     "SGST" : tax,
						     "CGST" : CGST,
						     "offercategory":offer})
						    
		except Exception as e:
			print(e)
			return Response({"success": False,
							"message":"config api stucked into exception!!"})
