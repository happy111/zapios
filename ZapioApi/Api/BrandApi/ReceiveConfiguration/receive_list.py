from rest_framework.views import APIView
from rest_framework.response import Response
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime
import os
from django.db.models import Q
from Brands.models import Company
from UserRole.models import ManagerProfile
from Configuration.models import HeaderFooter
from Outlet.models import *
from UserRole.models import ManagerProfile
from Configuration.models import HeaderFooter




class ReceiveList(APIView):

	"""
	Receipt Configuration listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of Receipt Configuration data.
	"""


	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		user = self.request.user.id
		auth_id = request.user.id
		user = request.user.id
		is_outlet = OutletProfile.objects.filter(auth_user_id=user)
		is_brand = Company.objects.filter(auth_user_id=user)
		is_cashier = ManagerProfile.objects.filter(auth_user_id=user)
		if is_cashier.count() > 0:
			cid = ManagerProfile.objects.filter(auth_user_id=user)[0].Company_id
		else:
			pass
		if is_outlet.count() > 0:
			outlet = OutletProfile.objects.filter(auth_user_id=user)
			cid = outlet[0].Company_id
		else:
			pass
		if is_brand.count() > 0:
			outlet = Company.objects.filter(auth_user_id=user)
			cid = outlet[0].id
		else:
			pass
		config_data = HeaderFooter.objects.filter(company_id=cid).order_by('id')
		if config_data.count() > 0:
			pro_data =[]
			for i in config_data:
				p_list ={}
				p_list['id'] = i.id
				p_list['header'] = i.header_text
				p_list['footer'] = i.footer_text
				p_list['gst'] = i.gst
				p_list['active_status'] = i.active_status
				pro_data.append(p_list)
			return Response({"status":True,
							"data":pro_data})
		else:
			return Response({"status":True,
							"data":[]})



