from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from Product.models import Product, Product_availability, Category_availability, ProductCategory
from ZapioApi.api_packages import *
import re
from ZapioApi.Api.BrandApi.outletmgmt.availability.available import *
from _thread import start_new_thread


def ProductAvailable(data,user):
	data["id"] = str(data["id"])
	err_message = {}
	if data["is_available"] == True:
		pass
	elif data["is_available"] == False:
		pass
	else:
		err_message["is_available"] = \
		"Availability flag is not set!!"
	err_message["product"] =\
		validation_master_anything(data["id"],
			"Product",contact_re, 1)
	if any(err_message.values())==True:
		return Response({
			"success": False,
			"error" : err_message,
			"message" : "Please correct listed errors!!"
			})
	product_q = Product_availability.objects.filter(outlet=data["outlet"])
	cat_q = Category_availability.objects.filter(outlet=data["outlet"])
	if cat_q.count() == 0:
		return Response({
			"success": False,
			"message" : "No categories are mapped with this outlet!!"
			})
	else:
		pass
	if product_q.count() == 0:
		return Response({
			"success": False,
			"message" : "No product are mapped with this outlet!!"
			})
	else:
		mapped_cat_id = Product.objects.filter(id=data["id"])[0]
		product_category_id = mapped_cat_id.product_categorys
		cat_ids = cat_q[0].available_cat
		if len(cat_ids) > 0:
			for p in product_category_id:
				print(p)
				if p in cat_ids:
					product_ids = product_q[0].available_product
					

					if data["id"] in product_ids and data["is_available"] == False:
						product_ids.remove(data["id"])
						product_q.update(available_product=product_ids)
						err = {
								"success":True,
								"message":"Product is unavailable now!!"
								 }
						return err
					else:
						pass
					if data["id"] not in product_ids and data["is_available"] == True:
						product_ids.append(data["id"])
						product_q.update(available_product=product_ids)
						err = {
							"success":True,
							"message":"Product is available now!!"
						  }
						return err
					else:
						err = {
							"success":True,
							"message":"Product is available now!!"
						  }
						return err
				else:
					err = {
					"success":True,
					"message":"The mapped category with this product is not available for now!!"
				  }
		else:
			err = {
				"success": False,
				"message" : "No category are mapped with this outlet!!"
			}

		# if str(mapped_cat_id) in cat_ids:
		# 	product_ids = product_q[0].available_product
		# 	if data["id"] in product_ids and data["is_available"] == False:
		# 		product_ids.remove(data["id"])
		# 		product_q.update(available_product=product_ids)
		# 		err = {
		# 					"success":True,
		# 					"message":"Product is unavailable now!!"
		# 					 }
		# 		return err
		# 	else:
		# 		pass
		# 	if data["id"] not in product_ids and data["is_available"] == True:
		# 		product_ids.append(data["id"])
		# 		product_q.update(available_product=product_ids)
		# 		err = {
		# 				"success":True,
		# 				"message":"Product is available now!!"
		# 			  }
		# 		return err
		# 	else:
		# 		pass
		# else:
		# 	err = {
		# 			"success":True,
		# 			"message":"The mapped category with this product is not available for now!!"
		# 		  }
		return err


def cat_product_sync(cat_id, outlet_id, status):
	mapped_product = Product.objects.filter(product_categorys__exact=[cat_id],active_status=1,is_hide=0)
	avail_product = Product_availability.objects.filter(outlet_id=outlet_id)
	if avail_product.count() != 0:
		pass
	else:
		avail_product_create = Product_availability.objects.create(outlet_id=outlet_id,available_product=[])
	avail_product = Product_availability.objects.filter(outlet_id=outlet_id)
	map_product_ids = avail_product[0].available_product
	product_ids = []
	for i in mapped_product:
		product_ids.append(str(i.id))
	if status == False:
		for i in product_ids:
			if i in map_product_ids:
				map_product_ids.remove(i)
			else:
				pass		
	else:
		for i in product_ids:
			if i not in map_product_ids:
				map_product_ids.append(i)
			else:
				pass
	avail_product.update(available_product=map_product_ids)
	return "Category & Products are synchronized!!"



def CategoryAvailable(data,user):
	data["id"] = str(data["id"])
	data["outlet"] = str(data["outlet"])
	err_message = {}
	if data["is_available"] == True:
		pass
	elif data["is_available"] == False:
		pass
	else:
		err_message["is_available"] = \
		"Availability flag is not set!!"
	err_message["Category"] =\
		validation_master_anything(data["id"],
			"Category",contact_re, 1)
	err_message["outlet"] =\
		validation_master_anything(data["outlet"],
			"Outlet",contact_re, 1)
	if any(err_message.values())==True:
		err = {
			"success": False,
			"error" : err_message,
			"message" : "Please correct listed errors!!"
			}
		return err
	product_q = Product_availability.objects.filter(outlet=data["outlet"])
	cat_q = Category_availability.objects.filter(outlet=data["outlet"])
	if cat_q.count() == 0:
		err = {
			"success": False,
			"message" : "No product are mapped with this outlet!!"
			}
		return err
	else:
		start_new_thread(cat_product_sync, (data["id"],data["outlet"], data["is_available"]))
		cat_ids = cat_q[0].available_cat
		if data["id"] in cat_ids and data["is_available"] == False:
			cat_ids.remove(data["id"])
			cat_q.update(available_cat=cat_ids)
			err = {
						"success":True,
						"message":"Category is unavailable now!!"
					  }
			return err
		else:
			pass
		if data["id"] not in cat_ids and data["is_available"] == True:
			cat_ids.append(data["id"])
			cat_q.update(available_cat=cat_ids)
			err = {
						"success":True,
						"message":"Category is available now!!"
					  }
			return err
		else:
			pass

