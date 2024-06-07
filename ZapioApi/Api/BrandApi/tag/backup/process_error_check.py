import re
import os
from ZapioApi.api_packages import *
from Product.models import FoodType, Product, ProductCategory, ProductsubCategory,\
	AddonDetails
from django.db.models import Q
from Outlet.models import OutletProfile
from django.db.models import Max
from kitchen.models import Ingredient,StepToprocess

 # Validation check
def err_check(data):
	err_message = {}
	if type(data["image"]) != str:
		im_name_path =  data["image"].file.name
		im_size = os.stat(im_name_path).st_size
		if im_size > 500*1024:
			err_message["image_size"] = "Product Process image can'nt excced the size more than 500kb!!"
	else:
		if data["image"] != "":
			pass
		else:
			data["image"] = None
	ingrediate_list = []
	if len(data["ingrediate"]) != 0:
		for i in data["ingrediate"]:
			if "name" in i and  "unit" in i and "quantity" in i and "id" in i:
				pass
			else:
				err_message["ingrediate"] = \
				"Ingredient name, unit or quantity value is not set!!"
				break	
			if i["name"] not in ingrediate_list:
				ingrediate_list.append(i["name"])
			else:
				err_message["duplicate_ingrediate"] = "Ingredient are duplicate!!"
				break
			err_message["ingrediate_name"] = \
			validation_master_anything(i["name"],"Ingredient name",
			username_re,3)
			if err_message["ingrediate_name"]!=None:
				break
			err_message["unit"] = \
			validation_master_anything(i["unit"],"Ingredient unit",
			alpha_re,2)
			if err_message["unit"]!=None:
				break
			err_message["quantity"] = \
			validation_master_anything(i["quantity"],"Quantity",
			lat_long_re,1)
			if err_message["quantity"]!=None:
				break
	else:
		pass
	err_message["product"] =\
				validation_master_anything(str(data["product"]),
					"Product",contact_re, 1)
	err_message["varient"] =\
				validate_anything(str(data["varient"]),contact_re,
					zero__re,1,"Variant")
				# validation_master_anything(str(data["varient"]),
				# 	"Variant",contact_re, 1)
	err_message["step"] = \
				validation_master_anything(str(data["step"]),
				"Process Step",contact_re, 1)
	err_message["process"] = \
			validation_master_anything(data["process"],
			"Process name",product_re, 3)
	err_message["description"] = \
		validate_anything(data["description"], product_re, 
			zero__re,3, "Process Desription")
	err_message["time_of_process"] = \
				validation_master_anything(str(data["time_of_process"]),
				"Time Of Process",contact_re, 1)
	if any(err_message.values())==True:
		err = {
			"success": False,
			"error" : err_message,
			"message" : "Please correct listed errors!!"
			}
		return err
	else:
		return None


def unique_record_check(data,auth_id):
	err_message = {}
	step_check = StepToprocess.objects.filter(Q(step=int(data["step"])),Q(product=int(data['product']))\
						,Q(company__auth_user=auth_id))
	if data['varient'] != "":
		step_check = step_check.filter(Q(varient=data['varient']))
	else:
		pass
	if "id" in data:
		step_check = step_check.filter(~Q(id=data["id"]))
	else:
		pass
	if step_check.count() != 0:
		# step_check.last().step
		avail_step = step_check.aggregate(Max('step'))
		suggestion = avail_step['step__max'] + 1
		err_message["priority_check"] = \
		"This step is already associated to other process..Next available step is "+str(suggestion)+\
		" !!"
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