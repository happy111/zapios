import re
import os
import dateutil.parser
from ZapioApi.api_packages import *
from django.db.models import Q
from discount.models import Coupon, QuantityCombo, PercentCombo, Product
from Outlet.models import OutletProfile

 # Validation check
def discount_err_check(data):
	err_message = {}
	err_message["valid_till"] = \
			only_required(data["valid_till"],"Valid Till")
	err_message["valid_frm"] = \
			only_required(data["valid_frm"],"Valid From")
	if err_message["valid_till"] == None and err_message["valid_frm"] == None:
		valid_frm = dateutil.parser.parse(data["valid_frm"])
		valid_till = dateutil.parser.parse(data["valid_till"])
		if valid_frm > valid_till:
			err_message["from_till"] = \
				"Validity dates are not valid!!"
		now = datetime.now().date()
		if valid_frm.date() < now:
			err_message["from"] = \
				"Please provide meaningfull date!!" 
	if data["coupon_type"] == "Flat":
		err_message["flat_discount"] = \
			only_required(data["flat_discount"],"Flat Discount")
	else:
		err_message["flat_percentage"] = \
			only_required(data["flat_percentage"],"Flat Percentage")
	err_message["coupon_type"] = \
			validation_master_anything(data["coupon_type"],
			"Coupon Type",username_re, 3)
	err_message["coupon_code"] = \
			validation_master_anything(data["coupon_code"],
			"Coupon code", username_re, 3)
	err_message["category"] = \
			validate_anything(data["category"], contact_re, zero__re, 1, "Category")
	err_message["frequency"] = \
			validation_master_anything(data["frequency"],"Frequency",
				contact_re,1)
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
			record_check = Product.objects.filter(Q(id=str(i)),Q(active_status=1))
			if record_check.count() == 0:
				err_message["product_map"] = \
				"Product is not valid!!"
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
	if data["is_min_shop"] == 'true':
		data["is_min_shop"]= 1
	else:
		data["is_min_shop"]= 0
	if data["is_min_shop"] == 0 or data["is_min_shop"] == 1:
		pass
	else:
		err_message["is_min_shop"] = \
		"Is min shop flag is not set!!"
	if data["is_automated"] == 'true':
		data["is_automated"]= 1
	else:
		data["is_automated"]= 0
	
	if data["is_banner"] == 'true':
		data["is_banner"]= 1
	else:
		data["is_banner"]= 0

	if data["is_automated"] == 0 or data["is_automated"] == 1:
		pass
	else:
		err_message["is_automated"] = \
		"Is automated flag is not set!!"
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
	print("aaaaaaaaaaa")
	unique_check = Coupon.objects.filter(coupon_code__iexact=data["coupon_code"],
									Company_id=data["Company"])
	if unique_check.count() != 0 and "id" not in data:
		err_message["unique_check"] = "Coupon with this code already exists!!"
	else:
		pass
	if data["is_min_shop"] == 1:
		if err_message["min_shoping"]==None:
			if int(data["min_shoping"]) > 10000:
				err_message["valid_min_shoping"] = \
				"Minimum shopping is not set in valid manner!!"
		else:
			pass
		if err_message["max_shoping"]==None:
			if int(data["max_shoping"]) > 10000:
				err_message["valid_max_shoping"] = \
				"Maximum shopping is not set in valid manner!!"
		else:
			pass
	else:
		pass
	if any(err_message.values())==True:
		err =	{
				"success": False,
				"error" : err_message,
				"message" : "Please correct listed errors!!"
				}
		return err
	else:
		return None
