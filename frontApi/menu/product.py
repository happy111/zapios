from rest_framework.views import APIView
from rest_framework.response import Response
from Product.models import *
from Outlet.models import OutletProfile
from Brands.models import Company
import re
from django.conf import settings
from ZapioApi.api_packages import *
from datetime import datetime
from django.db.models import Q
from rest_framework.generics import RetrieveAPIView
import random
from zapio.settings import Media_Path
from Configuration.models import *
from Product.models import Menu, Product,Addons
from  rest_framework import serializers
class MenuSerializer(serializers.ModelSerializer):
	class Meta:
		model = Menu
		fields = "__all__"

class FullProductList(APIView):
	"""
	Product Listing POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used to extract all product associated with outlet.

		Data Post: {

			"outlet_id" : 11
			"company_id":1    //optional (pass only 1 outlet_id or company_id)
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
			if "company_id" in data:
				outlet = OutletProfile.objects.filter(Company_id=data["company_id"]).first()
				data["outlet_id"] = outlet.id
			record = Product_availability.objects.filter(outlet=data["outlet_id"])
			final_result = []
			rating = [4,5,4.3,4.2]
			if record.count()!=0:
				avail_product = record[0].available_product
				if len(avail_product) != 0:
					for i in avail_product:
						query = Product.objects.filter(id=str(i),active_status=1,is_hide=0)
						if query.count()!=0:
							s  = query[0]
							menu_info = {}
							menu_info["outlet_availbility_id"] = data["outlet_id"]
							menu_info["name"] = s.product_name
							menu_info["product_id"] = s.id
							menu_info["product_desc"] = s.product_desc
							menu_info["short_desc"] = s.short_desc
							menu_info["allergen"] = s.allergen_Information
							menu_info["company"] = s.Company_id
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
							menu_info["product_rating"] = s.rating
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
							menu_info["tax_detail"] = []
							associate_tax = s.tax_association
							if associate_tax != None:
								if len(associate_tax) == 0:
									pass
								else:
									for t in associate_tax:
										tax_dict = {}
										t = Tax.objects.filter(id=t)
										if t.count() > 0:
											tax_q = t[0]
											tax_dict["id"] = tax_q.id
											tax_dict["tax_name"] = tax_q.tax_name+" | "+str(tax_q.tax_percent)
											tax_dict["tax_percent"] = tax_q.tax_percent
											menu_info["tax_detail"].append(tax_dict)
										else:
											pass
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

							chk_imag = ProductImage.objects.filter(product_id=i,primary_image=1)
							if chk_imag.count() > 0:
								menu_info['primary_image'] = Media_Path+str(chk_imag[0].product_image)
							else:
								menu_info['primary_image'] = None
							chk_img = ProductImage.objects.filter(product_id=i,primary_image=0)
							if chk_img.count() > 0:
								menu_info['multiple_image'] = []
								for index in chk_img:
									menu_info['multiple_image'].append(Media_Path+str(index.product_image))
									if index.video_url != None:
										menu_info['multiple_image'].append(str(index.video_url))

							else:
								menu_info['multiple_image'] = []
							
							has_variant = s.has_variant
							variant_deatils = s.variant_deatils
							if has_variant == False and len(s.addpn_grp_association) == 0:
								menu_info["price"] = s.price
								menu_info["compare_price"] = s.discount_price
								menu_info["is_customize"] = 0
							else:
								menu_info["price"] = s.price
								menu_info["compare_price"] = s.discount_price
								if s.addpn_grp_association != None:
									if len(s.addpn_grp_association) > 0:
										menu_info["addon_detail"] = []
										addon_detail = s.addpn_grp_association
										menu_info["is_customize"] = 1
										li =[]
										li2 = []
										for j in addon_detail:
											addon_detail = AddonDetails.objects.filter(id=j)
											ad = addon_detail[0].associated_addons
											for k in ad:
												dic = {}
												dic["price"] = k['price']
												dic["addon"] = k['addon_name']
												addon_data = Addons.objects.filter(name=dic['addon'],addon_amount=dic['price'],\
													Company_id=	menu_info["company"])
												if addon_data.count() > 0:
													dic['addon_id'] = addon_data[0].id
												else:
													pass
												menu_info["addon_detail"].append(dic)
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
							
							menu_info['packing_charge'] = []
							if s.price_type != None:
								temp = {}
								temp['price_type'] = s.price_type
								temp['packing_amount'] = s.packing_amount
								if s.is_tax == True:
									t = s.package_tax
									if len(t) > 0:
										temp['tax_detail'] = []
										for i in t:
											d = {}
											ta = Tax.objects.filter(id=str(i))
											if ta.count() > 0:
												d['tax_name'] = ta[0].tax_name
												d['percentage'] = ta[0].tax_percent
												temp['tax_detail'].append(d)
									else:
										pass
								menu_info['packing_charge'].append(temp)
							menu_info['tag_details'] = []
							if s.tags != None:
								if len(s.tags) > 0:
									for index in s.tags:
										tag = Tag.objects.filter(id=index)[0].tag_name
										menu_info['tag_details'].append(tag)
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
							"menu_data" : final_result
							}
			else:
				result = {
							"success": False,
							"message" : "No menu found",
						}
			return Response(result)
		except Exception as e:
			print("Product Listing Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})

class ProductDetailSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = "__all__"

class ProductDetails(RetrieveAPIView):
	"""
	Retreive API View for Produts

		just pass product id in url
	"""
	serializer_class = ProductDetailSerializer
	queryset = Product.objects.all()
