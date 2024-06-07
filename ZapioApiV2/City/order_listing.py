import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from ZapioApi.Api.BrandApi.profile.profile import CompanySerializer
from Brands.models import Company
from rest_framework import serializers
from Product.models import (Variant, 
							FoodType, 
							AddonDetails, 
							Product, 
							ProductsubCategory,
							FeatureProduct)
from Orders.models import Order,OrderStatusType, OrderTracking
from rest_framework.authtoken.models import Token
from Location.models import CityMaster, AreaMaster
from Outlet.models import DeliveryBoy,OutletProfile
from Outlet.Api.serializers.order_serializers import OrderSerializer
from django.db.models import Q
from datetime import datetime, timedelta
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ZapioApi.Api.paginate import pagination
import math  
from UserRole.models import ManagerProfile
import dateutil.parser
from django.db.models import Count, Sum, Max, Avg, Case, When, Value, IntegerField, BooleanField
from ZapioApi.api_packages import *
from Configuration.models import PaymentMethod
from Customers.models import *
from Configuration.models import OrderSource,PaymentMethod

class listOrder(APIView):
	"""
	Brand Dashboard retrieval post API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of Brand Dashboard data within brand.

		Data Post: {

			"order"  : 'today'
		}

		Response: {

			"success": True, 
			"message": "Brand Dashboard analysis api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			user = request.user.id
			data = request.data
			ch_brand = Company.objects.filter(auth_user_id=user)
			if ch_brand.count() > 0:
				nuser=user
			else:
				pass
			ch_cashier = ManagerProfile.objects.filter(auth_user_id=user)
			if ch_cashier.count() > 0:
				company_id = ch_cashier[0].Company_id
				auth_user_id = Company.objects.filter(id=company_id)[0].auth_user_id
				nuser=auth_user_id
			else:
				pass
			final_result = []
			card_dict = {}
			now = datetime.now()
			year = now.year
			month = now.month
			today = now.day
			todate = now.date()
			company_id = ch_brand[0].id
			#order_data = Order.objects.filter(Q(Company_id=company_id),~Q(order_status=7))
			order_data = Order.objects.filter(Q(Company_id=company_id))
			if data['order'] == 'today':
				order = order_data.filter(order_time__year=year, order_time__month=month,\
					order_time__day=today)
			elif(data['order'] == '7 days'):
				yesterday = now - timedelta(days=7)
				order = order_data.filter(order_time__gt=yesterday)
			elif(data['order'] == '30 days'):
				yesterday = now - timedelta(days=30)
				order = order_data.filter(order_time__gt=yesterday)
			elif(data['order'] == 'yesterday'):
				yesterday = now - timedelta(days=1)
				order = order_data.filter(order_time__year=year,order_time__month=month,\
					order_time__day=yesterday.day)
			elif(data['order'] == 'this month'):
				order = order_data.filter(order_time__year=year, order_time__month=month)
			elif(data['order'] == 'last month'):
				last_month = month - 1
				order = order_data.filter(order_time__year=year, order_time__month=last_month)
			else:
				pass
			if order.count() > 0:
				for i in order:
					p_list ={}
					add = i.address
					p_list['order_id'] = i.outlet_order_id
					if i.order_time != None:
						p_list['order_time'] =  i.order_time.strftime("%d/%b/%y at %I:%M %p")
					else:
						p_list['order_time'] = ''
					if i.users_id != None:
						p_list['customer_name'] = CustomerProfile.objects.filter(id=i.users_id)[0].name
					else:
						p_list['customer_name'] = ''
					if i.order_source_id != None:
						p_list['order_source'] = OrderSource.objects.filter(id=i.order_source_id)[0].source_name
					else:
						p_list['order_source'] = ''
					p_list['total_bill_value'] = i.total_bill_value
					if i.payment_mode != None:
						p = PaymentMethod.objects.filter(id=i.payment_mode)
						if p.count() > 0:
							p_list['payment_mode'] = p[0].payment_method
						else:
							p_list['payment_mode'] = ''
					else:
						if len(i.settlement_details) > 0:
							for index in i.settlement_details:
								p = PaymentMethod.objects.filter(id=index['mode'])
								if p.count() > 0:
									p_list['payment_mode'] = p[0].payment_method
								else:
									p_list['payment_mode'] = ''
						else:
							p_list['payment_mode'] = ''
					if i.order_status_id != None:
						p_list['order_status_name'] = OrderStatusType.objects.filter(id=i.order_status_id).first().Order_staus_name
						p_list['color_code'] = OrderStatusType.objects.filter(id=i.order_status_id).first().color_code
					else:
						p_list['order_status_name'] = ''
						p_list['color_code'] = ''
					if i.total_items != None:
						p_list['total_items'] = i.total_items
					else:
						p_list['total_items'] = 0
					if i.outlet_id != None:
						p_list['outlet'] = OutletProfile.objects.filter(id=i.outlet_id).first().Outletname
					else:
						p_list['outlet'] = ''
					p_list['id'] = i.id
					p_list['order_description'] = i.order_description
					final_result.append(p_list)
			else:
				pass
			return Response({
						"success": True, 
						"message": "Brand Dashboard analysis api worked well!!",
						"data" : final_result
						})
		except Exception as e:
			print("Dashboard Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})