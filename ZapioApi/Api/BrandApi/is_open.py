from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime
import os
from django.db.models import Max

from rest_framework import serializers
from Product.models import ProductCategory
from Brands.models import Company
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user

class BrandMgmtSerializer(serializers.ModelSerializer):
	class Meta:
		model = Company
		fields = '__all__'

class BrandOpen(APIView):
	"""
	Brand Is Open POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to close or open Brand.

		Data Post: {
			"is_open"             		: "false"
		}

		Response: {

			"success": True, 
			"message": "Outlet is closed now!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			from django.db.models import Q
			data = request.data
			user = request.user.id
			cid = get_user(user)
			err_message = {}
			if data["is_open"] == "true":
				pass
			elif data["is_open"] == "false":
				pass
			else:
				err_message["is_open"] = "Is Open data is not valid!!"
			record = Company.objects.filter(id=cid)
			if record.count() != 0:
				data["updated_at"] = datetime.now()
				if data["is_open"] == "true":
					info_msg = "Brand is open now!!"
				else:
					info_msg = "Brand is closed now!!"
				serializer = \
				BrandMgmtSerializer(record[0],data=data,partial=True)

				if serializer.is_valid():
					data_info = serializer.save()
				else:
					print("something went wrong!!")
					return Response({
						"success": False, 
						"message": str(serializer.errors),
						})
			else:
				return Response(
					{
						"success": False,
						"message": "Brand id is not valid to update!!"
					}
					)
			final_result = []
			final_result.append(serializer.data)
			return Response({
						"success": True, 
						"message": info_msg,
						# "data": final_result,
						})
		except Exception as e:
			print("Brand Is Open Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})