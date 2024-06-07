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
from Configuration.models import Unit



class StatusUnit(APIView):

	"""
	Unit Listing POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to provide unit Listing.

		Data Post: {

			"status"   ; "true"
		}

		Response: {

		}

	"""


	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			user = request.user.id
			cid = get_user(user)
			data = request.data
			if data['status'] == True:
				query = Unit.objects.\
						filter(company_id=cid,active_status=1).order_by('-created_at')
			else:
				query = Unit.objects.\
						filter(company_id=cid,active_status=0).order_by('-created_at')
			final_result = []
			if query.count() > 0:
				for i in query:
					allunit = {}
					allunit['unit_name'] = i.unit_name
					allunit['short_name'] = i.short_name
					allunit['id'] = i.id
					allunit['active_status'] = i.active_status
					allunit['unit_details'] = []
					if i.unit_details != None:
						if len(i.unit_details) > 0:
							for index in i.unit_details:
								dic = {}
								if 'unit' in index:
									u = Unit.objects.filter(id=index['unit'])
									if u.count() > 0:
										dic['unit'] = u[0].unit_name
									else:
										dic['unit'] = ''
								if 'units' in index:
									us = Unit.objects.filter(id=index['units'])
									if us.count() > 0:
										dic['units'] = us[0].unit_name
									else:
										dic['units'] = ''
								if 'unitValue' in index:
									dic['unitValue'] = index['unitValue']
								if 'unitValues' in index:
									dic['unitValues'] = index['unitValues']
								allunit['unit_details'].append(dic)
					else:
						pass
					final_result.append(allunit)
				return Response({
						"success": True, 
						"data": final_result})
			else:
				return Response({
						"success": True, 
						"data": []})
		except Exception as e:
			print("Unit listing Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})