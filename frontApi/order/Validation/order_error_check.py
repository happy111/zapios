import re
import os
from ZapioApi.api_packages import *
from Product.models import FoodType, Product, ProductCategory, ProductsubCategory,\
	AddonDetails
from Orders.models import Order
from django.db.models import Q
from Outlet.models import OutletProfile
from django.db.models import Max

 # Validation check
def err_check(data):
	err_message = {}
	if data["coupon_code"] == "":
		pass
	else:
		
	if data["has_variant"] == "true":
		data["has_variant"]= 1
	else:
		data["has_variant"]= 0
	if data["has_variant"] == 0 or data["has_variant"] == 1:
		pass
	else:
		err_message["has_variant"] = "Has variant flag is not set!!"
	if data["has_variant"] == 0:
		data["variant_deatils"] = None
		try:
			data["price"] = float(data["price"])
			data["discount_price"] = float(data["discount_price"])
		except Exception as e:
			err_message["price"] = "Price or Discounted price value is not valid!!"
	else:
		data["price"] = 0
		data["discount_price"] = 0
		varint_unique_list = []
		if len(data["variant_deatils"]) != 0:
			for i in data["variant_deatils"]:
				if "name" in i and  "price" in i and "discount_price" in i and "addon_group" in i:
					pass
				else:
					err_message["variant_detail"] = \
					"Variant Price and name value is not set!!"
					break	
				if i["name"] not in varint_unique_list:
					varint_unique_list.append(i["name"])
				else:
					err_message["duplicate_variant"] = "Variants are duplicate!!"
					break

				err_message["varinat_name"] = \
				validation_master_anything(i["name"],"Variant name",
				username_re,3)
				
				if err_message["varinat_name"] != None:
					break
				try:
					i["price"] = float(i["price"])
					i["discount_price"] = float(i["discount_price"])
				except Exception as e:
					err_message["varinat_price"] = \
					"Variant Price value is not valid!!"
					break
		else:
			err_message["variant_detail"] = \
					"Variant Price and name value is not set!!"
	# if len(data["outlet_map"]) != 0:
	# 	outlet_unique = []
	# 	for i in data["outlet_map"]:
	# 		if i not in outlet_unique:
	# 			outlet_unique.append(i)
	# 		else:
	# 			err_message["outlet_duplicate"] = "Selected outlets are duplicate!!"
	# 			break
	# else:
	# 	err_message["outlet_map"] = "Please select at least one outlet!!"
	err_message["product_name"] = \
			validation_master_anything(data["product_name"],
			"Product name",product_re, 3)
	err_message["product_desc"] = \
		validate_anything(data["product_desc"], description_re, 
			zero__re,3, "Product Desription")
	err_message["product_code"] = \
		validate_anything(data["product_code"], username_re, 
			zero__re,3, "Product Code")
	err_message["food_type"] = \
				validation_master_anything(str(data["food_type"]),
				"Food Type",contact_re, 1)
	err_message["product_category"] = \
				validation_master_anything(str(data["product_category"]),
				"Category",contact_re, 1)
	err_message["priority"] = \
				validation_master_anything(data["priority"],
				"Priority",contact_re, 1)
	if any(err_message.values())==True:
		err = {
			"success": False,
			"error" : err_message,
			"message" : "Please correct listed errors!!"
			}
		return err
	else:
		return None


def record_check_integrity(data):
	err_message = {}
	if "id" in data:
		unique_check = Product.objects.filter(~Q(id=data["id"]),\
			Q(product_name__iexact=data["product_name"]),\
			Q(product_category=data["product_category"]))
	else:
		unique_check = Product.objects.filter(Q(product_name__iexact=data["product_name"]),\
								Q(product_category=data["product_category"]))
	if unique_check.count() != 0:
		err_message["unique_check"] = "Product with this name already exists!!"
	else:
		pass
	if "id" in data:
		unique_code_check = Product.objects.filter(~Q(id=data["id"]),\
			Q(product_code__iexact=data['product_code']),\
			Q(product_category=data["product_category"]))\
			.exclude(product_code__isnull=True).exclude(product_code__exact='')
	else:
		unique_code_check = Product.objects.filter(Q(product_code__iexact=data['product_code']),\
							Q(product_category=data["product_category"]))\
							.exclude(product_code__isnull=True).exclude(product_code__exact='')
	if unique_code_check.count() != 0:
		err_message["unique_code_check"] = "Product with this code already exists!!"
	else:
		pass
	if "id" in data:
		priority_check = Product.objects.filter(~Q(id=data["id"]),\
						Q(priority=int(data["priority"])))
	else:
		if data["priority"] != "":
			priority_check = Product.objects.filter(Q(priority=int(data["priority"])))
		else:
			err_message["info"] = "Product information is not provided properly!!"
	if priority_check.count() != 0:
		max_priority = \
		Product.objects.aggregate(Max('priority'))
		suggestion = max_priority["priority__max"] + 1
		err_message["priority_check"] = \
		"This priority is already assigned to other product..You can try "+str(suggestion)+" as priority!!"
	else:
		pass
	Addon_check = AddonDetails.objects.filter(active_status=1)
	if len(data["addpn_grp_association"]) != 0:
		for q in data['addpn_grp_association']:
			add_check = Addon_check.filter(id=q)
			if add_check.count() == 1:
				pass
			else:
				err_message["addpn_grp_association"] = \
				"Addon Group Association is not valid..Please check!!"
	else:
		pass
	if any(err_message.values())==True:
		err = {
			"success": False,
			"error" : err_message,
			"message" : "Please correct listed errors!!"
			}
		return err
	else:
		return None