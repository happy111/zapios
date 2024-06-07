from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from Product.models import Product, Product_availability,Category_availability,ProductCategory,Tag
from Outlet.models import OutletProfile
from Brands.models import Company
import re
import os
from ZapioApi.api_packages import *
from UserRole.models import * 
from django.db.models import Q
from frontApi.menu.customize_fun import CustomizeProduct
import datetime
from discount.models import Coupon

def ProductAvailableList(data,user):
	err_message = {}
	err_message["outlet"] = \
			validation_master_anything(str(data["outlet"]),
			"Outlet",contact_re, 1)
	if any(err_message.values())==True:
		err = {
			"success": False,
			"error" : err_message,
			"message" : "Please correct listed errors!!"
			}
		return err
	user = user.id
	ch_brand = Company.objects.filter(auth_user_id=user)
	if ch_brand.count() > 0:
		user_id=user
	else:
		pass
	ch_cashier = ManagerProfile.objects.filter(auth_user_id=user)
	if ch_cashier.count() > 0:
		company_id = ch_cashier[0].Company_id
		auth_user_id = Company.objects.filter(id=company_id)[0].auth_user_id
		user_id=auth_user_id
	else:
		pass
	product_q = Product_availability.objects.filter(outlet_id=data["outlet"])
	if product_q.count() > 0:
		company_id = Company.objects.filter(auth_user=user_id)[0].id
		outlet_id = data["outlet"]
		product = Product.objects.filter(active_status=1,Company=company_id,is_hide=0)
		final_result = []
		if product_q.count() == 0:
			for i in product:
				product_dict = {}
				product_dict["id"] = i.id
				product_dict["product_name"] = i.product_name
				product_dict["is_available"] = False
				product_dict["food_type"] = i.food_type.food_type
				product_dict["priority"] = i.priority
				final_result.append(product_dict)	
		else:
			product_ids = product_q[0].available_product
			if len(product_ids) != 0:
				for p in product:
					product_dict = {}
					product_dict["id"] = p.id
					product_dict["product_name"] = p.product_name
					product_dict["food_type"] = p.food_type.food_type
					product_dict["priority"] = p.priority
					if str(p.id) not in product_ids:
						product_dict["is_available"] = False
					else:
						product_dict["is_available"] = True
					final_result.append(product_dict)
			else:
				for i in product:
					product_dict = {}
					product_dict["id"] = i.id
					product_dict["product_name"] = i.product_name
					product_dict["category_id"] = i.product_name
					product_dict["category_name"] = i.product_name
					product_dict["is_available"] = False
					product_dict["food_type"] = i.food_type.food_type
					product_dict["priority"] = i.priority
					final_result.append(product_dict)
		if len(final_result) > 0:
			err = {
				"success":True,
				"message":"Outletwise product listing worked well!!",
				"data":final_result
				}
		else:
			pass
	else:
		err = None
	return err



def CategoryAvailableList(data,user):
	err_message = {}
	err_message["outlet"] = \
			validation_master_anything(str(data["outlet"]),
			"Outlet",contact_re, 1)
	if any(err_message.values())==True:
		err = {
			"success": False,
			"error" : err_message,
			"message" : "Please correct listed errors!!"
			}
		return Response(err)
	outlet = OutletProfile.objects.filter(id=data["outlet"],active_status=1)
	if outlet.count() == 0:
		return None
	else:
		user = user.id
		ch_brand = Company.objects.filter(auth_user_id=user)
		if ch_brand.count() > 0:
			user_id=user
		else:
			pass
		ch_cashier = ManagerProfile.objects.filter(auth_user_id=user)
		if ch_cashier.count() > 0:
			company_id = ch_cashier[0].Company_id
			auth_user_id = Company.objects.filter(id=company_id)[0].auth_user_id
			user_id=auth_user_id
		else:
			pass
		cat_q = Category_availability.objects.filter(outlet_id=data["outlet"])
		company_id = Company.objects.filter(auth_user=user_id)[0].id
		category = ProductCategory.objects.filter(active_status=1,Company=company_id,is_hide=0)
		final_result = []
		if cat_q.count() == 0:
			create_cat_avail = \
			Category_availability.objects.create(outlet_id=data["outlet"],available_cat=[])
			for p in category:
				cat_dict = {}
				cat_dict["id"] = p.id
				cat_dict["category_name"] = p.category_name
				cat_dict["category_code"] = p.category_code
				cat_dict["priority"] = p.priority
				cat_dict["is_available"] = False
				final_result.append(cat_dict)
		else:
			cat_ids = cat_q[0].available_cat
			if len(cat_ids) != 0:
				for p in category:
					cat_dict = {}
					cat_dict["id"] = p.id
					cat_dict["category_name"] = p.category_name
					cat_dict["category_code"] = p.category_code
					cat_dict["priority"] = p.priority
					if str(p.id) not in cat_ids:
						cat_dict["is_available"] = False
					else:
						cat_dict["is_available"] = True
					final_result.append(cat_dict)
			else:
				for p in category:
					cat_dict = {}
					cat_dict["id"] = p.id
					cat_dict["category_name"] = p.category_name
					cat_dict["category_code"] = p.category_code
					cat_dict["priority"] = p.priority
					cat_dict["is_available"] = False
					final_result.append(cat_dict)
	if len(final_result) > 0:
		err = {
			"success":True,
			"message":"Outletwise category listing worked well!!",
			"data":final_result
			}
	else:
		err = None
	return err







