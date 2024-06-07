import re
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
from datetime import datetime
from ZapioApi.Api.BrandApi.listing.listing import addr_set
from rest_framework import serializers
from Product.models import (Product, 
							AddonDetails, 
							Tag,Variant,
							ProductImage,
							ProductCategory,
							ProductsubCategory)
from urbanpiper.models import *
from django.db.models import Q
from Configuration.models import TaxSetting,Tax
from kitchen.models import RecipeIngredient
from Configuration.models import Unit

class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = '__all__'


class ProductRetrieval(APIView):
	"""
	Product retrieval POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of Product data.

		Data Post: {
			"id"                   : "60"
		}

		Response: {

			"success": True, 
			"message": "Product retrieval api worked well!!",
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
					"Product Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = Product.objects.filter(id=data['id'])
			if record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Provided Product data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				q_dict = {}
				q_dict["id"] = record[0].id
				q_dict["cat_detail"] = []
				catDetail = record[0].product_categorys
				if catDetail !=None:
					for index in catDetail:
						cat_dict = {}
						cat_dict["label"] = ProductCategory.objects.filter(id=index)[0].category_name
						cat_dict['value'] = int(index)
						q_dict["cat_detail"].append(cat_dict)
				q_dict["subcat_detail"] = []
				subcatDetail = record[0].product_subcategorys
				if subcatDetail !=None:
					for index in subcatDetail:
						subcat_dict = {}
						subcat_dict["label"] = ProductsubCategory.objects.filter(id=index)[0].subcategory_name
						subcat_dict['value'] = int(index)
						q_dict["subcat_detail"].append(subcat_dict)
				else:
					q_dict["subcat_detail"] = []
				if record[0].spice != None:
					q_dict["spice_detail"] = []
					spice_dict = {}
					spice_dict["label"] = record[0].spice
					spice_dict["key"] = record[0].spice
					spice_dict["value"] = record[0].spice
					q_dict["spice_detail"].append(spice_dict)
				else:
					q_dict["spice_detail"] = []
				q_dict['pin']  = record[0].primaryIngredient_deatils
				va = q_dict['pin']
				if va != None:
					for v in va:
						if 'pingredient' in v:
							pin = v['pingredient']
							r = RecipeIngredient.objects.filter(id=pin)
							if r.count() > 0:
								pname = r[0]
								v['primaryIng'] = {}
								v['primaryIng']["label"] = pname.name
								v['primaryIng']["key"] = pin
								v['primaryIng']["value"] = pin
						if 'unit' in v:
							pin = v['unit']
							u = Unit.objects.filter(id=pin)
							if u.count() > 0:
								pname = u[0]
								v['unit'] = {}
								v['unit']["label"] = pname.unit_name
								v['unit']["key"] = pin
								v['unit']["value"] = pin
						del v["pingredient"]
					q_dict['pin'] = va
				q_dict["product_schema"] = record[0].product_schema
				ps = q_dict['product_schema']
				if ps !=None:
					for v in ps:
						if 'unit' in v:
							pin = v['unit']
							pname = Unit.objects.filter(id=pin)[0]
							v['unit'] = {}
							v['unit']["label"] = pname.unit_name
							v['unit']["key"] = pin
							v['unit']["value"] = pin
					q_dict['product_schema'] = ps
				else:
					pass
				if record[0].delivery_option != None:
					q_dict["delivery_option"] = record[0].delivery_option
				else:
					q_dict['delivery_option'] = ''
				q_dict["product_name"] = record[0].product_name
				q_dict["food_type"] = record[0].food_type.food_type
				q_dict["foodtype_detail"] = []
				food_dict = {}
				food_dict["label"] = record[0].food_type.food_type
				food_dict["key"] = record[0].food_type_id
				food_dict["value"] = record[0].food_type_id
				q_dict["foodtype_detail"].append(food_dict)
				q_dict["priority"] = record[0].priority
		
				q_dict["product_image"] = record[0].product_image
				full_path = addr_set()
				if q_dict["product_image"] != None and q_dict["product_image"]!="":
					q_dict["product_image"] = full_path+str(q_dict["product_image"])
				else:
					q_dict["product_image"] = None
				q_dict["product_video"] = record[0].pvideo
				full_path = addr_set()
				if q_dict["product_video"] != None and q_dict["product_video"]!="":
					q_dict["product_video"] = full_path+str(q_dict["product_video"])
				else:
					q_dict["product_video"] = None
				q_dict["product_image"] = []
				pimg = ProductImage.objects.filter(product_id=data['id'])
				if pimg.count() > 0:
					for index in pimg:
						full_path = addr_set()
						fimgs = full_path+str(index.product_image)
						q_dict["product_image"].append(fimgs)
				q_dict["product_code"] = record[0].product_code
				q_dict["product_desc"] = record[0].product_desc
				q_dict["kot_desc"] = record[0].kot_desc
				q_dict["has_variant"] = record[0].has_variant
				q_dict["price"] = record[0].price
				q_dict["is_recommended"] = record[0].is_recommended
				q_dict["discount_price"] = record[0].discount_price
				q_dict["variant_deatils"] = record[0].variant_deatils
				q_dict["is_recommended"] = record[0].is_recommended
				q_dict["packing_charge"] = record[0].packing_charge
				q_dict["short_desc"] = record[0].short_desc
				va = q_dict["variant_deatils"] 
				if va != None:
					for v in va:
						if "name" in v:
							v_name = v["name"]
							v["name"] = {}
							v["name"]["id"] = v_name
							p_id= record[0].id
							v["name"]["label"] = v_name
							v["name"]["key"] = v_name
							v["dis"] = v["discount_price"]
							v_id = Variant.objects.filter(variant=v_name)[0].id
							p_v=ProductSync.objects.filter(Q(product_id=p_id),\
								  Q(variant_id=v_id))
							if p_v.count() > 0:
								v['u_id'] = p_v[0].id
							else:
								pass
							v_addon = v["addon_group"]
							v["addonGroup"] = []
							if len(v_addon) != 0:
								for i in v_addon:
									v_addon_dict = {}
									addon_q = AddonDetails.objects.filter(id=i)
									if addon_q.count() > 0:
										v_addon_dict["value"] = addon_q[0].id
										v_addon_dict["key"] = addon_q[0].id
										v_addon_dict["label"] = addon_q[0].addon_gr_name
										v["addonGroup"].append(v_addon_dict)
									else:
										pass
							else:
								pass
							del v["addon_group"]
							del v["discount_price"]
						else:
							pass
					q_dict["variant_deatils"] = va
				else:
					pass
				addons_detail = record[0].addpn_grp_association
				q_dict["addon_details"] = []
				if addons_detail != None:
					for q in addons_detail:
						addon_q = AddonDetails.objects.filter(id=q)
						if addon_q.count() > 0:
							addon_dict = {}
							addon_dict["value"] = addon_q[0].id
							addon_dict["key"] = addon_q[0].id
							addon_dict["label"] = addon_q[0].addon_gr_name
							addon_dict["associated_addons"] = addon_q[0].associated_addons
							q_dict["addon_details"].append(addon_dict)
						else:
							pass
				else:
					pass
				tag_detail  = record[0].tags
				q_dict["tags"] = []
				if tag_detail != None:
					for i in tag_detail:
						tag_q = Tag.objects.filter(id=i)
						if tag_q.count() > 0:
							tag_dict = {}
							tag_dict["value"] = tag_q[0].id
							tag_dict["key"] = tag_q[0].id
							tag_dict["label"] = tag_q[0].tag_name
							q_dict["tags"].append(tag_dict)
						else:
							pass
				else:
					pass
				platform_detail  = record[0].included_platform
				q_dict["platform_detail"] = []
				if platform_detail != None:
					for i in platform_detail:
						tag_dict = {}
						tag_dict["value"] = i
						tag_dict["key"] = i
						tag_dict["label"] = i
						q_dict["platform_detail"].append(tag_dict)
				else:
					pass
				allergen_detail  = record[0].allergen_Information
				q_dict["allergen_Information"] = []
				if allergen_detail != None:
					for i in allergen_detail:
						in_dict = {}
						in_dict["value"] = i
						in_dict["key"] = i
						in_dict["label"] = i
						q_dict["allergen_Information"].append(in_dict)
				else:
					pass
				tax_detail = record[0].tax_association
				q_dict["tax_association"] = []
				if tax_detail != None:
					for i in tax_detail:
						tax_q = Tax.objects.filter(id=i)
						if tax_q.count() != 0:
							tax_dict = {}
							tax_dict["value"] = tax_q[0].id
							tax_dict["key"] = tax_q[0].id
							tax_dict["label"] = str(tax_q[0].tax_name)+" | "+str(tax_q[0].tax_percent)+"%" 
							q_dict["tax_association"].append(tax_dict)
						else:
							pass
				else:
					pass
				q_dict['packaging_amount'] = record[0].packing_amount
				q_dict['price_types'] = []
				if record[0].price_type != None:
					dic = {}
					dic['label'] = record[0].price_type
					dic['value'] = record[0].price_type
					q_dict['price_types'].append(dic)

				packageTax = record[0].package_tax
				q_dict["package_tax"] = []
				if packageTax != None:
					for i in packageTax:
						tax_q = Tax.objects.filter(id=i)
						if tax_q.count() != 0:
							tax_dict = {}
							tax_dict["value"] = tax_q[0].id
							tax_dict["key"] = tax_q[0].id
							tax_dict["label"] = str(tax_q[0].tax_name)+" | "+str(tax_q[0].tax_percent)+"%" 
							q_dict["package_tax"].append(tax_dict)
						else:
							pass
				else:
					pass
				q_dict["is_tax"] = record[0].is_tax


				final_result.append(q_dict)
			if final_result:
				return Response({
							"success": True, 
							"message": "Product retrieval api worked well!!",
							"data": final_result,
							})
			else:
				return Response({
							"success": True, 
							"message": "No product data found!!"
							})
		except Exception as e:
			print("Product retrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})


