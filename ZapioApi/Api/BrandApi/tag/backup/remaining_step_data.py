from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime
from django.db.models import Sum,Count
#Serializer for api
from rest_framework import serializers
from Product.models import ProductCategory
from kitchen.models import StepToprocess
from Product.models import Product,Variant,ProductCategory
from Brands.models import Company
from django.db.models import Q


def addr_set():
	domain_name = "https://zapio-admin.com/media/"
	return domain_name

class ProductCategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductCategory
		fields = '__all__'


class StepProcessRemaining(APIView):

	"""
	Remaining Step process data  POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for Remaining Step processs data within brand.

		Data Post: {
			
		}

		Response: {


		}

	"""
	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			data = request.data
			user = request.user
			company_id = Company.objects.filter(auth_user_id=user.id).first().id
			allproduct_data = Product.objects.filter(Q(active_status=1),Q(Company=company_id))
			final_result = []
			for i in  allproduct_data:
				rema = {}
				product_id = i.id
				is_variant = i.has_variant
				rema['product_id'] = i.id
				cat_name = ProductCategory.objects.filter(id=i.product_category_id)[0].category_name
				pro_name = Product.objects.filter(id=i.id).first().product_name
				rema['product_name'] =  pro_name + " | " + cat_name
				if is_variant == True:
					b = i.variant_deatils
					vlen = len(i.variant_deatils)
					for k in range(vlen):
						remai = {}
						vname = b[k]['name']
						variant_id = Variant.objects.filter(variant=vname).first().id
						chk_step = StepToprocess.objects.filter(Q(product_id=product_id),Q(varient_id=variant_id))
						if chk_step.count() > 0:
							pass
						else:
							remai['product_id'] = rema['product_id']
							remai['va_id'] = variant_id
							cat_name = ProductCategory.objects.filter(id=i.product_category_id)[0].category_name
							pro_name = Product.objects.filter(id=rema['product_id']).first().product_name
							remai['product_name'] = pro_name + " | " + cat_name
							remai['varient_name'] = Variant.objects.filter(id=variant_id).first().variant
							final_result.append(remai)
				else:
					chk_step = StepToprocess.objects.filter(Q(product_id=product_id))
					if chk_step.count() > 0:
						pass
					else:
						final_result.append(rema)

			if len(final_result) > 0:
				return Response({
							"success": True, 
							"data": final_result,
							})
			else:
				return Response({
							"success": False, 
							"data": "No Data Found",
							})
		except Exception as e:
			print("Process retrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, 
							"message": "Error happened!!", 
							"errors": str(e)})
