import re
import json
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
from datetime import datetime
from django.db.models import Q
from Configuration.models import BusinessType



class listBusiness(APIView):

	"""
	All business type  Get API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to listing of business type.
		Data Post: {

		}

		Response: {

			"success"		: True, 
			"message"       : "Listing business type api worked well!!",
			"data"          : final_result
		}

	"""

	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			alldata = BusinessType.objects.filter(active_status=1)
			final_result = []
			if alldata.count() > 0:
				for i in alldata:
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
		except Exception as e:
			print("State listing Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})