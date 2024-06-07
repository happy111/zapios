from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.sites.shortcuts import get_current_site
from ZapioApi.Api.BrandApi.profile.profile import CompanySerializer
from Brands.models import Company
import json
#Serializer for api
from rest_framework import serializers
from Product.models import Variant, FoodType, AddonDetails, Product, ProductsubCategory,\
FeatureProduct
from Orders.models import Order,OrderStatusType, OrderTracking
from rest_framework.authtoken.models import Token
from Location.models import CityMaster, AreaMaster
from Outlet.models import DeliveryBoy,OutletProfile
from django.db.models import Q
from History.models import CouponUsed
from discount.models import Coupon
from Orders.models import Order
from ZapioApi.api_packages import *
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user

class historyCustomer(APIView):
	"""
	Customer History Details of Order

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to history of Customer Orders.

		Data Post: {
			"mobile"		   : "8750477098",

		}

		Response: {

			"success": True, 
			"message": "Addon details creation/updation api worked well!!",
			"data"      : final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			outlet_id = OutletProfile.objects.filter(auth_user=request.user.id).first().id
			data = request.data
			err_message ={}
			err_message["mobile"] = \
						validation_master_anything(data["mobile"],
						"Mobile or Order ID",vat_re, 3)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			mdata = data['mobile']
			track_data = Order.objects.filter(customer__mobile_number=mdata).order_by('-order_time')
			track_datas = track_data.filter(outlet=outlet_id)
			ord_data =[]
			for i in track_datas:
				p_list ={}
				add = i.address
				p_list['id'] = i.id
				p_list['order_id'] = i.order_id
				p_list['longitude'] = add['longitude']
				p_list['latitude'] = add['latitude']
				p_list['address'] = add['address']
				p_list['locality'] = add['locality']
				p_list['city'] = add['city']
				p_list['order_status'] = i.order_status_id
				p_list['order_time'] = i.order_time.strftime("%d/%b/%y %I:%M %p")
				if  i.payment_mode == '0':
					p_list['payment_mode'] = "Cash on Delivery"
				else:
					p_list['payment_mode'] = "Online"
				p_list['order_status_name'] = OrderStatusType.objects.filter(id=i.order_status_id).first().Order_staus_name
				p_list['color_code'] = OrderStatusType.objects.filter(id=i.order_status_id).first().color_code
				cus = i.customer
				p_list['name'] = cus['name']
				p_list['mobile_number'] = cus['mobile_number']
				p_list['email'] = cus['email']
				p_list['order_description'] = i.order_description
				ord_data.append(p_list)
			return Response({"status":True,
							"orderdata":ord_data
							})
		except Exception as e:
			print("Customer history Stucked into exception!!")
			print(e)
			return Response({"success": False, 
							"message": "Error happened!!", 
							"errors": str(e)})


