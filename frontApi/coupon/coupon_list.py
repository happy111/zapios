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

from rest_framework import serializers
from Product.models import ProductCategory, Product
from ZapioApi.Api.BrandApi.discount.Validation.coupon_error_check import *
from UserRole.models import *
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user
from rest_framework.generics import ListAPIView
from discount.models import *
from ZapioApi.Api.BrandApi.coupon.Validation.coupon_error_check import *






class Couponlisting(APIView):
	"""
	Coupon  / discount listing Get API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to provide all Coupon / discount within brand.

		param: {

			"outlet_id" 	    : "3",

		}

		Response: {

			"success": True,
			"message": "Coupon fetching successful!!"
		}

	"""
	def get(self, request, format=None):
		try:
			from Brands.models import Company
			now = datetime.now()
			todate = now.date()
			outlet_id = str(request.query_params["outlet_id"]).strip()
			outlet_data = OutletProfile.objects.filter(id=outlet_id)
			if outlet_data.count() > 0:
				company_id = outlet_data[0].Company_id
			else:
				raise Exception("Invalide id!!")
			cdata = Coupon.objects.filter(Q(valid_till__gte=todate),\
					Q(Company_id=company_id),Q(active_status=1))
			coupon_conf_data_serializer = []
			if cdata.count() > 0:
				for q in cdata:
					q_dict = {}
					if q.frequency > 0 and q.is_banner == 1:
						if len(q.outlet_id) == 0 or outlet_id in q.outlet_id:
							q_dict["id"] = q.id
							q_dict["active_status"] = q.active_status
							q_dict['coupon_type'] = q.coupon_type
							q_dict['coupon_code'] = q.coupon_code
							q_dict['frequency'] = q.frequency
							q_dict['valid_frm'] = q.valid_frm.strftime("%d/%b/%y")
							q_dict['valid_till'] = q.valid_till.strftime("%d/%b/%y")
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
			ddata = Discount.objects.filter(Q(valid_till__gte=todate)
					,Q(Company_id=company_id),Q(active_status=1))
			if ddata.count() > 0:
				for q in ddata:
					q_dict = {}
					if q.is_banner == 1:
						if len(q.outlet_id) == 0 or outlet_id in q.outlet_id:
							q_dict["id"] = q.id
							q_dict["active_status"] = q.active_status
							q_dict['discount_type'] = q.discount_type
							q_dict['discount_name'] = q.discount_name
							q_dict['valid_frm'] = q.valid_frm.strftime("%d/%b/%y")
							q_dict['valid_till'] = q.valid_till.strftime("%d/%b/%y")
							domain_name = addr_set()
							img = str(q.image)
							if img != "" and img != None and img != "null":
								full_path = domain_name + str(img)
								q_dict['image'] = full_path
							else:
								q_dict['image'] = ''				
							if q.category_map !=None:
								q_dict['category_id'] = q.category_map
							else:
								q_dict['category_id'] = ''
							if q.product_map !=None:
								q_dict['product_map'] = q.product_map
							else:
								q_dict['product_map'] = ''
							coupon_conf_data_serializer.append(q_dict)
			return Response(
					{
						"success": True,
						"data" : coupon_conf_data_serializer,
	 					"message": "Coupon fetching successful!!"
					}
					)
		except Exception as e:
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})

