import re
import os
from ZapioApi.api_packages import *
from UserRole.models import UserType, MainRoutingModule, RoutingModule, SubRoutingModule
from django.db.models import Q
from django.db.models import Max

 # Validation check
def err_check(data):
	err_message = {}
	if len(data["main_routes"]) == 0:
		err_message["main_routes"] = "Please select at least one main module!"
	else:
		pass
	for i in data["main_routes"]:	
		err_message["main_routes"] = \
				validation_master_anything(str(i),"Main Module", contact_re,1)
		if err_message["main_routes"] == None:
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


def record_integrity_check(data):
	err_message = {} 
	main_routes = data["main_routes"]
	for i in main_routes:
		q = MainRoutingModule.objects.filter(id=i)
		if q.count() == 0:
			err_message["valid_check"] = "Provided info is not valid!!"
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