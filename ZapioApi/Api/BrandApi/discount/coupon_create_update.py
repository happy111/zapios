from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime, timedelta
from django.db.models import Q
import os
from django.db.models import Max
import dateutil.parser
#Serializer for api
from rest_framework import serializers
from Product.models import ProductCategory, Product
from discount.models import Coupon
from ZapioApi.Api.BrandApi.discount.Validation.coupon_error_check import *
from UserRole.models import *
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user

class CouponSerializer(serializers.ModelSerializer):
	class Meta:
		model = Coupon
		fields = '__all__'


class CouponCreationUpdation1(APIView):
	"""
	Coupon Creation & Updation POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create & update Coupon within brand.

		Data Post: {
			"id"                   : "1"(Send this key in update record case,else it is not required!!)
			"coupon_type"		   : "Flat",
			"coupon_code"		   : "BUZZ30",
			"frequency" 	       : "300",
			"valid_frm"            : "2019-07-24 00:00:00:00",
			"valid_till"           : "2019-07-29 00:00:00:00"
			"category"             : "2",
			"product_map"          : "[1,2]",
			"outlet_id"            : "[1,2]",
			"flat_discount"        : "150",
			"flat_percentage"      : "",
			"is_min_shop"          : "true",
			"is_automated"         : "true",
			"min_shoping"          : "200",
			"max_shoping"          : "350"
		}

		Response: {

			"success": True, 
			"message": "Coupon creation/updation api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			mutable = request.POST._mutable
			request.POST._mutable = True
			auth_id = request.user.id
			Company_id = get_user(auth_id)
			data['Company'] = Company_id
			data["category"] = str(data["category"])
			data["flat_percentage"] = str(data["flat_percentage"])
			data["flat_discount"] = str(data["flat_discount"])
			data["min_shoping"] = str(data["min_shoping"])
			data["max_shoping"] = str(data["max_shoping"])
			data["frequency"] = str(data["frequency"])
			validation_check = coupon_err_check(data)
			if validation_check != None:
				return Response(validation_check)
			valid_frm = dateutil.parser.parse(data["valid_frm"])
			valid_till = dateutil.parser.parse(data["valid_till"])
			data["valid_frm"] = valid_frm
			data["valid_till"] = valid_till
			if data["coupon_type"] == "Flat":
				data["flat_percentage"] = 0
				data["flat_discount"] = data["flat_discount"]
			else:
				data["flat_discount"] = 0
				data["flat_percentage"] = data["flat_percentage"]
			if "id" in data:
				record = Coupon.objects.filter(id=data['id'])
				if record.count() == 0:
					return Response(
					{
						"success": False,
	 					"message": "Coupon data is not valid to update!!"
					}
					)
				else:
					unique_check = \
					Coupon.objects.filter(~Q(id=data["id"]),\
									Q(coupon_code__iexact=data['coupon_code']),
									Q(Company=Company_id))
					if unique_check.count() == 0:
						data["updated_at"] = datetime.now()
						serializer = \
						CouponSerializer(record[0],data=data,partial=True)
						if serializer.is_valid():
							data_info = serializer.save()
							info_msg = "Coupon is updated sucessfully!!"
						else:
							print(str(serializer.errors))
							print("something went wrong!!")
							return Response({
								"success": False, 
								"message": str(serializer.errors),
								})
					else:
						err_message = {}
						err_message["unique_check"] = "Coupon with this code already exists!!"
						return Response({
									"success": False,
									"error" : err_message,
									"message" : "Please correct listed errors!!"
									})
			else:
				serializer = CouponSerializer(data=data)
				if serializer.is_valid():
					data_info = serializer.save()
					info_msg = "Coupon is created successfully!!"
				else:
					print(str(serializer.errors))
					print("something went wrong!!")
					return Response({
						"success": False, 
						"message": str(serializer.errors),
						})
			final_result = []
			final_result.append(serializer.data)
			return Response({
						"success": True, 
						"message": info_msg,
						"data": final_result,
						})
		except Exception as e:
			print("Coupon creation/updation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})
