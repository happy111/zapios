import re
import os
from ZapioApi.api_packages import *
from Product.models import FoodType, Product, ProductCategory, ProductsubCategory,\
	AddonDetails,Tag, FeatureProduct
from django.db.models import Q
from Outlet.models import OutletProfile
from django.db.models import Max

 # Validation check
def err_check(data):
	err_message = {}
	if len(data["feature_product"]) == 0:
		err_message["info"] = "Please select at least one Featured Product"
	else:
		pass
	if len(data["feature_product"]) > 5:
		err_message["info"] = "You can select upto 5 products only!!"
	else:
		feature = []
		for i in data["feature_product"]:
			if i not in feature:
				feature.append(i)
			else:
				err_message["duplicate_feature_product"] = "Selected Product are duplicate!!"
				break
	err_message["outlet"] = \
			validation_master_anything(str(data["outlet"]),"Outlet", contact_re,1)
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
	if "id" in data:
		unique_check = FeatureProduct.objects.filter(~Q(id=data["id"]),\
			Q(outlet_id=data["outlet"]))
	else:
		unique_check = FeatureProduct.objects.filter(Q(outlet_id=data["outlet"]))
	if unique_check.count() != 0:
		err_message["outlet_check"] = "This outlet is already associated with some other featured products!!"
	else:
		pass
	product_check = Product.objects.filter(active_status=1)
	if len(data["feature_product"]) != 0:
		for q in data['feature_product']:
			check = product_check.filter(id=q)
			if check.count() == 1:
				pass
			else:
				err_message["feature_product"] = \
				"Product is not valid..Please check!!"
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