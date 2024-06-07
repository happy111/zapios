import re
import os
from ZapioApi.api_packages import *
from django.db.models import Q
from urbanpiper.models import OutletSync

 # Validation check
def err_check(data):
	err_message = {}
	ids = data["outlet_ids"]
	if len(ids) != 0:
		for i in ids: 
			err_message["outlet"] = \
							validation_master_anything(str(i),
							"Outlet",contact_re, 1)
			if err_message["outlet"] == None:
				pass
			else:
				break
	else:
		err_message["outlet"] = "Please select at least one outlet to sync!!"
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
	ids = data["outlet_ids"]
	for i in ids:
		q = OutletSync.objects.filter(outlet=i,company=company_id)
		if q.count() == 0:
			err_message["outlet"] = "Outlet is not valid!!"
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



