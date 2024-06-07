from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from Product.models import Product, Product_availability, Category_availability, ProductCategory
from ZapioApi.api_packages import *
import re


class Productavail(APIView):
	"""
	Product availability Post API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to make products available or unavailable within outlet.

		Data Post: {
			"is_available"  : False,
			"id"            : "1"
		}

		Response: {

			"success": True, 
			"message": "Product is unavailable now!!",

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
			err_message["product"] =\
				validation_master_anything(data["id"],
					"Product",contact_re, 1)
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
				mapped_cat_id = Product.objects.filter(id=data["id"])[0].product_category_id
				cat_ids = cat_q[0].available_cat
				if str(mapped_cat_id) in cat_ids:
					product_ids = product_q[0].available_product
					if data["id"] in product_ids and data["is_available"] == False:
						product_ids.remove(data["id"])
						product_q.update(available_product=product_ids)
						msg_info = "Product is unavailable now!!"
					else:
						pass
					if data["id"] not in product_ids and data["is_available"] == True:
						product_ids.append(data["id"])
						product_q.update(available_product=product_ids)
						msg_info = "Product is available now!!"
					else:
						pass
					return Response({
									"success":True,
									"message":msg_info
									 })
				else:
					return Response({
									"success":True,
									"message":"The mapped category with this product is not available for now!!"
									 })
		except Exception as e:
			print("Outletwise Product availability Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})