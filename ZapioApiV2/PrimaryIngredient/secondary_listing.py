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
from colorama import init
from colorama import Fore,Style
from Configuration.models import Unit
from kitchen.models import RecipeIngredient


class listSecondaryIngredients(APIView):

	"""
	 listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of secondary ingredient data.

	"""

	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			user = request.user.id
			user = request.user.id
			cid = get_user(user)
			allunit = RecipeIngredient.objects.filter(company_id=cid,active_status=1).order_by('name')
			final_result = []
			if allunit.count() > 0:
				for i in allunit:
					if i.ingredient_type == "primary":
						allunit = {}
						allunit['name'] = i.name
						allunit['id'] = i.id
						allunit['active_status'] = i.active_status
						allunit['color'] = "blue"
					else:
						allunit = {}
						allunit['name'] = i.name
						allunit['id'] = i.id
						allunit['active_status'] = i.active_status
						allunit['color'] = "green"
					final_result.append(allunit)
				return Response({
						"success": True, 
						"data": final_result})
			else:
				return Response({
						"success": True, 
						"data": []})
		except Exception as e:
			print("Secondary ingredient sss listing Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})