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
from discount.models import Coupon, QuantityCombo, PercentCombo
from ZapioApi.Api.BrandApi.discount.Validation.combo_error_check import *
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user


class QuantityComboSerializer(serializers.ModelSerializer):
	class Meta:
		model = QuantityCombo
		fields = '__all__'

class PercentComboSerializer(serializers.ModelSerializer):
	class Meta:
		model = PercentCombo
		fields = '__all__'


class QuantityComboCreationUpdation(APIView):
	"""
	Quantity Combo Creation & Updation POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create & update Quantity based Combo within brand.

		Data Post: {
			"id"                   : "1"(Send this key in update record case,else it is not required!!)
			"product"		       : "1",
			"free_product"		   : "2",
			"product_quantity" 	   : "1",
			"free_pro_quantity"    : "2",
			"valid_frm"            : "2019-07-24 00:00:00:00",
			"valid_till"           : "2019-07-29 00:00:00:00"
		}

		Response: {

			"success": True, 
			"message": "Quantity Combo creation/updation api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			auth_id = request.user.id
			Company_id = get_user(auth_id)
			mutable = request.POST._mutable
			request.POST._mutable = True
			data["product"] = str(data["product"])
			data["free_product"] = str(data["free_product"])
			data["product_quantity"] = str(data["product_quantity"])
			data["free_pro_quantity"] = str(data["free_pro_quantity"])
			data["company"] = Company_id
			validation_check = quantity_err_check(data)
			if validation_check != None:
				return Response(validation_check)
			valid_frm = dateutil.parser.parse(data["valid_frm"])
			valid_till = dateutil.parser.parse(data["valid_till"])
			data["Company"] = Company_id
			p_query = Product.objects.filter(id=data["product"])
			free_p_query = Product.objects.filter(id=data["free_product"])
			combo_product = p_query[0].product_name
			free_product = free_p_query[0].product_name
			data["combo_name"] = \
			"Buy "+data["product_quantity"]+" "+combo_product+" Get "\
								+data["free_pro_quantity"]+" "+free_product
			data["valid_frm"] = valid_frm
			data["valid_till"] = valid_till
			data["product_quantity"] = int(data["product_quantity"])
			data["free_pro_quantity"] = int(data["free_pro_quantity"])
			if "id" not in data:
				unique_check = \
					QuantityCombo.objects.filter(Q(combo_name__iexact=data['combo_name']),
									Q(Company=Company_id),\
									Q(product=data['product']),\
									Q(free_product=data['free_product']),\
									Q(product_quantity=data['product_quantity']),\
									Q(free_pro_quantity=data['free_pro_quantity']))
				if unique_check.count() == 0:
					pass
				else:
					err_message = {}
					err_message["unique_check"] = \
					"Quantity based Combo with this name and product mapping already exists!!"
					return Response({
								"success": False,
								"error" : err_message,
								"message" : "Please correct listed errors!!"
								})
			else:
				pass
			if "id" in data:
				record = QuantityCombo.objects.filter(id=data['id'])
				if record.count() == 0:
					return Response(
					{
						"success": False,
	 					"message": "Quantity Combo data is not valid to update!!"
					}
					)
				else:
					unique_check = \
					QuantityCombo.objects.filter(~Q(id=data["id"]),\
									Q(combo_name__iexact=data['combo_name']),
									Q(Company=Company_id),\
									Q(product=data['product']),\
									Q(free_product=data['free_product']),\
									Q(product_quantity=data['product_quantity']),\
									Q(free_pro_quantity=data['free_pro_quantity']))
					if unique_check.count() == 0:
						data["updated_at"] = datetime.now()
						serializer = \
						QuantityComboSerializer(record[0],data=data,partial=True)
						if serializer.is_valid():
							data_info = serializer.save()
							info_msg = "Combo is updated sucessfully!!"
						else:
							print("something went wrong!!")
							return Response({
								"success": False, 
								"message": str(serializer.errors),
								})
					else:
						err_message = {}
						err_message["unique_check"] = \
						"Quantity based Combo with this name and product mapping already exists!!"
						return Response({
									"success": False,
									"error" : err_message,
									"message" : "Please correct listed errors!!"
									})
			else:
				serializer = QuantityComboSerializer(data=data)
				if serializer.is_valid():
					data_info = serializer.save()
					info_msg = "Combo is created successfully!!"
				else:
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
			print("Quantity Combo creation/updation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})



class PercentComboCreationUpdation(APIView):
	"""
	Percent Combo Creation & Updation POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create & update Percent based Combo within brand.

		Data Post: {
			"id"                   : "1"(Send this key in update record case,else it is not required!!)
			"product"		       : "1",
			"discount_product"	   : "2",
			"discount_percent" 	   : "10",
			"valid_frm"            : "2019-07-24 00:00:00:00",
			"valid_till"           : "2019-07-29 00:00:00:00"
		}

		Response: {

			"success": True, 
			"message": "Percent Combo creation/updation api worked well!!",
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
			data["company"] = Company_id
			data["product"] = str(data["product"])
			data["discount_product"] = str(data["discount_product"])
			data["discount_percent"] = str(data["discount_percent"])
			validation_check = percentage_err_check(data)
			if validation_check != None:
				return Response(validation_check)
			valid_frm = dateutil.parser.parse(data["valid_frm"])
			valid_till = dateutil.parser.parse(data["valid_till"])
			data["Company"] = Company_id
			p_query = Product.objects.filter(id=data["product"])
			discount_p_query = Product.objects.filter(id=data["discount_product"])
			combo_product = p_query[0].product_name
			discount_product = discount_p_query[0].product_name
			data["pcombo_name"] = \
			"Buy "+combo_product+" and Get "\
								+data["discount_percent"]+"%"+" off on "+discount_product
			data["valid_frm"] = valid_frm
			data["valid_till"] = valid_till
			data["discount_percent"] = int(data["discount_percent"])
			if "id" not in data:
				unique_check = \
					PercentCombo.objects.filter(Q(pcombo_name__iexact=data['pcombo_name']),
									Q(Company=Company_id),\
									Q(product=data['product']),\
									Q(discount_product=data['discount_product']),\
									Q(discount_percent=data['discount_percent']))
				if unique_check.count() == 0:
					pass
				else:
					err_message = {}
					err_message["unique_check"] = \
					"Percentage based Combo with this name and product mapping already exists!!"
					return Response({
								"success": False,
								"error" : err_message,
								"message" : "Please correct listed errors!!"
								})
			else:
				pass
			if "id" in data:
				record = PercentCombo.objects.filter(id=data['id'])
				if record.count() == 0:
					return Response(
					{
						"success": False,
	 					"message": "Quantity Combo data is not valid to update!!"
					}
					)
				else:
					unique_check = \
					PercentCombo.objects.filter(~Q(id=data["id"]),\
									Q(pcombo_name__iexact=data['pcombo_name']),
									Q(Company=Company_id),
									Q(product=data['product']),\
									Q(discount_product=data['discount_product']),\
									Q(discount_percent=data['discount_percent']))
					if unique_check.count() == 0:
						data["updated_at"] = datetime.now()
						serializer = \
						PercentComboSerializer(record[0],data=data,partial=True)
						if serializer.is_valid():
							data_info = serializer.save()
							info_msg = "Combo is updated sucessfully!!"
						else:
							print("something went wrong!!")
							return Response({
								"success": False, 
								"message": str(serializer.errors),
								})
					else:
						err_message = {}
						err_message["unique_check"] = \
						"Quantity based Combo with this name and product mapping already exists!!"
						return Response({
									"success": False,
									"error" : err_message,
									"message" : "Please correct listed errors!!"
									})
			else:
				serializer = PercentComboSerializer(data=data)
				if serializer.is_valid():
					data_info = serializer.save()
					info_msg = "Combo is created successfully!!"
				else:
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
			print("Percentage Combo creation/updation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})