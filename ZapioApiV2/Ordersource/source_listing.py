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
from Configuration.models import OrderSource



class listSource(APIView):

	"""
	Order Source listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of Source data.

	"""


	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			user = request.user.id
			user = request.user.id
			cid = get_user(user)
			allsource = OrderSource.objects.filter(company_id=cid).order_by('priority')
			final_result = []
			if allsource.count() > 0:
				for i in allsource:
					dict_source = {}
					dict_source['source_name'] = i.source_name
					dict_source['id'] = i.id
					dict_source['active_status'] = i.active_status
					dict_source['is_edit'] = i.is_edit
					im = str(i.image)
					if im != "" and im != None and im != "null":
						domain_name = addr_set()
						full_path = domain_name + str(i.image)
						dict_source['image'] = full_path
					else:
						pass
					final_result.append(dict_source)
				return Response({
						"success": True, 
						"data": final_result})
			else:
				return Response({
						"success": True, 
						"data": []})
		except Exception as e:
			print("Source listing Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})