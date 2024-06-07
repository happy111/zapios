import re,json,os,dateutil.parser
from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
from datetime import datetime, timedelta
from django.db.models import Q
from django.db.models import Max
from rest_framework import serializers
from Product.models import ProductCategory, Product
from ZapioApi.Api.BrandApi.discount.Validation.coupon_error_check import *
from UserRole.models import *
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user
from rest_framework.generics import ListAPIView
from .serializers import *
from discount.models import *
from ZapioApi.Api.BrandApi.coupon.Validation.coupon_error_check import *
from ZapioApi.Api.BrandApi.discount.Validation.combo_error_check import *

from django.db import transaction
from django.http import Http404
from django.utils.translation import gettext_lazy



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
			data1    =     json.loads(data["category_map"])
			data['category_map'] = data1
			data2    =     json.loads(data["product_map"])
			data['product_map'] = data2
			data3    =     json.loads(data["outlet_id"])
			data['outlet_id'] = data3
			data4    =     json.loads(data["user_roll"])
			data['user_roll'] = data4
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
					coupon_data = record.update(\
						discount_name=data['discount_name'],
						discount_type=data['discount_type'],\
						user_roll=data['user_roll'],\
						valid_frm=data["valid_frm"],
						valid_till=data['valid_till'],\
						Company_id=data['Company'],\
						category_map=data['category_map'],\
						product_map=data['product_map'],\
						flat_discount=data['flat_discount'],\
						flat_percentage=data['flat_percentage'],\
						outlet_id=data['outlet_id'],\
						is_min_shop=data['is_min_shop'],\
						is_reason_required=data['is_reason_required'],\
						min_shoping=data['min_shoping'],\
						max_shoping=data['max_shoping'],\
						is_all_category=data['is_all_category'],\
						is_all_product=data['is_all_product'],\
						is_banner=data['is_banner'],\
						updated_at=data['updated_at']
						)
					if 'image' in data:
						if data["image"] != None and data["image"] != " ":
							discount = Discount.objects.get(id=data["id"])
							discount.image = data["image"]
							discount.save()
					if coupon_data:
						info_msg = gettext_lazy("Discount is updated successfully!!")
			else:
				coupon_data = Discount.objects.create(\
					discount_name=data['discount_name'],
					discount_type=data['discount_type'],\
					user_roll=data['user_roll'],\
					valid_frm=data["valid_frm"],
					valid_till=data['valid_till'],\
					Company_id=data['Company'],\
					category_map=data['category_map'],\
					product_map=data['product_map'],\
					flat_discount=data['flat_discount'],\
					flat_percentage=data['flat_percentage'],\
					outlet_id=data['outlet_id'],\
					is_min_shop=data['is_min_shop'],\
					is_reason_required=data['is_reason_required'],\
					min_shoping=data['min_shoping'],\
					max_shoping=data['max_shoping'],\
					is_all_category=data['is_all_category'],\
					is_all_product=data['is_all_product'],\
					is_banner=data['is_banner'],\
					image=data['image'])
				if coupon_data:
					info_msg = "Discount is created successfully!!"
			return Response({
						"success": True, 
						"message": gettext_lazy(info_msg),
						})
		except Exception as e:
			print("Coupon creation/updation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})


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
			"max_shoping"          : "350",
			"is_banner"            : 1 or 0 
			"image"                :
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
			data2    =     json.loads(data["product_map"])
			data['product_map'] = data2
			data3    =     json.loads(data["outlet_id"])
			data['outlet_id'] = data3
			validation_check = discount_err_check(data)
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
	 					"message": gettext_lazy("Coupon data is not valid to update!!")
					}
					)
				else:
					unique_check = \
					Coupon.objects.filter(~Q(id=data["id"]),\
									Q(coupon_code__iexact=data['coupon_code']),
									Q(Company=Company_id))
					if unique_check.count() == 0:
						data["updated_at"] = datetime.now()
						coupon_data = record.update(coupon_type=data['coupon_type'],
							coupon_code=data['coupon_code'],frequency=data['frequency'],
							valid_frm=data["valid_frm"],valid_till=data['valid_till'],\
							category_id=data['category'],\
							Company_id=data['Company'],\
							product_map=data['product_map'],\
							flat_discount=data['flat_discount'],\
							outlet_id=data['outlet_id'],\
							is_min_shop=data['is_min_shop'],\
							is_automated=data['is_automated'],\
							min_shoping=data['min_shoping'],\
							max_shoping=data['max_shoping'],\
							is_banner=data['is_banner'],\
							updated_at=data['updated_at']
							)
						if 'image' in data:
							if data["image"] != None and data["image"] != " ":
								discount = Coupon.objects.get(id=data["id"])
								discount.image = data["image"]
								discount.save()
						if coupon_data:
							info_msg = gettext_lazy("Coupon is updated sucessfully!!")
					else:
						err_message = {}
						err_message["unique_check"] = gettext_lazy("Coupon with this code already exists!!")
						return Response({
									"success": False,
									"error" : err_message,
									"message" : "Please correct listed errors!!"
									})
			else:
				coupon_data = Coupon.objects.create(\
				coupon_type=data['coupon_type'],\
				coupon_code=data['coupon_code'],\
				frequency=data['frequency'],\
				valid_frm=data["valid_frm"],\
				valid_till=data['valid_till'],\
				category_id=data['category'],\
				Company_id=data['Company'],\
				product_map=data['product_map'],\
				flat_discount=data['flat_discount'],\
				flat_percentage=data['flat_percentage'],\
				outlet_id=data['outlet_id'],\
				is_min_shop=data['is_min_shop'],\
				is_automated=data['is_automated'],\
				min_shoping=data['min_shoping'],\
				max_shoping=data['max_shoping'],\
				is_banner=data['is_banner'],\
				image=data['image'])
				if coupon_data:
					info_msg = gettext_lazy("Coupon is created successfully!!")
			return Response({
						"success": True, 
						"message": info_msg,
						})
		except Exception as e:
			print("Coupon creation/updation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})





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
	 					"message":gettext_lazy("Quantity Combo data is not valid to update!!")
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
							info_msg = gettext_lazy("Combo is updated sucessfully!!")
						else:
							print("something went wrong!!")
							return Response({
								"success": False, 
								"message": str(serializer.errors),
								})
					else:
						err_message = {}
						err_message["unique_check"] = \
						gettext_lazy("Quantity based Combo with this name and product mapping already exists!!")
						return Response({
									"success": False,
									"error" : err_message,
									"message" : "Please correct listed errors!!"
									})
			else:
				serializer = QuantityComboSerializer(data=data)
				if serializer.is_valid():
					data_info = serializer.save()
					info_msg = gettext_lazy("Combo is created successfully!!")
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



class QuantityCombolisting(ListAPIView):
	"""
	Quantity Combo detail listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for providing the Quantity based Combo details of brand.
	"""
	permission_classes = (IsAuthenticated,)

	def get_queryset(self):
		user = self.request.user.id
		Company_id = get_user(user)
		queryset = QuantityCombo.objects.filter(Company=Company_id).order_by('-created_at')
		return queryset

	def list(self, request):
		queryset = self.get_queryset()
		serializer = QuantityComboSerializer(queryset, many=True)
		response_list = serializer.data 
		return Response({
					"success": True,
					"data" : response_list,
					"message" : "Quantity Combo detail API worked well!!"})



class PercentCombolisting(ListAPIView):
	"""
	Percent Combo detail listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for providing the Percent based Combo details of brand.
	"""
	permission_classes = (IsAuthenticated,)

	def get_queryset(self):
		user = self.request.user.id
		Company_id = get_user(user)
		queryset = PercentCombo.objects.filter(Company=Company_id).order_by('-created_at')
		return queryset

	def list(self, request):
		queryset = self.get_queryset()
		serializer = PercentComboSerializer(queryset, many=True)
		response_list = serializer.data 
		return Response({
					"success": True,
					"data" : response_list,
					"message" : "Percent Combo detail API worked well!!"})


class Couponlisting1(APIView):
	"""
	Coupon listing Configuration POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to provide all Coupon within brand.

		Data Post: {

			"company_auth_id" 	    : "3",
			"status"                ; "true"
		}

		Response: {

			"success": True,
			"data" : coupon_conf_data_serializer,
			"message": "Coupon fetching successful!!"
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			user = request.user.id
			cid = get_user(user)
			err_message = {}
			if data['status'] == True:
				query = Coupon.objects.\
						filter(Company=cid,active_status=1).order_by('-created_at')
			else:
				query = Coupon.objects.\
						filter(Company=cid,active_status=0).order_by('-created_at')

			coupon_conf_data_serializer = []
			for q in query:
				q_dict = {}
				q_dict["id"] = q.id
				q_dict["active_status"] = q.active_status
				q_dict['coupon_type'] = q.coupon_type
				q_dict['coupon_code'] = q.coupon_code
				q_dict['frequency'] = q.frequency
				q_dict['is_automated'] = q.is_automated
				q_dict['is_min_shop'] = q.is_min_shop
				v_time = q.valid_frm+timedelta(hours=5,minutes=30)
				q_dict['valid_frm'] = v_time.strftime("%d/%b/%y")
				v_till = q.valid_till+timedelta(hours=5,minutes=30)
				q_dict['valid_till'] = v_till.strftime("%d/%b/%y")
				domain_name = addr_set()
				img = str(q.image)
				if img != "" and img != None and img != "null":
					full_path = domain_name + str(img)
					q_dict['image'] = full_path
				else:
					q_dict['image'] = ''	
				if q.category_id !=None:
					q_dict['category_name'] = q.category.category_name
				else:
					q_dict['category_name'] = ''
				coupon_conf_data_serializer.append(q_dict)
			return Response(
					{
						"success": True,
						"data" : coupon_conf_data_serializer,
	 					"message": "Coupon fetching successful!!"
					}
					)
		except Exception as e:
			print("Coupon listing configuration Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})



class CouponRetrieval1(APIView):
	"""
	Coupon retrieval POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of Coupon data.

		Data Post: {
			"id"                   : "1"
		}

		Response: {

			"success": True, 
			"message": "Coupon retrieval api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			err_message = {}
			err_message["id"] = \
					validation_master_anything(data["id"],
					"Coupon Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = Coupon.objects.filter(id=data['id'])
			if record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Provided Coupon data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				q_dict = {}
				q_dict["id"] = record[0].id
				q_dict["coupon_type"] = []
				coupon_dict = {}
				coupon_dict["label"] = record[0].coupon_type
				coupon_dict["key"] = record[0].coupon_type
				coupon_dict["value"] = record[0].coupon_type
				q_dict["coupon_type"].append(coupon_dict)
				q_dict["coupon_code"] = record[0].coupon_code
				q_dict["frequency"] = record[0].frequency
				q_dict["valid_frm"] = record[0].valid_frm
				q_dict["valid_till"] = record[0].valid_till
				q_dict["category"] = []
				cat_dict = {}
				if record[0].category_id != None:
					cat_dict["label"] = record[0].category.category_name
					cat_dict["key"] = record[0].category_id
					cat_dict["value"] = record[0].category_id
					q_dict["category"].append(cat_dict)
				else:
					pass
				q_dict["product_detail"] = []
				pa = record[0].product_map
				for p in pa:
					query = Product.objects.filter(id=p)
					p_dict = {}
					p_dict["label"] = query[0].product_name
					p_dict["key"] = query[0].id
					p_dict["value"] = query[0].id
					q_dict["product_detail"].append(p_dict)
				q_dict["outlet_detail"] = []
				pa = record[0].outlet_id
				if pa != None:
					for p in pa:
						query = OutletProfile.objects.filter(id=p)
						p_dict = {}
						p_dict["label"] = query[0].Outletname
						p_dict["key"] = query[0].id
						p_dict["value"] = query[0].id
						q_dict["outlet_detail"].append(p_dict)
				else:
					pass
				q_dict["flat_discount"] = record[0].flat_discount
				q_dict["flat_percentage"] = record[0].flat_percentage
				q_dict["is_min_shop"] = record[0].is_min_shop
				q_dict["is_automated"] = record[0].is_automated
				q_dict["min_shoping"] = record[0].min_shoping
				q_dict["max_shoping"] = record[0].max_shoping
				q_dict["active_status"] = record[0].active_status
				domain_name = addr_set()
				img = str(record[0].image)
				if img != "" and img != None and img != "null":
					full_path = domain_name + str(img)
					q_dict['image'] = full_path
				else:
					q_dict['image'] = ''	



				final_result.append(q_dict)
			if final_result:
				return Response({
							"success": True, 
							"message": "Coupon retrieval api worked well!!",
							"data": final_result,
							})
			else:
				return Response({
							"success": True, 
							"message": "No Coupon data found!!"
							})
		except Exception as e:
			print("Coupon retrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})




class QuantityComboRetrieval(APIView):
	"""
	Quantity Combo retrieval POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of Quantity Combo data.

		Data Post: {
			"id"                   : "1"
		}

		Response: {

			"success": True, 
			"message": "Quantity Combo retrieval api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			err_message = {}
			err_message["id"] = \
					validation_master_anything(data["id"],
					"Combo Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = QuantityCombo.objects.filter(id=data['id'])
			if record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Provided Quantity Combo data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				q_dict = {}
				q_dict["id"] = record[0].id
				q_dict["combo_name"] = record[0].combo_name
				q_dict["product_detail"] = []
				p_dict = {}
				p_dict["label"] = record[0].product.product_name
				p_dict["key"] = record[0].product_id
				p_dict["value"] = record[0].product_id
				q_dict["product_detail"].append(p_dict)
				q_dict["free_product_detail"] = []
				f_p_dict = {}
				f_p_dict["label"] = record[0].free_product.product_name
				f_p_dict["key"] = record[0].free_product_id
				f_p_dict["value"] = record[0].free_product_id
				q_dict["free_product_detail"].append(f_p_dict)
				q_dict["product_quantity"] = record[0].product_quantity
				q_dict["free_pro_quantity"] = record[0].free_pro_quantity
				q_dict["valid_frm"] = record[0].valid_frm
				q_dict["valid_till"] = record[0].valid_till
				q_dict["active_status"] = record[0].active_status
				final_result.append(q_dict)
			if final_result:
				return Response({
							"success": True, 
							"message": "Quantity Combo retrieval api worked well!!",
							"data": final_result,
							})
			else:
				return Response({
							"success": True, 
							"message": "No Quantity Combo data found!!"
							})
		except Exception as e:
			print("Quantity Combo retrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})


class PercentComboRetrieval(APIView):
	"""
	Percent Combo retrieval POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of Percent Combo data.

		Data Post: {
			"id"                   : "1"
		}

		Response: {

			"success": True, 
			"message": "Percent Combo retrieval api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			err_message = {}
			err_message["id"] = \
					validation_master_anything(data["id"],
					"Combo Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = PercentCombo.objects.filter(id=data['id'])
			if record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Provided Percent Combo data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				q_dict = {}
				q_dict["id"] = record[0].id
				q_dict["pcombo_name"] = record[0].pcombo_name
				q_dict["product_detail"] = []
				p_dict = {}
				p_dict["label"] = record[0].product.product_name
				p_dict["key"] = record[0].product_id
				p_dict["value"] = record[0].product_id
				q_dict["product_detail"].append(p_dict)
				q_dict["discount_product_detail"] = []
				d_p_dict = {}
				d_p_dict["label"] = record[0].discount_product.product_name
				d_p_dict["key"] = record[0].discount_product_id
				d_p_dict["value"] = record[0].discount_product_id
				q_dict["discount_product_detail"].append(d_p_dict)
				q_dict["discount_percent"] = record[0].discount_percent
				q_dict["valid_frm"] = record[0].valid_frm
				q_dict["valid_till"] = record[0].valid_till
				q_dict["active_status"] = record[0].active_status
				final_result.append(q_dict)
			if final_result:
				return Response({
							"success": True, 
							"message": "Percent Combo retrieval api worked well!!",
							"data": final_result,
							})
			else:
				return Response({
							"success": True, 
							"message": "No Percent Combo data found!!"
							})
		except Exception as e:
			print("Percent Combo retrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})


class CouponAction(APIView):
	"""
	Coupon Action POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to activate or deactivate Coupon.

		Data Post: {
			"id"                   		: "2",
			"active_status"             : "0"
		}

		Response: {

			"success": True, 
			"message": "Coupon is deactivated now!!",
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
			err_message = {}
			if data["active_status"] == "true":
				pass
			elif data["active_status"] == "false":
				pass
			else:
				err_message["active_status"] = "Active status data is not valid!!"
			err_message["id"] = \
						validation_master_anything(data["id"],
						"Coupon Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = Coupon.objects.filter(id=data["id"])
			if record.count() != 0:
				data["updated_at"] = datetime.now()
				if data["active_status"] == "true":
					info_msg = "Coupon is activated successfully!!"
				else:
					info_msg = "Coupon is deactivated successfully!!"
				serializer = \
				CouponSerializer(record[0],data=data,partial=True)
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
						"message": "Coupon id is not valid to update!!"
					}
					)
			final_result = []
			final_result.append(serializer.data)
			return Response({
						"success": True, 
						"message": info_msg,
						"data": final_result,
						})
		except Exception as e:
			print("Coupon action Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})



class QuantityComboAction(APIView):
	"""
	Quantity Combo Action POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to activate or deactivate Quantity based Combo.

		Data Post: {
			"id"                   		: "2",
			"active_status"             : "0"
		}

		Response: {

			"success": True, 
			"message": "Combo is deactivated now!!",
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
			err_message = {}
			if data["active_status"] == "true":
				pass
			elif data["active_status"] == "false":
				pass
			else:
				err_message["active_status"] = "Active status data is not valid!!"
			err_message["id"] = \
						validation_master_anything(data["id"],
						"Combo Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = QuantityCombo.objects.filter(id=data["id"])
			if record.count() != 0:
				data["updated_at"] = datetime.now()
				if data["active_status"] == "true":
					info_msg = "Combo is activated successfully!!"
				else:
					info_msg = "Combo is deactivated successfully!!"
				serializer = \
				QuantityComboSerializer(record[0],data=data,partial=True)
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
						"message": "Combo id is not valid to update!!"
					}
					)
			final_result = []
			final_result.append(serializer.data)
			return Response({
						"success": True, 
						"message": info_msg,
						"data": final_result,
						})
		except Exception as e:
			print("Quantity Combo action Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})



class PercentComboAction(APIView):
	"""
	Percent Combo Action POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to activate or deactivate Percent based Combo.

		Data Post: {
			"id"                   		: "2",
			"active_status"             : "0"
		}

		Response: {

			"success": True, 
			"message": "Combo is deactivated now!!",
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
			err_message = {}
			if data["active_status"] == "true":
				pass
			elif data["active_status"] == "false":
				pass
			else:
				err_message["active_status"] = "Active status data is not valid!!"
			err_message["id"] = \
						validation_master_anything(data["id"],
						"Coupon Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = PercentCombo.objects.filter(id=data["id"])
			if record.count() != 0:
				data["updated_at"] = datetime.now()
				if data["active_status"] == "true":
					info_msg = "Combo is activated successfully!!"
				else:
					info_msg = "Combo is deactivated successfully!!"
				serializer = \
				PercentComboSerializer(record[0],data=data,partial=True)
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
						"message": "Combo id is not valid to update!!"
					}
					)
			final_result = []
			final_result.append(serializer.data)
			return Response({
						"success": True, 
						"message": info_msg,
						"data": final_result,
						})
		except Exception as e:
			print("Percent Combo action Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})



class CouponRetrieval(APIView):
	"""
	Coupon retrieval POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of Discount data.

		Data Post: {
			"id"                   : "1"
		}

		Response: {

			"success": True, 
			"message": "Discount retrieval api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			err_message = {}
			err_message["id"] = \
					validation_master_anything(data["id"],
					"Discount Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = Discount.objects.filter(id=data['id'])
			if record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Provided Coupon data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				q_dict = {}
				q_dict["id"] = record[0].id
				q_dict["discount_type"] = []
				coupon_dict = {}
				coupon_dict["label"] = record[0].discount_type
				coupon_dict["key"] = record[0].discount_type
				coupon_dict["value"] = record[0].discount_type
				q_dict["discount_type"].append(coupon_dict)
				q_dict["valid_frm"] = record[0].valid_frm
				q_dict["discount_name"] = record[0].discount_name
				q_dict["valid_till"] = record[0].valid_till
				q_dict["is_all_category"] = record[0].is_all_category
				q_dict["is_all_product"] = record[0].is_all_product
				q_dict["category"] = []				
				pa = record[0].category_map
				if pa != None:
					for p in pa:
						query = ProductCategory.objects.filter(id=p)
						p_dict = {}
						p_dict["label"] = query[0].category_name
						p_dict["key"] = query[0].id
						p_dict["value"] = query[0].id
						q_dict["category"].append(p_dict)
				else:
					pass
				q_dict["product_detail"] = []
				pa = record[0].product_map
				for p in pa:
					query = Product.objects.filter(id=p)
					p_dict = {}
					p_dict["label"] = query[0].product_name
					p_dict["key"] = query[0].id
					p_dict["value"] = query[0].id
					q_dict["product_detail"].append(p_dict)
				q_dict["user_roll"] = []
				pa = record[0].user_roll
				for p in pa:
					query = UserType.objects.filter(id=p)
					p_dict = {}
					p_dict["label"] = query[0].user_type
					p_dict["key"] = query[0].id
					p_dict["value"] = query[0].id
					q_dict["user_roll"].append(p_dict)
				q_dict["outlet_detail"] = []
				pa = record[0].outlet_id
				for p in pa:
					query = OutletProfile.objects.filter(id=p)
					p_dict = {}
					p_dict["label"] = query[0].Outletname
					p_dict["key"] = query[0].id
					p_dict["value"] = query[0].id
					q_dict["outlet_detail"].append(p_dict)

				q_dict["flat_discount"] = record[0].flat_discount
				q_dict["flat_percentage"] = record[0].flat_percentage
				q_dict["is_min_shop"] = record[0].is_min_shop
				q_dict["is_reason_required"] = record[0].is_reason_required
				q_dict["min_shoping"] = record[0].min_shoping
				q_dict["max_shoping"] = record[0].max_shoping
				q_dict["active_status"] = record[0].active_status
				domain_name = addr_set()
				img = str(record[0].image)
				if img != "" and img != None and img != "null":
					full_path = domain_name + str(img)
					q_dict['image'] = full_path
				else:
					q_dict['image'] = ''



				final_result.append(q_dict)
			if final_result:
				return Response({
							"success": True, 
							"message": "Discount retrieval api worked well!!",
							"data": final_result,
							})
			else:
				return Response({
							"success": True, 
							"message": "No Discount data found!!"
							})
		except Exception as e:
			print("Discount retrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})





class Couponlisting(ListAPIView):
	"""
	Coupon detail listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for providing the Coupon details of brand.
	"""
	permission_classes = (IsAuthenticated,)

	def get_queryset(self):
		user = self.request.user
		auth_id = user.id
		Company_id = get_user(auth_id)
		queryset = Discount.objects.filter(Company=Company_id).order_by('-created_at')
		return queryset

	def list(self, request):
		queryset = self.get_queryset()
		serializer = CouponsSerializer(queryset, many=True)
		response_list = serializer.data 
		return Response({
					"success": True,
					"data" : response_list,
					"message" : "Discount profile detail API worked well!!"})




class CouponActions(APIView):
	"""
	Coupon Action POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to activate or deactivate Discount.

		Data Post: {
			"id"                   		: "2",
			"active_status"             : "0"
		}

		Response: {

			"success": True, 
			"message": "Coupon is deactivated now!!",
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
			err_message = {}
			if data["active_status"] == "true":
				pass
			elif data["active_status"] == "false":
				pass
			else:
				err_message["active_status"] = "Active status data is not valid!!"
				
			err_message["id"] = \
						validation_master_anything(data["id"],
						"Discount Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = Discount.objects.filter(id=data["id"])
			if record.count() != 0:
				data["updated_at"] = datetime.now()
				if data["active_status"] == "true":
					info_msg = "Discount is activated successfully!!"
				else:
					info_msg = "Discount is deactivated successfully!!"
				serializer = \
				DiscountSerializer(record[0],data=data,partial=True)
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
						"message": "Discount id is not valid to update!!"
					}
					)
			final_result = []
			final_result.append(serializer.data)
			return Response({
						"success": True, 
						"message": info_msg,
						"data": final_result,
						})
		except Exception as e:
			print("Discount action Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})



class ReasonCreationUpdation(APIView):
	"""
	Reason Creation & Updation POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create & update Discount Reason.

		Data Post: {
			"id"                       : "1"(Send this key in update record case,else it is not required!!)
			"reason"		           : "dddddd",
		}

		Response: {

			"success": True, 
			"message": "Discount Reason creation/updation api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			user = request.user.id
			cid = get_user(user)
			err_message = {}
			err_message["reason"] = \
					validation_master_anything(data["reason"],
					"Discount Reason",description_re, 2)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			if "id" in data:
				unique_check = DiscountReason.objects.filter(~Q(id=data["id"]),\
								Q(reason=data["reason"]),Q(Company_id=cid))
			else:
				unique_check = DiscountReason.objects.filter(Q(reason=data["reason"]),\
										Q(Company_id=cid))
			if unique_check.count() != 0:
				err_message["unique_check"] = "Discount Reason with this name already exists!!"
			else:
				pass
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			data["active_status"] = 1
			data['Company'] = cid
			if "id" in data:
				reason_record = DiscountReason.objects.filter(id=data['id'])
				if reason_record.count() == 0:
					return Response(
					{
						"success": False,
	 					"message": "Discount Reason is not valid to update!!"
					}
					)
				else:
					data["updated_at"] = datetime.now()
					reason_serializer = \
					ReasonSerializer(reason_record[0],data=data,partial=True)
					if reason_serializer.is_valid():
						data_info = reason_serializer.save()
						info_msg = "Discount Reason is updated successfully!!"
					else:
						print("something went wrong!!")
						return Response({
							"success": False, 
							"message": str(reason_serializer.errors),
							})
			else:
				reason_serializer = ReasonSerializer(data=data)
				if reason_serializer.is_valid():
					data_info = reason_serializer.save()
					info_msg = "Discount Reason  is created successfully!!"
				else:
					print("something went wrong!!")
					return Response({
						"success": False, 
						"message": str(reason_serializer.errors),
						})
			return Response({
						"success": True, 
						"message": info_msg
						})
		except Exception as e:
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})



class ReasonAction(APIView):

	"""
	Discount Reason Action POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to activate or deactivate Tag.

		Data Post: {
			"id"                   		: "2",
			"active_status"             : "0"
		}

		Response: {

			"success": True, 
			"message": "Discount Reason is deactivated now!!",
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
			err_message = {}
			if data["active_status"] == "true":
				pass
			elif data["active_status"] == "false":
				pass
			else:
				err_message["active_status"] = "Active status data is not valid!!"

			err_message["id"] = \
						validation_master_anything(data["id"],
						"Discount Reason Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = DiscountReason.objects.filter(id=data["id"])
			if record.count() != 0:
				data["updated_at"] = datetime.now()
				if data["active_status"] == "true":
					info_msg = "Discount Reason is activated successfully!!"
				else:
					info_msg = "Discount Reason is deactivated successfully!!"
				serializer = \
				ReasonSerializer(record[0],data=data,partial=True)
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
						"message": "Discount Reason id is not valid to update!!"
					}
					)
			final_result = []
			final_result.append(serializer.data)
			return Response({
						"success": True, 
						"message": info_msg,
						"data": final_result,
						})
		except Exception as e:
			print("Discount Reason action Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})



class ReasonRetrieve(APIView):

	"""
	Discount Reason POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used for retrieval of Discount Reason data.

		Data Post: {
			"id"                   : "1"
		}

		Response: {

			"success": True, 
			"message": "Discount Reason retrieval api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			err_message = {}
			err_message["id"] = \
					validation_master_anything(data["id"],
					"Discount Reason Id",contact_re, 1)

			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})

			record = DiscountReason.objects.filter(id=data['id'])
			if record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Provided Discount reason data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				q_dict = {}
				q_dict["id"] = record[0].id
				q_dict["reason"] = record[0].reason
				q_dict["active_status"] = record[0].active_status
				q_dict["created_at"] = record[0].created_at
				q_dict["updated_at"] = record[0].updated_at
				final_result.append(q_dict)
			return Response({
						"success": True, 
						"message": "Discount Reason retrieval api worked well!!",
						"data": final_result,
						})
		except Exception as e:
			print("Discount Reason retrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})


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