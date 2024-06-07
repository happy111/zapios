import re
import os
import dateutil.parser
from ZapioApi.api_packages import *
from django.db.models import Q
from discount.models import Coupon, QuantityCombo, PercentCombo, Product,Discount
from Outlet.models import OutletProfile
from Product.models import ProductCategory
from UserRole.models import UserType
 # Validation check
def coupon_err_check(data):

	err_message = {}
	if type(data['valid_frm']) == str and data['valid_frm'] == '':
		data['valid_frm'] = None
	else:
		pass
	if type(data['valid_till']) == str and data['valid_till'] == '':
		data['valid_till'] = None
	else:
		pass

	if data["valid_till"] != None and data["valid_frm"] != None:
		valid_frm = dateutil.parser.parse(data["valid_frm"])
		valid_till = dateutil.parser.parse(data["valid_till"])
		if valid_frm > valid_till:
			err_message["from_till"] = \
				"Validity dates are not valid!!"
		now = datetime.now().date()
		if valid_frm.date() < now:
			err_message["from"] = \
				"Please provide meaningfull date!!" 

	if data["discount_type"] == "Flat":
		err_message["flat_discount"] = \
			only_required(data["flat_discount"],"Flat Discount")
	else:
		err_message["flat_percentage"] = \
			only_required(data["flat_percentage"],"Flat Percentage")
	err_message["discount_type"] = \
			validation_master_anything(data["discount_type"],
			"Discount Type",username_re, 3)

	err_message["discount_name"] = \
			validation_master_anything(data["discount_name"],
			"Discount Name",username_re, 3)

	if len(data["product_map"]) != 0:
		product_unique_list = []
		for i in data["product_map"]:
			err_message["product_map"] = \
				validation_master_anything(str(i),
				"Product",contact_re, 1)
			if err_message["product_map"] != None:
				break
			if i not in product_unique_list:
				product_unique_list.append(i)
			else:
				err_message["duplicate_product"] = "Products are duplicate!!"
				break
			record_check = Product.objects.filter(Q(id=i),Q(active_status=1))
			if record_check.count() == 0:
				err_message["product_map"] = \
				"Product is not valid!!"
				break
	else:
		pass

	if len(data["user_roll"]) != 0:
		user_unique_list = []
		for i in data["user_roll"]:
			err_message["user_roll"] = \
				validation_master_anything(str(i),
				"User Type",contact_re, 1)
			if err_message["user_roll"] != None:
				break
			if i not in user_unique_list:
				user_unique_list.append(i)
			else:
				err_message["duplicate_userType"] = "User Roll are duplicate!!"
				break
			record_check = UserType.objects.filter(Q(id=i),Q(active_status=1))
			if record_check.count() == 0:
				err_message["user_roll"] = \
				"User Type is not valid!!"
				break
	else:
		err_message["user_roll"] = "Please Enter User Type"



	if len(data["category_map"]) != 0:
		category_unique_list = []
		for i in data["category_map"]:
			err_message["category_map"] = \
				validation_master_anything(str(i),
				"Category",contact_re, 1)
			if err_message["category_map"] != None:
				break
			if i not in category_unique_list:
				category_unique_list.append(i)
			else:
				err_message["duplicate_category"] = "Categorys are duplicate!!"
				break
			record_check = ProductCategory.objects.filter(Q(id=i),Q(active_status=1))
			if record_check.count() == 0:
				err_message["category_map"] = \
				"Category is not valid!!"
				break
	else:
		pass

	if len(data["outlet_id"]) != 0:
		outlet_unique_list = []
		for i in data["outlet_id"]:
			err_message["outlet_map"] = \
				validation_master_anything(str(i),
				"Outlet",contact_re, 1)
			if err_message["outlet_map"] != None:
				break
			if i not in outlet_unique_list:
				outlet_unique_list.append(i)
			else:
				err_message["duplicate_outlet"] = "Outlet are duplicate!!"
				break
			record_check = OutletProfile.objects.filter(Q(id=i),Q(active_status=1))
			if record_check.count() == 0:
				err_message["outlet_map"] = \
				"Outlet is not valid!!"
				break
	else:
		pass

	# print("rrrrrrrrrrrr",len(data['category_map'])
	# print("ssssssssssssssss",data['is_all_category'])
	# if len(data["category_map"]) == 0 and data["is_all_category"] == 'False':
	# 	print("dddddddddddd")
	# 	err_message["choose_category"] = "Choose any one field allcategory or category"



	if data["is_min_shop"] == 'true':
		data["is_min_shop"]= 1
	else:
		data["is_min_shop"]= 0


	if data["is_all_category"] == 'true':
		data["is_all_category"]= 1
	else:
		data["is_all_category"]= 0

	if data["is_all_product"] == 'true':
		data["is_all_product"]= 1
	else:
		data["is_all_product"]= 0

	if data["is_min_shop"] == 0 or data["is_min_shop"] == 1:
		pass
	else:
		err_message["is_min_shop"] = \
		"Is min shop flag is not set!!"
	if data["is_banner"] == 'true':
		data["is_banner"]= 1
	else:
		data["is_banner"]= 0



	if data["is_reason_required"] == 'true':
		data["is_reason_required"]= 1
	else:
		data["is_reason_required"]= 0

	if data["is_reason_required"] == 0 or data["is_reason_required"] == 1:
		pass
	else:
		err_message["is_reason_required"] = \
		"Is Reason Required flag is not set!!"

	if data["is_min_shop"] == 1:
		err_message["min_shoping"] = \
		validation_master_anything(data["min_shoping"],"Minimum shopping amount",
				contact_re,1)
		err_message["max_shoping"] = \
		validation_master_anything(data["max_shoping"],"Maximum shopping amount",
				contact_re,1)
		if err_message["min_shoping"] == None and err_message["max_shoping"] == None:
			if float(data["min_shoping"]) > float(data["max_shoping"]):
				err_message["min_max_value"] = "Minimum & Maximum amount is not valid!!"
			else:
				pass
		else:
			pass
	else:
		data["min_shoping"] = 0.0
		data["max_shoping"] = 0.0

	if any(err_message.values())==True:
		err =	{
				"success": False,
				"error" : err_message,
				"message" : "Please correct listed errors!!"
				}
		return err
	else:
		return None
