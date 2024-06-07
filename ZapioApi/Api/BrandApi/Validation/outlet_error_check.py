import re
from ZapioApi.api_packages import *
from Outlet.models import OutletProfile
import os

 # Validation check
def err_check(data):
	print("eeeeeeeeeeeeeeeeeee",data['pincode'])
	err_message = {}
	err_message["Outletname"] = \
			only_required(data["Outletname"],"Outletname")
	err_message["address"] = \
			only_required(data["address"],"Google location")
	err_message["country"] = \
			only_required(data["country"],"Country")
	err_message["prefecture"] = \
			only_required(data["prefecture"],"prefecture")
	err_message["pincode"] = \
			validation_master_anything(data["pincode"],"Pincode",
			pincode,7)
	err_message["address"] = \
			only_required(data["address"],"Outlet Full address")
	# err_message["company_auth_id"] = \
	# 		only_required(data["company_auth_id"],"Company")

	print("wwwwwwwwwwwwwwwwwwwww",err_message)
	if type(data["outlet_image"]) != str:
		im_name_path =  data["outlet_image"].file.name
		im_size = os.stat(im_name_path).st_size
		if im_size > 100*1024:
			err_message["image_size"] = "Outlet image can'nt excced the size more than 100kb!!"
	else:
		data["outlet_image"] = ''
	if any(err_message.values())==True:
		err = {
			"success": False,
			"error" : err_message,
			"message" : "Please correct listed errors!!"
			}
		return err
	else:
		return None


def err_checks(data):
	err_message = {}
	err_message["country"] = \
			only_required(data["country"],"Country")
	err_message["prefecture"] = \
			only_required(data["prefecture"],"Prefecture")
	
	err_message["city"] = \
			only_required(data["city"],"City")


	err_message["pincode"] = \
			validation_master_anything(data["pincode"],"Pincode",
			pincode,7)
			
	if type(data["outlet_image"]) != str:
		im_name_path =  data["outlet_image"].file.name
		im_size = os.stat(im_name_path).st_size
		if im_size > 100*1024:
			err_message["image_size"] = "Outlet image can'nt excced the size more than 100kb!!"
	else:
		data["outlet_image"] = ''

	outlet_id = OutletProfile.objects.filter(id=data['id'])
	if outlet_id.count() > 0:
		pass
	else:
		err_message['outlet_id'] = "Provided Outler data is not valid to retrieve!!"
	if any(err_message.values())==True:
		err = {
			"success": False,
			"error" : err_message,
			"message" : "Please correct listed errors!!"
			}
		return err
	else:
		return None
