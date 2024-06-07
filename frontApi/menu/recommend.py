from rest_framework.views import APIView
from rest_framework.response import Response
from Product.models import ProductCategory, Product_availability, Category_availability, Product,\
Variant,ProductsubCategory,ProductImage
from Outlet.models import OutletProfile
from Brands.models import Company
import re
from django.conf import settings
from ZapioApi.api_packages import *
from datetime import datetime
from django.db.models import Q
import random
from zapio.settings import Media_Path
from Configuration.models import *


class ProductRecommend(APIView):
	"""
	Product Recommended  POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used to recommended product.

		Data Post: {

			"product_id" : 627
		}

		Response: {

			"success": True,
			"credential" : True,
			"product_count" : product_count,
			"menu_data" : final_result
		}

	"""
	def post(self, request, format=None):
		try:
			data = request.data
			record = Product.objects.filter(id=str(data['product_id']))
			rating = [3,5,4.2]
			if record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Provided Product data is not valid to retrieve!!"
				})
			else:
				category = record[0].product_categorys
				final_result = []
				if len(category) > 0:
					pid = []
					for index in category:
						pcount = Product.objects.filter(Q(product_categorys__icontains=index),Q(Company=data['Company']))
						for i in pcount:
							pid.append(i.id)
						fid = []
						for k in range(0,4):
							random_num = random.choice(pid)
							if random_num in fid:
								pass
							else:
								fid.append(random_num)
						for m in fid:
							if str(m) != str(data['product_id']):
								query = Product.objects.filter(id=m)
								if query.count()!=0:
									s  = query[0]
									menu_info = {}
									menu_info["name"] = s.product_name
									menu_info["product_id"] = s.id
									menu_info["product_desc"] = s.product_desc
									menu_info["allergen"] = s.allergen_Information
									menu_info["product_rating"] = random.choice(rating)
									menu_info["parent_category_id"] = s.product_categorys
									menu_info["parent_category_name"] = []
									if len(s.product_categorys) > 0:
										for index in s.product_categorys:
											cat_dict = {}
											category_name = ProductCategory.objects.filter(id=index)
											cat_dict['parent_category_name'] = category_name[0].category_name
											cat_dict['parent_category_id'] = index
											menu_info["parent_category_name"].append(cat_dict)
									else:
										menu_info["parent_category_name"] =[]
									p = s.product_schema
									fs = []
									if p !=None:
										if len(p) > 0:
											for k in p:
												dic = {}
												if 'unit' in k:
													pin = k['unit']
													uname = Unit.objects.filter(id=pin)[0].unit_name
													quantity = k['quantity']
													name = k['name']
													dic['name'] = name
													dic['qty'] = str(quantity)+' '+str(uname)
													fs.append(dic)
										else:
											pass
									else:
										pass
									menu_info["nutrition"] = fs
									menu_info["tax_detail"] = []
									associate_tax = s.tax_association
									if associate_tax != None:
										if len(associate_tax) == 0:
											pass
										else:
											for t in associate_tax:
												tax_dict = {}
												tax_q = Tax.objects.filter(id=t)[0]
												tax_dict["id"] = tax_q.id
												tax_dict["tax_name"] = tax_q.tax_name+" | "+str(tax_q.tax_percent)
												tax_dict["tax_percent"] = tax_q.tax_percent
												menu_info["tax_detail"].append(tax_dict)
									else:
										pass
									menu_info["subcategory_name"] =[]
									if len(s.product_categorys) > 0:
										for index in s.product_categorys:
											sub_dict = {}
											sav = ProductsubCategory.objects.filter(category_id=index)
											if sav.count() > 0:
												sub_dict['parent_category_id'] = index
												sub_dict['category_id'] = sav[0].id
												sub_dict['category_name'] = sav[0].subcategory_name
												menu_info["subcategory_name"].append(sub_dict)
											else:
												menu_info["subcategory_name"] = []
									else:
										pass
									menu_info["food_type"] = s.food_type.food_type
									if s.food_type.foodtype_image != None or s.food_type.foodtype_image != "": 
										menu_info["food_type_image"] = \
										Media_Path+str(s.food_type.foodtype_image)
									else:
										menu_info["food_type_image"] = \
										None

									chk_imag = ProductImage.objects.filter(product_id=s.id,primary_image=1)
									if chk_imag.count() > 0:
										menu_info['primary_image'] = Media_Path+str(chk_imag[0].product_image)
									else:
										menu_info['primary_image'] = None
									chk_img = ProductImage.objects.filter(product_id=i,primary_image=0)
									if chk_img.count() > 0:
										menu_info['multiple_image'] = []
										for index in chk_img:
											menu_info['multiple_image'].append(Media_Path+str(chk_imag[0].product_image))
									else:
										menu_info['multiple_image'] = []


									has_variant = s.has_variant
									variant_deatils = s.variant_deatils
									if has_variant == False:
										menu_info["price"] = s.price
										menu_info["compare_price"] = s.discount_price
										menu_info["is_customize"] = 0
									else:
										li =[]
										li2 = []
										for j in variant_deatils:
											li.append(j["price"])
											li2.append(j["discount_price"])
										menu_info["price"] = min(li)
										menu_info["compare_price"] = min(li2)
										menu_info["Variant_id"] = \
										Variant.objects.filter(variant__iexact=variant_deatils[0]["name"])[0].id
										menu_info["Variant_name"] = variant_deatils[0]["name"]
										menu_info["is_customize"] = 1
									final_result.append(menu_info)
								else:
									pass
				else:
					pass
			if len(final_result) != 0:
				p_count = len(final_result)
				result = {
							"success": True,
							"credential" : True,
							"menu_data" : final_result
							}
			else:
				result = {
							"success": True,
							"credential" : True
						}
			return Response(result)
		except Exception as e:
			print("Product Listing Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})