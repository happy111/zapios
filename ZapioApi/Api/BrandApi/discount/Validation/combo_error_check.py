import re
import os
import dateutil.parser
from ZapioApi.api_packages import *
from django.db.models import Q
from Outlet.models import OutletProfile
from django.db.models import Max
from discount.models import Coupon, QuantityCombo, PercentCombo

 # Validation check
def quantity_err_check(data):
	err_message = {}
	if data["valid_till"] != "" and data["valid_frm"] != "":
		valid_frm = dateutil.parser.parse(data["valid_frm"])
		valid_till = dateutil.parser.parse(data["valid_till"])
		if valid_frm > valid_till:
			err_message["from_till"] = \
				"Validity dates are not valid!!"
		now = datetime.now().date()
		print("ssssssssss",valid_frm.date())

		print("qqqqqqqqqqqqq",now)


		if valid_frm.date() < now:
			err_message["from"] = \
				"Please provide meaningfull date!!" 
		else:
			pass
	else:
		pass
	err_message["product"] = \
			validation_master_anything(data["product"],
			"Product",contact_re, 1)
	err_message["free_product"] = \
			validation_master_anything(data["free_product"],
			"Free Product", contact_re, 1)
	err_message["product_quantity"] = \
			validation_master_anything(data["product_quantity"],"Product quantity",
				contact_re,1)
	err_message["free_pro_quantity"] = \
			validation_master_anything(data["free_pro_quantity"],"Free product quantity",
				contact_re,1)
	err_message["valid_till"] = \
			only_required(data["valid_till"],"Valid Till")
	err_message["valid_frm"] = \
			only_required(data["valid_frm"],"Valid From")
	if data["product_quantity"] != "":
		if int(data["product_quantity"]) > 10000:
			err_message["valid_product_quantity"] = \
			"Product quantity is not set in valid manner!!"
	else:
		pass
	if data["free_pro_quantity"] != "":
		if int(data["free_pro_quantity"]) > 10000:
			err_message["valid_free_pro_quantity"] = \
			"Free product quantity is not set in valid manner!!"
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


 # Validation check
def percentage_err_check(data):
	err_message = {}
	if data["valid_till"] != "" and data["valid_frm"] != "":
		valid_frm = dateutil.parser.parse(data["valid_frm"])
		valid_till = dateutil.parser.parse(data["valid_till"])
		if valid_frm > valid_till:
			err_message["from_till"] = \
				"Validity dates are not valid!!"
		now = datetime.now().date()
		if valid_frm.date() < now:
			err_message["from"] = \
				"Please provide meaningfull date!!" 
	else:
		pass
	err_message["product"] = \
			validation_master_anything(data["product"],
			"Product",contact_re, 1)
	err_message["discount_product"] = \
			validation_master_anything(data["discount_product"],
			"Discounted Product", contact_re, 1)
	err_message["discount_percent"] = \
			validation_master_anything(data["discount_percent"],"Discount Percent",
				contact_re,1)
	if err_message["discount_percent"] == None:
		if int(data["discount_percent"]) > 100:
			err_message["percent_value"] = \
			"Discount Percent value is not valid!!"
		else:
			pass
	else:
		pass
	err_message["valid_till"] = \
			only_required(data["valid_till"],"Valid Till")
	err_message["valid_frm"] = \
			only_required(data["valid_frm"],"Valid From")
	if any(err_message.values())==True:
		err =	{
				"success": False,
				"error" : err_message,
				"message" : "Please correct listed errors!!"
				}
		return err
	else:
		return None