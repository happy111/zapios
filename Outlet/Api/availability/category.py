from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from Product.models import Product, Product_availability, Category_availability, ProductCategory
from ZapioApi.api_packages import *
from Outlet.models import OutletProfile
import re
from _thread import start_new_thread

def cat_product_sync(cat_id, auth_id, status):
	mapped_product = Product.objects.filter(product_category=cat_id)
	outlet_id = OutletProfile.objects.get(auth_user=auth_id)
	avail_product = Product_availability.objects.filter(outlet__auth_user=auth_id)
	if avail_product.count() != 0:
		pass
	else:
		avail_product_create = Product_availability.objects.create(outlet=outlet_id,available_product=[])
	avail_product = Product_availability.objects.filter(outlet__auth_user=auth_id)
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



class Category(APIView):
	"""
	Category availability Post API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to make Category available or unavailable within outlet.

		Data Post: {
			"is_available"  : False,
			"id"            : "1"
		}

		Response: {

			"success": True, 
			"message": "Category is unavailable now!!",

		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			data["id"] = str(data["id"])
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
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			user_id = request.user.id
			product_q = Product_availability.objects.filter(outlet__auth_user=user_id)
			cat_q = Category_availability.objects.filter(outlet__auth_user=user_id)
			if cat_q.count() == 0:
				return Response({
					"success": False,
					"message" : "No product are mapped with this outlet!!"
					})
			else:
				start_new_thread(cat_product_sync, (data["id"],user_id, data["is_available"]))
				cat_ids = cat_q[0].available_cat
				if data["id"] in cat_ids and data["is_available"] == False:
					cat_ids.remove(data["id"])
					cat_q.update(available_cat=cat_ids)
					msg_info = "Category is unavailable now!!"
				else:
					pass
				if data["id"] not in cat_ids and data["is_available"] == True:
					cat_ids.append(data["id"])
					cat_q.update(available_cat=cat_ids)
					msg_info = "Category is available now!!"
				else:
					pass
				return Response({
								"success":True,
								"message":msg_info
								 })
		except Exception as e:
			print("Outletwise Category availability Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})