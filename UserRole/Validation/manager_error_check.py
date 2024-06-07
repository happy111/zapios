import re
import os
from ZapioApi.api_packages import *
from UserRole.models import UserType
from django.db.models import Q
from django.db.models import Max
from UserRole.models import ManagerProfile
from django.contrib.auth.models import User
from Outlet.models import *

 # Validation check
def err_check(data):
	err_message = {}
	if len(data["outlet"]) != 0:
		outlet_unique_list = []
		for i in data["outlet"]:
			err_message["outlet_map"] = \
				validation_master_anything(str(i),
				"Outlet",contact_re, 1)
			if err_message["outlet_map"] != None:
				break
			if i not in outlet_unique_list:
				outlet_unique_list.append(i)
			else:
				pass
			record_check = OutletProfile.objects.filter(Q(id=i))
			if record_check.count() == 0:
				err_message["outlet"] = \
				"Outlet is not valid!!"
				break
	else:
		err_message["outlet"] = "Please Enter Outlet ID"
	err_message["username"] = \
			only_required(data["username"],"Username")
	if "id" in data:
		err_message["id"] = \
			validation_master_anything(data["id"],"Manager Id", contact_re,1)
	else:
		pass
	err_message["user_type"] = \
			validation_master_anything(str(data["user_type"]),"User Type", contact_re,1)
	err_message["first_name"] = \
			only_required(data["first_name"],"Name")
	err_message["password"] =  only_required(data["password"],"Password")
	
	err_message["mobile"] = validation_master_exact(
		data["mobile"], "Mobile No.", contact_re, 11
	)
	try:
		data['compensation'] = float(data['compensation'])
		if data['compensation'] > 0:
			pass
		else:
			err_message['compensation'] = "Please enter valid compensation rate!!"
	except:
		pass
	try:
		data['km'] = float(data['km'])
		if data['km'] > 0:
			pass
		else:
			err_message['km'] = "Please enter valid km!!"
	except:
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


def record_integrity_check(data,auth_id,cid):
	err_message = {} 
	if "id" in data:
		pass
	else:
		user_already_exist = User.objects.filter(username=data["auth_username"])
		if user_already_exist.count()==1:
			err_message = {}
			err_message["duplicate"] = \
			"User with the entered username already exists..Please try other!!"
		else:
			pass
	if "id" in data:
		unique_check = ManagerProfile.objects.filter(~Q(id=data["id"]),\
			Q(username=data["username"]))
	else:
		unique_check = ManagerProfile.objects.filter(Q(username=data["username"]))
	if unique_check.count() != 0:
		err_message["username"] = "This user name is already assigned to someone else!!"
	else:
		pass
	
	if "id" in data:
		unique_check = ManagerProfile.objects.filter(~Q(id=data["id"]),\
			Q(mobile=data["mobile"]),Q(Company_id=cid))
	else:
		unique_check = ManagerProfile.objects.filter(Q(mobile=data["mobile"]),Q(Company_id=cid))
	if unique_check.count() != 0:
		err_message["mobile"] = "Mobile number already exists!!"
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