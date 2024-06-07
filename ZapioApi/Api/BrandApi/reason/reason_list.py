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
from discount.models import DiscountReason
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user





class ReasonList(APIView):

	"""
	Discount Reason listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of Tag data.
	"""


	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			user = request.user.id
			cid = get_user(user)
			allreason = DiscountReason.objects.filter(Company_id=cid)
			final_result = []
			if allreason.count() > 0:
				for i in allreason:
					allrea = {}
					allrea['reason'] = i.reason
					allrea['id'] = i.id
					allrea['active_status'] = i.active_status
					final_result.append(allrea)
				return Response({
						"success": True, 
						"data": final_result})
			else:
				return Response({
						"success": True, 
						"data": []})
		except Exception as e:
			print("Discount Reason listing Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})