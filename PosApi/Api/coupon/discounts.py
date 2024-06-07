from rest_framework.views import APIView
from rest_framework.response import Response
from Product.models import ProductCategory, Product_availability, Category_availability, Product,\
Variant,AddonDetails
from ZapioApi.api_packages import *
from django.db.models import Q
from rest_framework_tracking.mixins import LoggingMixin
import datetime
from discount.models import Coupon
# from frontApi.coupon.coupon_check import *
from rest_framework.permissions import IsAuthenticated
from .coupon_check import *


class CouponcodeView(LoggingMixin,APIView):
	"""
	Coupon Code POST API

		Authentication Required		: yes
		Service Usage & Description	: This Api is used Coupon discount on the basis of provided 
		Coupon code,

		Data Post:   {
						"coupon_code":"3564",
						"outlet":"1",
						"tax":189.5,
						"company":11,
					"cart":[
								{
									"outlet_availbility_id":65,
									"name":"Red Thai Curry Chicken & Rice Bowl",
									"product_id":642,
									"allergen":[
									],
									"company":11,
									"nutrition":[
									],
									"product_rating":4.3,
									"parent_category_id":[
									"77"
									],
									"parent_category_name":[
									{
									"parent_category_name":"Rice Bowl",
									"parent_category_id":"77"
									}
									],
									"tax_detail":[
									{
									"id":22,
									"tax_name":"CGST | 2.5",
									"tax_percent":2.5
									},
									{
									"id":26,
									"tax_name":"SGST | 2.5",
									"tax_percent":2.5
									}
									],
									"subcategory_name":[
									{
									"parent_category_id":"77",
									"category_id":117,
									"category_name":"test"
									}
									],
									"food_type":"Non Vegetarian",
									"food_type_image":"https://zapio-admin.com/media/foodtype_images/images/non-vegetarian_icon.png\t\n",
									"primary_image":"None",
									"multiple_image":[
									],
									"price":364,
									"compare_price":0,
									"addon_detail":[
									{
									"price":99,
									"addon":"Fried Chicken Karage With Spicy Mayo",
									"addon_id":1300
									},
									{
									"price":99,
									"addon":"Healthy Spinach And Beans Gomae Salad",
									"addon_id":1301
									},
									{
									"price":99,
									"addon":"3 Pcs Chicken Dimsums",
									"addon_id":1302
									},
									{
									"price":99,
									"addon":"3 Pcs Veg Dimsums",
									"addon_id":1303
									}
									],
									"is_customize":1,
									"packing_charge":[
									],
									"tag_details":[
									],
									"add_ons":[
									{
									"addon_id":1300,
									"addon_name":"Fried Chicken Karage With Spicy Mayo",
									"price":99
									}
									],
									"tag":[
									],
									"quantity":1,
									"cart_id":"item-1621055821820",
									"tax":189.5,
									"discount":"200",
									"coupon_code":"3564",
									"subTotal":""
								},

							]
			}
		Response: {
				{
					"status": true,
					"subtotalprice": 1396
				}
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data  = request.data
			ccode = data['coupon_code']
			outlet = data['outlet']
			company = data['company']
			today = datetime.datetime.now()
			if ccode !="":
				err_message = {}
				err_message["outlet"] = validation_master_anything(str(outlet),
				"Outlet id",contact_re, 1)
				if any(err_message.values())==True:
					return Response({
						"success": False,
						"error" : err_message,
						"message" : "Please correct listed errors!!"
						})
				query = Coupon.objects.filter(coupon_code__exact=ccode,frequency__gte=1,
							valid_till__gte=today)
				

				if query.count() > 0:

					if len(query[0].outlet_id) > 0:
						query = Coupon.objects.filter(frequency__gte=1,coupon_code__exact=ccode,
								valid_till__gte=today,outlet_id__icontains=str(data["outlet"]))
						
						if query.count() > 0:
							apply_coupon = check_coupon(data,ccode,company)
							

							Old_subtotal =  apply_coupon["Old_subtotal"]
							coupon_applied = apply_coupon["coupon_applied"]
							tdaprice = apply_coupon["tdaprice"]
							if coupon_applied == 1:
								total_tax = calculate_tax(Old_subtotal,tdaprice,data)
							else:
								total_tax = 0
							if coupon_applied == 1:
								return Response({"status":True,
												"Old_subtotal" : Old_subtotal,
												"Discount_value" : tdaprice,
												"Tax" : total_tax
														})
							else:
								return Response({"status":False,
											"message":"Applied coupon code is invalid!!"})
			  
						else:
							return Response({"status":False,
							   "message":"Applied coupon code is not valid for outlet!!"})
					else:
						apply_coupon = check_coupon(data,ccode)
						Old_subtotal =  apply_coupon["Old_subtotal"]
						coupon_applied = apply_coupon["coupon_applied"]
						tdaprice = apply_coupon["tdaprice"]
						
						if coupon_applied == 1:
							total_tax = calculate_tax(Old_subtotal,tdaprice,data)
						else:
							total_tax = 0
						
						if coupon_applied == 1:
							return Response({"status":True,
											"Old_subtotal" : Old_subtotal,
											"Discount_value" : tdaprice,
											"Tax" : total_tax
											})
						else:
							return Response({"status":False,
										"message":"Applied coupon code is invalid!!"})
				else:
					return Response({"status":False,
									"message":"Applied coupon code is invalid!!"})

			else:
				return Response({"status": False, 
								"message": "Coupon Code is not provided!!"})
		except Exception as e:
			print("CoupondataApiException")
			print(e)
			return Response({"status": False, 
							"message": "Bad Request", 
							 "error": str(e)})