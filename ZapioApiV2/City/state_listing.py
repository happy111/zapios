import re
import json
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
from datetime import datetime
from django.db.models import Q
from Brands.models import Company
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user
from Location.models import CityMaster,StateMaster



class listState(APIView):

	"""
	All state  POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to listing state via country.
		Data Post: {
			"country_id"		               : 1,
		}

		Response: {

			"success"		: True, 
			"message"       : "Listing state api worked well!!",
			"data"          : final_result
		}

	"""

	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			user = request.user.id
			cid = get_user(user)
			data = request.data
			try:
				allstate = StateMaster.objects.filter(country_id=data['country_id'])
				final_result = []
				if allstate.count() > 0:
					for i in allstate:
						dict_source = {}
						dict_source['state'] = i.state
						dict_source['id'] = i.id
						dict_source['active_status'] = i.active_status
						final_result.append(dict_source)
					return Response({
							"success": True, 
							"data": final_result})
				else:
					return Response({
							"success": True, 
							"data": []})
			except:
				return Response({
							"success": True, 
							"data": []})
		except Exception as e:
			print("State listing Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})