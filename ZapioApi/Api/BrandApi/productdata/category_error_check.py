import re
import os
from ZapioApi.api_packages import *
from django.db.models import Q
from django.db.models import Max

def err_check(data):
	err_message = {}
	if len(data["cat_id"]) == 0:
		pass
	else:
		for i in data["cat_id"]:	
			err_message["cat_id"] = \
					validation_master_anything(str(i),"Category ID", contact_re,1)
			if err_message["cat_id"] == None:
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


