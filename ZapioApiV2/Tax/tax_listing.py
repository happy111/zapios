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
from Configuration.models import *



class listTax(APIView):

	"""
	Tax listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of Tax data.

	"""

	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			user = request.user.id
			user = request.user.id
			cid = get_user(user)
			data = request.data
			if data['status'] == True:
				alltax = TaxSetting.objects.\
						filter(company=cid,active_status=1).order_by('-created_at')
			else:
				alltax = TaxSetting.objects.\
						filter(company=cid,active_status=0).order_by('-created_at')
			final_result = []
			if alltax.count() > 0:
				for i in alltax:
					dict_tax = {}
					dict_tax['tax_name'] = i.tax_name
					dict_tax['tax_percent'] = i.tax_percent
					dict_tax['id'] = i.id
					dict_tax['active_status'] = i.active_status
					final_result.append(dict_tax)
				return Response({
						"success": True, 
						"data": final_result})
			else:
				return Response({
						"success": True, 
						"data": []})
		except Exception as e:
			print("Tax listing Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})