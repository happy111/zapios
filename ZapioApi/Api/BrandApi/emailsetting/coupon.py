from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
import json
from datetime import datetime
from django.db.models import Q
from rest_framework import serializers
from discount.models import PercentOffers
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user

from UserRole.models import * 

class CouponData(APIView):

	"""
	Coupon GETAPI

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for list coupon data.

	"""
	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			data = request.data
			auth_id = request.user.id
			Company_id = get_user(auth_id)
			record = PercentOffers.objects.filter(Q(company_id=Company_id),Q(category_id=None),Q(active_status=1))
			if record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Provided Ingredient data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				for i in record:
					food_dict = {}
					food_dict["label"] = i.offer_name
					food_dict["key"] = i.id
					food_dict["value"] = i.id
					final_result.append(food_dict)
			return Response({
						"success": True, 
						"message": "Coupon retrieval api worked well!!",
						"data": final_result,
						})
		except Exception as e:
			print("FoodType retrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})