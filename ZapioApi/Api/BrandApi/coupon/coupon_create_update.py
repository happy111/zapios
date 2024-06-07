import re
import json
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
from datetime import datetime, timedelta
from django.db.models import Q
from django.db.models import Max
import dateutil.parser
#Serializer for api
from rest_framework import serializers
from Product.models import ProductCategory, Product
from discount.models import Coupon,Discount
from ZapioApi.Api.BrandApi.coupon.Validation.coupon_error_check import *
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user


class CouponSerializer(serializers.ModelSerializer):
	class Meta:
		model = Discount
		fields = '__all__'


class CouponCreationUpdation(APIView):
	"""
	Coupon Creation & Updation POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create & update Coupon within brand.

		Data Post: {
			"id"                   : "1"(Send this key in update record case,else it is not required!!)
			"discount_type"		   : "Flat",
			"discount_name"		   : "awdawda"
			"user_roll"		       : "[1,2]"
 			"valid_frm"            : "2019-07-24 00:00:00:00",
			"valid_till"           : "2019-07-29 00:00:00:00"
			"category_map"         : "[1,2]",
			"product_map"          : "[1,2]",
			"outlet_id"            : "[1,2]",
			"flat_discount"        : "150",
			"flat_percentage"      : "",
			"is_min_shop"          : "true",
			"is_reason_required"   : "true",
			"min_shoping"          : "200",
			"max_shoping"          : "350",
			"is_all_category"      : "true",
			"is_all_product"       : "true"
			"is_banner"            : 1 or 0 
			"image"                :
		}

		Response: {

			"success": True, 
			"message": "Discount creation/updation api worked well!!",
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
			data["flat_percentage"] = str(data["flat_percentage"])
			data["flat_discount"] = str(data["flat_discount"])
			data["min_shoping"] = str(data["min_shoping"])
			data["max_shoping"] = str(data["max_shoping"])
			data["company_auth_id"] = request.user.id
			validation_check = coupon_err_check(data)
			if validation_check != None:
				return Response(validation_check)
			if type(data['valid_frm']) == str and data['valid_frm'] != '':
				valid_frm = dateutil.parser.parse(data["valid_frm"])
				data["valid_frm"] = valid_frm
			else:
				pass
			if type(data['valid_till']) == str and data['valid_till'] != '':
				valid_till = dateutil.parser.parse(data["valid_till"])
				data["valid_till"] = valid_till
			else:
				pass
			auth_id = request.user.id
			Company_id = get_user(auth_id)
			data["Company"] = Company_id
			if data["discount_type"] == "Flat":
				data["flat_percentage"] = 0
				data["flat_discount"] = data["flat_discount"]
			else:
				data["flat_discount"] = 0
				data["flat_percentage"] = data["flat_percentage"]
			if "id" in data:
				record = Discount.objects.filter(id=data['id'])
				if record.count() == 0:
					return Response(
					{
						"success": False,
	 					"message": "Coupon data is not valid to update!!"
					}
					)
				else:
					data["updated_at"] = datetime.now()
					if data["image"] == '':
						data["image"] = record[0].category_image
					else:
						pass
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

