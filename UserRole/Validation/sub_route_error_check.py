import re
import os
from ZapioApi.api_packages import *
from UserRole.models import UserType, MainRoutingModule, RoutingModule, SubRoutingModule
from django.db.models import Q

 # Validation check
def err_check(data):
	err_message = {}
	if len(data["routes"]) == 0:
		err_message["routes"] = "Please select at least one module!"
	else:
		pass
	for i in data["routes"]:	
		err_message["routes"] = \
				validation_master_anything(str(i),"Module", contact_re,1)
		if err_message["routes"] == None:
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
	main_routes = data["routes"]
	for i in main_routes:
		q = RoutingModule.objects.filter(id=i)
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