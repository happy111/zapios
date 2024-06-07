import re
import os
from ZapioApi.api_packages import *
from django.db.models import Q
from urbanpiper.models import OutletSync

 # Validation check
def err_check(data):
	err_message = {}
	err_message["outlet"] = validation_master_anything(data["outlet_id"],
							"Outlet",contact_re, 1)
	if data["store_status"] == "true":
		pass
	elif data["store_status"] == "false":
		pass
	else:
		err_message["store_status"] = "Status is not valid!!"
	if any(err_message.values())==True:
		err = {
			"success": False,
			"error" : err_message,
			"message" : "Please correct listed errors!!"
			}
		return err
	else:
		return None


def integrity_check(data,company_id):
	err_message = {}
	q = OutletSync.objects.filter(id=data["outlet_id"],company=company_id)
	if q.count() == 0:
		err_message["outlet"] = "Outlet is not valid!!"
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



