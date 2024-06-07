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



class GoogleAnalytics(APIView):
	"""
	Google analytics data for post API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for providing google analytics data of brand.


		Data Post: {
  			"company"                          : "1"
		}

		Response: {

			"success"   : True, 
			"data" 		: offers,
			"message" 	: "Google analytics api worked well!!"
		}

	"""
	def post(self, request, format=None):
		try:
			data = request.data
			offerdata = AnalyticsSetting.objects.filter(company=data['company'])
			offers = []
			if offerdata.count() > 0:
				for i in offerdata:
					offer = {}
					offer['u_id'] = i.u_id
					offer['analytics_snippets'] =i.analytics_snippets
					offers.append(offer)
				return Response({"success"	: True,
							"data" 			: offers,
							"message" 		: "Google analytics api worked well!!"
							})
			else:
				return Response({"success": False,
							"data" : "No Data Found"
							})
		except Exception as e:
			print(e)
			return Response({"success": False,
							"message":"config api stucked into exception!!"})
