import re
import json
import calendar
from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
from datetime import datetime
from django.db.models import Q

#Serializer for api
from rest_framework import serializers
from Product.models import ProductCategory, AddonDetails, Variant
from Orders.models import Order
from django.db.models import Count, Sum, Max, Avg, Case, When, Value, IntegerField, BooleanField
from django.db.models.functions import ExtractYear, ExtractMonth,ExtractWeek, ExtractWeekDay
from django.db.models.functions import Extract
from datetime import datetime, timedelta
from backgroundjobs.models import backgroundjobs
from UserRole.models import ManagerProfile
from Customers.models import CustomerProfile
from Configuration.models import PaymentMethod,WebsiteStatistic,OrderSource
from History.models import MenuCounts
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user
import dateutil.parser

class dashboard(APIView):
	"""
	Brand Dashboard retrieval GET API

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
			data = request.datatotal_sale
			ch_brand = Company.objects.filter(auth_user_id=user)
			if ch_brand.count() > 0:
				nuser=user
				company_id = ch_brand[0].id
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
			order_data = Order.objects.filter(Q(Company_id=company_id))
			if data['order'] == 'today':
				order = order_data.filter(order_time__year=year,\
                order_time__month=month,order_time__day=today)		
				ws = WebsiteStatistic.objects.filter(company_id=company_id)
				if ws.count() > 0:
					c = ws.filter(created_at__year=year,created_at__month=month,\
					created_at__day=today,visitors=1)
					if c.count() > 0:
						card_dict["no_visitiors"] = c.count()
					else:
						card_dict["no_visitiors"] = 0
				else:
					pass
				m = ws.filter(created_at__year=year,created_at__month=month,\
					created_at__day=today,menu_views=1)
				if m.count() > 0:
					card_dict["no_menu_views"] = m.count()
				else:
					card_dict["no_menu_views"] = 0

				c = ws.filter(created_at__year=year,created_at__month=month,\
					created_at__day=today,checkout=1)
				if c.count() > 0:
					card_dict["no_user_reach_checkout"] = c.count()
				else:
					card_dict["no_user_reach_checkout"] = 0

				source_data = OrderSource.objects.filter(source_name='Website Order',company_id=company_id)
				if source_data.count() > 0:
					online_order = order_data.filter(order_time__year=year,order_time__month=month,\
					order_time__day=today,order_source_id=source_data[0].id)
					if online_order.count() > 0:
						card_dict["no_online_orders"] = online_order.count()
					else:
						card_dict["no_online_orders"] = 0
				else:
					card_dict["no_online_orders"] = 0
				mdata = MenuCounts.objects.filter(event_time__date=datetime.now().date(),company_id=company_id)
			elif(data['order'] == '7 days'):
				yesterday = now - timedelta(days=7)
				order = order_data.filter(order_time__gt=yesterday)
				ws = WebsiteStatistic.objects.filter(company_id=company_id)
				if ws.count() > 0:
					c = ws.filter(created_at__gt=yesterday,visitors=1)
					if c.count() > 0:
						card_dict["no_visitiors"] = c.count()
					else:
						card_dict["no_visitiors"] = 0
				else:
					pass
				m = ws.filter(created_at__gt=yesterday,menu_views=1)
				if m.count() > 0:
					card_dict["no_menu_views"] = m.count()
				else:
					card_dict["no_menu_views"] = 0
				c = ws.filter(created_at__gt=yesterday,checkout=1)
				if c.count() > 0:
					card_dict["no_user_reach_checkout"] = c.count()
				else:
					card_dict["no_user_reach_checkout"] = 0
				source_data = OrderSource.objects.filter(source_name='Website Order',company_id=company_id)
				if source_data.count() > 0:
					online_order = order_data.filter(order_time__gt=yesterday,\
									order_source_id=source_data[0].id)
					if online_order.count() > 0:
						card_dict["no_online_orders"] = online_order.count()
					else:
						card_dict["no_online_orders"] = 0
				else:
					card_dict["no_online_orders"] = 0
				mdata = MenuCounts.objects.filter(event_time__gt=yesterday,company_id=company_id)
			elif(data['order'] == '30 days'):
				yesterday = now - timedelta(days=30)
				order = order_data.filter(order_time__gt=yesterday)
				ws = WebsiteStatistic.objects.filter(company_id=company_id)
				if ws.count() > 0:
					c = ws.filter(created_at__gt=yesterday,visitors=1)
					if c.count() > 0:
						card_dict["no_visitiors"] = c.count()
					else:
						card_dict["no_visitiors"] = 0
				else:
					pass
				m = ws.filter(created_at__gt=yesterday,menu_views=1)
				if m.count() > 0:
					card_dict["no_menu_views"] = m.count()
				else:
					card_dict["no_menu_views"] = 0
				c = ws.filter(created_at__gt=yesterday,checkout=1)
				if c.count() > 0:
					card_dict["no_user_reach_checkout"] = m.count()
				else:
					card_dict["no_user_reach_checkout"] = 0
				source_data = OrderSource.objects.filter(source_name='Website Order',company_id=company_id)
				if source_data.count() > 0:
					online_order = order_data.filter(order_time__gt=yesterday,\
									order_source_id=source_data[0].id)
					if online_order.count() > 0:
						card_dict["no_online_orders"] = online_order.count()
					else:
						card_dict["no_online_orders"] = 0
				else:
					card_dict["no_online_orders"] = 0
				mdata = MenuCounts.objects.filter(event_time__gt=yesterday,company_id=company_id)
			elif(data['order'] == 'yesterday'):
				yesterday = now - timedelta(days=1)
				order = order_data.filter(order_time__year=year,order_time__month=month,\
					order_time__day=yesterday.day)				
				ws = WebsiteStatistic.objects.filter(company_id=company_id)
				if ws.count() > 0:
					c = ws.filter(created_at__year=year,created_at__month=month,\
					created_at__day=yesterday.day,visitors=1)
					if c.count() > 0:
						card_dict["no_visitiors"] = c.count()
					else:
						card_dict["no_visitiors"] = 0
				else:
					pass
				m = ws.filter(created_at__year=year,created_at__month=month,\
					created_at__day=yesterday.day,menu_views=1)
				if m.count() > 0:
					card_dict["no_menu_views"] = m.count()
				else:
					card_dict["no_menu_views"] = 0

				c = ws.filter(created_at__year=year,created_at__month=month,\
					created_at__day=yesterday.day,checkout=1)
				if c.count() > 0:
					card_dict["no_user_reach_checkout"] = c.count()
				else:
					card_dict["no_user_reach_checkout"] = 0
				source_data = OrderSource.objects.filter(source_name='Website Order',company_id=company_id)
				if source_data.count() > 0:
					online_order = order_data.filter(order_time__year=year,order_time__month=month,\
					order_time__day=yesterday.day,order_source_id=source_data[0].id)
					if online_order.count() > 0:
						card_dict["no_online_orders"] = online_order.count()
					else:
						card_dict["no_online_orders"] = 0
				else:
					card_dict["no_online_orders"] = 0
				mdata = MenuCounts.objects.filter(event_time__gt=yesterday,company_id=company_id)
			elif(data['order'] == 'this month'):
				order = order_data.filter(order_time__year=year, order_time__month=month)
				ws = WebsiteStatistic.objects.filter(company_id=company_id)
				if ws.count() > 0:
					c = ws.filter(created_at__year=year,created_at__month=month,visitors=1)
					if c.count() > 0:
						card_dict["no_visitiors"] = c.count()
					else:
						card_dict["no_visitiors"] = 0
				else:
					pass
				m = ws.filter(created_at__year=year,created_at__month=month,menu_views=1)
				if m.count() > 0:
					card_dict["no_menu_views"] = m.count()
				else:
					card_dict["no_menu_views"] = 0

				c = ws.filter(created_at__year=year,created_at__month=month,checkout=1)
				if c.count() > 0:
					card_dict["no_user_reach_checkout"] = c.count()
				else:
					card_dict["no_user_reach_checkout"] = 0
				source_data = OrderSource.objects.filter(source_name='Website Order',company_id=company_id)
				if source_data.count() > 0:
					online_order = order_data.filter(order_time__year=year,order_time__month=month,\
									order_source_id=source_data[0].id)
					if online_order.count() > 0:
						card_dict["no_online_orders"] = online_order.count()
					else:
						card_dict["no_online_orders"] = 0
				else:
					card_dict["no_online_orders"] = 0
				mdata = MenuCounts.objects.filter(event_time__month=month,company_id=company_id)
			elif(data['order'] == 'last month'):
				last_month = month - 1
				order = order_data.filter(order_time__year=year, order_time__month=last_month)
				ws = WebsiteStatistic.objects.filter(company_id=company_id)
				if ws.count() > 0:
					c = ws.filter(created_at__year=year,created_at__month=last_month,visitors=1)
					if c.count() > 0:
						card_dict["no_visitiors"] = c.count()
					else:
						card_dict["no_visitiors"] = 0
				else:
					pass
				m = ws.filter(created_at__year=year,created_at__month=last_month,menu_views=1)
				if m.count() > 0:
					card_dict["no_menu_views"] = m.count()
				else:
					card_dict["no_menu_views"] = 0
				c = ws.filter(created_at__year=year,created_at__month=last_month,checkout=1)
				if c.count() > 0:
					card_dict["no_user_reach_checkout"] = c.count()
				else:
					card_dict["no_user_reach_checkout"] = 0
				source_data = OrderSource.objects.filter(source_name='Website Order',company_id=company_id)
				if source_data.count() > 0:
					online_order = order_data.filter(order_time__year=year,order_time__month=last_month,\
									order_source_id=source_data[0].id)
					if online_order.count() > 0:
						card_dict["no_online_orders"] = online_order.count()
					else:
						card_dict["no_online_orders"] = 0
				else:
					card_dict["no_online_orders"] = 0
				mdata = MenuCounts.objects.filter(event_time__month=last_month,event_time__year=year,company_id=company_id)
			else:
				pass
			if order.count() > 0:
				total_order = order.count()
				tevenue = order.values('Company').\
							annotate(total_revenue=Sum('total_bill_value'),order_count=Count("id"))
				
				today_revenue = tevenue[0]["total_revenue"]

				tax_result = order.values('Company').\
							annotate(total_tax=Sum('taxes'),order_count=Count("id"))
				dis_result = order.values('Company').\
							annotate(total_discount=Sum('discount_value'),order_count=Count("id"))
				today_tax = tax_result[0]['total_tax']
				today_discount = dis_result[0]['total_discount']
			else:
				today_revenue = 0
				today_tax = 0
				today_discount = 0
				total_order = 0
			card_dict['menu_detail'] = []
			if mdata.count() > 0:
				sb_result = mdata.values('company','menu_name').\
								annotate(id=Sum('id'),menu_view=Count("menu_id"))
				total = 0
				if sb_result.count() > 0:
					for index in sb_result:
						dic = {}
						dic['menu_name'] = index['menu_name']
						dic['menu_view'] = index['menu_view']
						total = total + int(index['menu_view'])
						card_dict['menu_detail'].append(dic)
				else:
					pass
				card_dict['total_view'] = total
			else:
				card_dict['total_view'] = 0
			card_dict["today_order_count"] = total_order
			card_dict["today_order_sale"] = today_revenue
			card_dict["today_total_tax"] = today_tax
			card_dict["today_total_discount"] = today_discount
			# card_dict["no_user_reach_checkout"] = 0
			final_result.append(card_dict)
			return Response({
						"success": True, 
						"message": "Brand Dashboard analysis api worked well!!",
						"data" : final_result
						})
		except Exception as e:
			print("Dashboard Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})

