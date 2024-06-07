from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import re
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from Brands.models import Company
from _thread import start_new_thread
from datetime import datetime
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
import json
from Configuration.models import *

from discount.models import PercentOffers
from Product.models import ProductCategory




class OfferList(APIView):
	"""
	List of Offer Product Category GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for list of Offer product category of brand.


		Data Post: {
  			
		}

		Response: {

			"success"  : True, 
			"message"  : "Theme api worked well!!",
			"data"     : final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			user =  request.user.id
			Company_id = Company.objects.filter(auth_user=user)[0].id
			odata = PercentOffers.objects.filter(company=Company_id)
			alldata = []
			if odata.count() > 0:
				for i in odata:
					offer = {}
					offer['category'] = i.category_id
					offer['categoryname'] = ProductCategory.objects.filter(id=i.category_id).first().category_name
					offer['discount'] = i.discount_percent
					alldata.append(offer)
				return Response({"success": True,
						     "offer":alldata})
			else:
				pass



		except Exception as e:
			print(e)
			return Response({"success": False,
							"message" : "config api stucked into exception!!"})
