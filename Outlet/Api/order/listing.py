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
from Outlet.Api.serializers.order_serializers import OrderSerializer
from django.db.models import Q



class OrderListingData(APIView):
	"""
	Order listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for providing the profile details of brand.
	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request):
		try:
			user = request.user.id
			orderdata = Order.objects.filter(outlet__auth_user=user).order_by('-order_time')
			ord_data =[]
			for i in orderdata:
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
				p_list['discount_value'] = i.discount_value
				p_list['sub_total'] = i.sub_total
				p_list['total_bill_value'] = i.total_bill_value
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
				p_list["statusType"] = []
				ch_pr = OrderStatusType.objects.filter(active_status=1)
				l = []
				for k in ch_pr:
					l.append(k.priority)
				if len(l) > 0:
					maxp = max(l)
				else:
					pass
				status_pr = OrderStatusType.objects.filter(id=i.order_status_id).first().priority
				if status_pr == maxp:
					p_list['maxmium'] = "1"
				else:
					p_list['maxmium'] = "0"
				f_status = OrderStatusType.objects.filter(priority__gt=status_pr)
				st =[]
				for i in f_status:
					st.append(i.priority)
				if len(st) > 0:
					minp = min(st)
				else:
					pass
				orderstatus = OrderStatusType.objects.filter(Q(active_status=1) & Q(priority=minp))
				if orderstatus: 
					for j in orderstatus:
						q_list={}
						q_list['label'] = j.Order_staus_name
						q_list['value'] = j.id
						q_list['key'] = j.Order_staus_name
						if j.is_delivery_boy:
							q_list['is_delivery_boy'] = j.is_delivery_boy
						else:
							q_list['is_delivery_boy'] = 0

						p_list["statusType"].append(q_list)
				else:
					pass
			delivery_boy_data = OutletProfile.objects.filter(auth_user=user).first().id
			deliverydata = DeliveryBoy.objects.filter(Q(active_status=1) & Q(is_assign=0) & Q(Outlet=delivery_boy_data))
			del_type_data=[]
			for k in deliverydata:
				s_list={}
				s_list['label'] = k.name
				s_list['value'] = k.id
				s_list['key'] = k.name
				del_type_data.append(s_list)
			return Response({"status":True,
							"orderdata":ord_data,
							"deliverydata":del_type_data})
		except Exception as e:
			print(e)



