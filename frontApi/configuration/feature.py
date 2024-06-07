import re
import json
import random
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from Brands.models import Company
from _thread import start_new_thread
from datetime import datetime
from django.db.models import Q
from Product.models import FeatureProduct,Product, Product_availability, Variant
from Outlet.models import OutletProfile
from zapio.settings import Media_Path


class FeatureProductList(APIView):
	"""
	Feature Product listing GET API

		Authentication Required		: No
		Service Usage & Description	: This Api is used for providing fetaured products of brand.

		{
			"outlet_id"                          : "1"
		}

		Response: {

			"success"  : True, 
			"message"  : "Feature Product api worked well!!",
			"data"     : final_result
		}

	"""
	# permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			record = Product_availability.objects.filter(outlet=data["outlet_id"])
			final_result = []
			rating = [4,5,4.7,4.2]
			if record.count()!=0:
				avail_product = record[0].available_product
				if len(avail_product) != 0:
					for i in avail_product:
						feature_query =\
						FeatureProduct.objects.filter(feature_product__contains=[str(i)],
							active_status=1,outlet=data["outlet_id"])
						if feature_query.count() == 0:
							feature_flag = 0
						else:
							feature_flag = 1
							query = Product.objects.filter(id=i,active_status=1)
						if feature_flag == 1 and query.count()!=0:
							s  = query[0]
							menu_info = {}
							menu_info["outlet_availbility_id"] = data["outlet_id"]
							menu_info["name"] = s.product_name
							menu_info["product_id"] = s.id
							menu_info["product_desc"] = s.product_desc
							menu_info["product_rating"] = random.choice(rating)
							menu_info["parent_category_id"] = s.product_category_id
							menu_info["parent_category_name"] = s.product_category.category_name
							menu_info["category_id"] = s.product_subcategory_id
							if menu_info["category_id"] != None:
								menu_info["category_name"] = \
								s.product_subcategory.subcategory_name
							else:
								menu_info["category_name"] = None
							menu_info["food_type"] = s.food_type.food_type
							if s.food_type.foodtype_image != None or s.food_type.foodtype_image != "": 
								menu_info["food_type_image"] = \
								Media_Path+str(s.food_type.foodtype_image)
							else:
								menu_info["food_type_image"] = \
								None
							if s.product_image != None and s.product_image != "":
								menu_info["product_image"] = \
								Media_Path+str(s.product_image)
							else:
								menu_info["product_image"] = \
								None
							has_variant = s.has_variant
							variant_deatils = s.variant_deatils
							if has_variant == False:
								menu_info["price"] = s.price
								menu_info["discount"] = s.discount_price
							else:
								li =[]
								li2 = []
								for j in variant_deatils:
									li.append(j["price"])
									li2.append(j["discount_price"])
								menu_info["price"] = min(li)
								menu_info["discount"] = min(li2)
								menu_info["Variant_id"] = \
								Variant.objects.filter(variant__iexact=variant_deatils[0]["name"])[0].id
								menu_info["Variant_name"] = variant_deatils[0]["name"]
							final_result.append(menu_info)
						else:
							pass
				else:
					pass
			else:
				pass
			if len(final_result) != 0:
				p_count = len(final_result)
				result = {
							"success": True,
							"credential" : True,
							"product_count" : p_count,
							"featured_data" : final_result
							}
			else:
				result = {
							"success": True,
							"credential" : True,
							"message" : "Featured Products are not set at brand manager level for this outlet!!"
						}
			return Response(result)
		except Exception as e:
			print(e)
			return Response({
							"success": False,
							"message":"Feature api stucked into exception!!"
							})

