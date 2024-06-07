import re
import os
from ZapioApi.api_packages import *
from UserRole.models import UserType
from django.db.models import Q
from Outlet.models import OutletProfile
from django.db.models import Max

 # Validation check
def err_check(data):
	err_message = {}
	err_message["user_type"] =  only_required(data["user_type"],"User Type")


	if "id" in data:
		err_message["id"] = \
			validation_master_anything(data["id"],"User Type Id", contact_re,1)
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


def record_integrity_check(data,auth_id,cid):
	err_message = {}
	if "id" in data:
		unique_check = UserType.objects.filter(~Q(id=data["id"]),\
			Q(user_type=data["user_type"]), Q(Company__auth_user=auth_id))
	else:
		unique_check = UserType.objects.filter(Q(user_type=data["user_type"]), \
			Q(Company__auth_user=auth_id))
	if unique_check.count() != 0:
		err_message["user_type"] = "This user type is already created!!"
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