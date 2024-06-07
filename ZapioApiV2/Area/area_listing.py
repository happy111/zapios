import re,json,os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
from datetime import datetime
from django.db.models import Q
from Brands.models import Company
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user
from Location.models import CityMaster,AreaMaster
from django.db import transaction
from django.utils.translation import gettext_lazy


class listLocality(APIView):

	"""
	Locality listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of City data.

	"""


	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			user = request.user.id
			user = request.user.id
			cid = get_user(user)
			allcity = AreaMaster.objects.filter(company_id=cid)
			final_result = []
			if allcity.count() > 0:
				for i in allcity:
					dict_source = {}
					dict_source['area'] = i.area
					dict_source['city'] = CityMaster.objects.filter(id=i.city_id)[0].city
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
			print("Locality listing Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})