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
from Product.models import Menu
import base64



class listMenu(APIView):

	"""
	Order Source listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of Source data.

	"""


	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			user = request.user.id
			cid = get_user(user)
			allsource = Menu.objects.filter(company_id=cid,is_hide=0)
			final_result = []
			if allsource.count() > 0:
				for i in allsource:
					dict_source = {}
					dict_source['menu_name'] = i.menu_name
					dict_source['id'] = i.id
					dict_source['active_status'] = i.active_status
					#dict_source['img'] = base64.b64encode(i.menu_image.read()).decode('utf-8')
					dict_source['img'] = i.base_code
					im = str(i.menu_image)
					if im != "" and im != None and im != "null":
						domain_name = addr_set()
						full_path = domain_name + str(i.menu_image)
						dict_source['menu_image'] = full_path
					else:
						pass
					bc = str(i.barcode_pic)
					if bc != "" and bc != None and bc != "null":
						domain_name = addr_set()
						full_path = domain_name 
						dict_source['qr_code'] = full_path + str('barcode') +'/' + str(i.barcode_pic)
					else:
						dict_source['qr_code']  = ''
					final_result.append(dict_source)
				return Response({
						"success": True, 
						"data": final_result})
			else:
				return Response({
						"success": True, 
						"data": []})
		except Exception as e:
			print("Menu listing Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})

