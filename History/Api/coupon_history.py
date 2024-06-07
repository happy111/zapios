from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.sites.shortcuts import get_current_site
from ZapioApi.Api.BrandApi.profile.profile import CompanySerializer
import json
#Serializer for api
from rest_framework import serializers

from Orders.models import Order,OrderStatusType, OrderTracking
from rest_framework.authtoken.models import Token
# from Location.models import CityMaster, AreaMaster
from Outlet.models import DeliveryBoy,OutletProfile
from django.db.models import Q
from History.models import CouponUsed
from discount.models import Coupon
from Orders.models import Order
from Brands.models import Company
from UserRole.models import ManagerProfile
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user



class historyCoupon(APIView):
	"""
	Coupon History listing Post API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for providing the profile details of Coupon History for outlet.
	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request):
		try:
			user = request.user.id
			outlet_id = OutletProfile.objects.filter(auth_user=user).first().id
			if outlet_id:
				coupon_history_data = CouponUsed.objects.filter(outlet=outlet_id)
			else:
				pass
			cup_data = []
			if coupon_history_data:
				for i in coupon_history_data:
					p_list ={}
					p_list['c_code'] = Coupon.objects.filter(id=i.Coupon_id).first().coupon_code
					cus_data = i.customer
					p_list['cname'] = cus_data['name']
					p_list['email'] = cus_data['email']
					p_list['mobile'] = cus_data['mobile_number']
					p_list['coupon_used_at'] = i.created_at.strftime("%d/%b/%y %I:%M %p")
					p_list['order_id'] = Order.objects.filter(id=i.order_id_id).first().order_id
					orderdata = Order.objects.filter(id=i.order_id_id).first()
					ords = orderdata.address
					p_list['longitude'] = ords['longitude']
					p_list['latitude'] = ords['latitude']
					p_list['address'] = ords['address']
					p_list['locality'] = ords['locality']
					p_list['city'] = ords['city']
					ord_desc = orderdata.order_description
					p_list['odesc'] = ord_desc
					if  orderdata.payment_mode == '0':
						p_list['payment_mode'] = "Cash on Delivery"
					else:
						p_list['payment_mode'] = "Online"
					p_list['sub_total'] = orderdata.sub_total
					p_list['discount_value'] = orderdata.discount_value
					p_list['total_bill_value'] = orderdata.total_bill_value
					orderdata = Order.objects.filter(id=i.order_id_id).first()
					cup_data.append(p_list)
			else:
				pass
			return Response({"status":True,
							"message":cup_data})
		except Exception as e:
			print(e)
			return Response({"status":False,
				             "message":cus_data,
				             })



class brandhistoryCoupon(APIView):
	"""
	Coupon History listing Post API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for providing the profile details of Coupon History for outlet.
	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request):
		try:
			user = request.user.id
			cid = get_user(user)
			print("gggggggggggggggggggggg")
			com_id = Company.objects.filter(id=cid).first().id
			if com_id:
				coupon_history_data = CouponUsed.objects.filter(Company=com_id)
			else:
				pass
			cup_data = []
			if coupon_history_data:
				for i in coupon_history_data:
					p_list ={}
					p_list['c_code'] = Coupon.objects.filter(id=i.Coupon_id).first().coupon_code
					cus_data = i.customer
					p_list['cname'] = cus_data['name']
					p_list['email'] = cus_data['email']
					p_list['mobile'] = cus_data['mobile_number']
					p_list['coupon_used_at'] = i.created_at.strftime("%d/%b/%y %I:%M %p")
					p_list['order_id'] = Order.objects.filter(id=i.order_id_id).first().order_id
					orderdata = Order.objects.filter(id=i.order_id_id).first()
					ords = orderdata.address
					p_list['longitude'] = ords['longitude']
					p_list['latitude'] = ords['latitude']
					p_list['address'] = ords['address']
					p_list['locality'] = ords['locality']
					p_list['city'] = ords['city']
					ord_desc = orderdata.order_description
					p_list['odesc'] = ord_desc
					if  orderdata.payment_mode == '0':
						p_list['payment_mode'] = "Cash on Delivery"
					else:
						p_list['payment_mode'] = "Online"
					p_list['sub_total'] = orderdata.sub_total
					p_list['discount_value'] = orderdata.discount_value
					p_list['total_bill_value'] = orderdata.total_bill_value
					orderdata = Order.objects.filter(id=i.order_id_id).first()
					cup_data.append(p_list)
			else:
				pass
			return Response({"status":True,
							"message":cup_data})
		except Exception as e:
			print(e)
			return Response({"status":False,
				             "message":cup_data,
				             })

