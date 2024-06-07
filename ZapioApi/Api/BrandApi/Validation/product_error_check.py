import re
import os
from ZapioApi.api_packages import *
from Product.models import FoodType, Product, ProductCategory, ProductsubCategory,\
	AddonDetails,Tag, Variant
from django.db.models import Q
from Outlet.models import OutletProfile
from django.db.models import Max
from Configuration.models import *
from django.db import transaction
from django.http import Http404
from django.utils.translation import gettext_lazy


def err_tab_check(data):
	err_message = {}
	err_message["product_name"] = \
			only_required(data["product_name"],"Product Name")
	err_message["sku"] = \
			only_required(data["product_code"],"SKU")
	err_message["food_type"] = \
				validation_master_anything(str(data["food_type"]),
				"Food Type",contact_re, 1)
	if len(data["tax_association"]) == 0:
		err_message["tax_association"] = gettext_lazy("No Taxes are associated!!")
	else:
		for i in data["tax_association"]:
			err_message["tax_association"] = \
			validation_master_anything(str(i),"Tax", contact_re,1)
			if err_message["tax_association"] == None:
				pass
			else:
				break 
	if any(err_message.values())==True:
		err = {
			"success": False,
			"error" : err_message,
			"message" : "Please correct listed errors!!"
			}
		return err
	else:
		return None


def unique_record_tab_check(data, Company_id):
	err_message = {}
	if "id" in data:
		name_check = Product.objects.filter(~Q(id=data["id"]),\
						Q(product_name=data["product_name"]),Q(Company_id=Company_id))
	else:
		name_check = Product.objects.filter(Q(product_name=data["product_name"]),Q(Company_id=Company_id))
	if name_check.count() != 0:
		err_message["priority_check"] = gettext_lazy("Product name is already exist!!")
	else:
		pass
	tax_check = TaxSetting.objects.filter(active_status=1)
	if tax_check.count() == 0:
		err_message["tax_association"] = \
			gettext_lazy("Tax is not configured at super-admin level!!")
	else:
		pass
	for q in data["tax_association"]:
		check = tax_check.filter(id=q)
		if check.count() == 1:
			pass
		else:
			err_message["tax_association"] = \
			"Tax is not valid!!"
			break
	if any(err_message.values())==True:
		err = {
			"success": False,
			"error" : err_message,
			"message" : "Please correct listed errors!!"
			}
		return err
	else:
		return None


def err_tab1_check(data):
	err_message = {}
	if data["has_variant"] == "true":
		data["has_variant"]= 1
	else:
		data["has_variant"]= 0
	if data["has_variant"] == 0 or data["has_variant"] == 1:
		pass
	else:
		err_message["has_variant"] = "Has variant flag is not set!!"
	if data["has_variant"] == 0:
		if data['price'] == '':
			pass
		else:
			if float(data['price']) < 0:
				err_message["price"] = "Price is not valid!!"
		data["variant_deatils"] = None
		try:
			data["price"] = float(data["price"])
			if data['discount_price'] == '' or data['discount_price'] == 'null':
				data["discount_price"] = 0
			else:
				data["discount_price"] = float(data["discount_price"])
		except Exception as e:
			err_message["price"] = "Price  value is not valid!!"
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
				if float(i['price']) < 0:
					err_message["price"] = "Variant price is not valid!!"
				try:
					i["price"] = float(i["price"])
					if i['discount_price'] == '':
						i['discount_price'] = 0
					else:
						i["discount_price"] = float(i["discount_price"])
				except Exception as e:
					err_message["varinat_price"] = \
					"Variant Price value is not valid!!"
					break
		else:
			err_message["variant_detail"] = \
					"Variant Price and name value is not set!!"
	if any(err_message.values())==True:
		err = {
			"success": False,
			"error" : err_message,
			"message" : "Please correct listed errors!!"
			}
		return err
	else:
		return None


def unique_record_tab1_check(data, Company_id):
	err_message = {}
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
	if data["variant_deatils"] == None:
		pass
	else:
		for i in data["variant_deatils"]:			
			v_check = Variant.objects.filter(variant=i["name"],Company=Company_id, active_status=1)
			if v_check.count()==0:
				err_message["variant_deatils"] = "Variant is not valid or active!!"
				break
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





def err_tag_check(data):
	err_message = {}
	if len(data["tags"]) == 0:
		pass
	else:
		for i in data["tags"]:
			err_message["tags"] = \
			validation_master_anything(str(i),"Tag", contact_re,1)
			if err_message["tags"] == None:
				pass
			else:
				break 
	if len(data["included_platform"]) == 0:
		pass
	else:
		for i in data["included_platform"]:
			if i != "swiggy" and i != "zomato":
				err_message["included_platform"] = \
				"Invalid plateform is supplied!!"
				break
			else:
				pass
	if data["is_recommended"] != "true" and data["is_recommended"] != "false":
		err_message["is_recommended"] = \
		"Recommended flag is not set!!"
	else:
		pass
	data12 = data["primaryIngredient_deatils"] 
	parient_unique_list = []
	if len(data12) != 0:
		for i in data12:
			if "unit" in i and  "unitValue" in i and "pingredient" in i:
				pass
			else:
				err_message["parient_detail"] = \
				"PrimaryIngredient,unit and unit value is not set!!"
				break	
			if i["pingredient"] not in parient_unique_list:
				parient_unique_list.append(i["pingredient"])
			else:
				err_message["duplicate_ingredient"] = "PrimaryIngredient are duplicate!!"
				break
			err_message["unit"] = 	only_required(i["unitValue"],"Unit Value")
			ch_v = i['unitValue'].find('.')
			if ch_v == 1:
				st = i['unitValue'].split('.')
				if len(st[1]) > 3:
					err_message["unit"] = 	"Only upto 3 decimal unit value allow!!"
			else:
				print("r")
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

def err_image_check(data):
	err_message = {}
	if type(data["product_video"]) != str:
		im_name_path =  data["product_video"].file.name
		im_size = os.stat(im_name_path).st_size
		if im_size > 100000000*1024:
			err_message["image_size"] = "Video can'nt excced the size more than 500kb!!"
	else:
		if data["product_video"] != "":
			pass
		else:
			data["product_video"] = None
	if any(err_message.values())==True:
		err = {
			"success": False,
			"error" : err_message,
			"message" : "Please correct listed errors!!"
			}
		return err
	else:
		return None