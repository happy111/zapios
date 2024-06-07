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
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user



class OrderListingData(APIView):
	"""
	Order listing and searching  POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for Order listng and searcing of Brand.

		Data Post: {
			"start_date"            : "2019-07-24 00:00:00:00",
			"end_date"              : "2019-07-29 00:00:00:00"  
			"outlet_id"             : []                    
		}

		Response: {

			"success": True, 
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			err_message = {}

			if data['start_date'] == 'Invalid date' or data['end_date'] == 'Invalid date':
				err_message["Invalid_date"] = "Please enter valid date!!"

			if data['start_date'] == None or data['end_date'] == None:
				err_message["Invalid_date"] = "Please enter valid date!!"

			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})

			if data["start_date"] != '' and data["end_date"] != '':
				start_date = dateutil.parser.parse(data["start_date"])
				end_date = dateutil.parser.parse(data["end_date"])
				if start_date > end_date:
					err_message["from_till"] = "Validity dates are not valid!!"
			else:
				pass
			if len(data["outlet_id"]) > 0:
				outlet_unique_list = []
				for i in data["outlet_id"]:
					err_message["outlet_map"] = validation_master_anything(str(i),
												"Outlet",contact_re, 1)
					if err_message["outlet_map"] != None:
						break
					if i not in outlet_unique_list:
						outlet_unique_list.append(i)
					else:
						err_message["duplicate_outlet"] = "Outlet are duplicate!!"
						break
					record_check = OutletProfile.objects.filter(Q(id=i))
					if record_check.count() == 0:
						err_message["outlet_map"] = "Outlet is not valid!!"
						break
					else:
						pass
			else:
				err_message["outlet_map"] = "Please Enter Outlet!!"
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
				
			user = request.user.id
			cid = get_user(user)
			outlet = data['outlet_id']
			if data["start_date"] != '' and data["end_date"] != '':
				e = end_date
				s = start_date
				query = Order.objects.filter(Q(order_time__lte=e),Q(order_time__gte=s)
					,Q(Company=cid))
				orderdata = query.order_by('-order_time')
				que = Order.objects.filter(Q(order_time__lte=e),Q(order_time__gte=s)
					,Q(Company=cid))
				res1 = que.filter(Q(order_status = 1) | Q(order_status = 2) |
					Q(order_status = 3) | Q(order_status = 4) | Q(order_status = 5))
				csale1 = que.filter(Q(payment_mode = 0),Q(order_status = 5))
				c_item1 = que.filter(order_status = 7)
				settle_order = query.filter(order_status = 6)
			else:
				pass
			q_count = orderdata.count()
			if q_count > 0:
				ord_data =[] 	
				total_value = 0
				tax_value = 0
				dis_value = 0
				sub_value = 0
				pack_value = 0
				deli_value = 0
				ca_items = 0
				pending_orders = 0
				totaltax = 0
				totaldis = 0
				totalsettleorder = 0
				order_value_post_tax = 0
				Order_Value_Pre_tax = 0
				for i in outlet:
					querydata = query.filter(outlet_id=i).order_by('-order_time')
					orderdatas = que.filter(outlet_id=i)
					res = res1.filter(outlet_id=i)
					csale = csale1.filter(outlet_id=i)
					c_item = c_item1.filter(outlet_id=i)
					s_order = settle_order.filter(outlet_id=i)
					for i in querydata:
						p_list ={}
						add = i.address
						p_list['id'] = i.id
						p_list['order_id'] = i.outlet_order_id
						p_list['order_status'] = i.order_status_id
						p_list['discount_value'] = i.discount_value
						p_list['order_source'] = i.order_source.source_name
						p_list['sub_total'] = i.sub_total
						p_list['distance'] = i.distance
						p_list['coupon_code'] = i.coupon_code

						p_list['total_bill_value'] = i.total_bill_value
						o_time = i.order_time+timedelta(hours=5,minutes=30)
						p_list['order_time'] = o_time.strftime("%d/%b/%y %I:%M %p")
						p = i.delivery_time
						if p != None:
							d_time = i.delivery_time+timedelta(hours=5,minutes=30)
							p_list['delivery_time'] = d_time.strftime("%d/%b/%y %I:%M %p")
						else:
							p_list['delivery_time'] = None
						
						if i.settlement_details !=None:
							if len(i.settlement_details) > 0:
								for k in i.settlement_details:
									if k['mode'] !=None and k['mode'] != 0:
										p_list['payment_mode'] = PaymentMethod.objects.filter(id=k['mode'])[0].payment_method
									else:
										if i.is_aggregator == True:
											p_list['payment_mode'] = i.aggregator_payment_mode
										else:
											p_list['payment_mode'] = ''
							else:
								if i.is_aggregator == True:
									p_list['payment_mode'] = i.aggregator_payment_mode
								else:
									p_list['payment_mode'] = ''
						else:
							if i.is_aggregator == True:
								p_list['payment_mode'] = i.aggregator_payment_mode
							else:
								if i.order_source.source_name == 'Website Order':
									p_list["payment_mode"] = i.payment_mode
								else:
									p_list["payment_mode"] = ""
						
						order_status_rec = OrderStatusType.objects.filter(id=i.order_status_id)
						if order_status_rec.count() != 0:
							p_list['order_status_name'] =\
							order_status_rec.first().Order_staus_name
							p_list['color_code'] = order_status_rec.first().color_code
						else:
							return Response(
								{"message":"Order Status Configuration data is not set in backend!!"})
						p_list["can_process"] = True
						if i.order_status.can_process == 1:
							pass
						else:
							p_list["can_process"] = False
						if i.outlet == None:
							p_list["outlet_name"] = 'N/A'
						else:
							p_list["outlet_name"] = i.outlet.Outletname
						ord_data.append(p_list)
					pen_order = res.values('Company').\
								annotate(total_revenue=Sum('total_bill_value'),order_count=Count("id"))
					if pen_order.count() > 0:
						p = pen_order[0]['order_count']
						pending_orders = pending_orders + int(p)
					else:
						pass
					if c_item.count() > 0:
						can_result = c_item.values('Company').\
								annotate(total_revenue=Sum('total_bill_value'),order_count=Count("id"))
						ca =  can_result[0]["order_count"]
						ca_items = ca_items + int(ca)
					else:
						pass
					if s_order.count() > 0:
						tax_result = s_order.values('Company').\
								annotate(total_revenue=Sum('taxes'),order_count=Count("id"))
						dis_result = s_order.values('Company').\
								annotate(total_revenue=Sum('discount_value'),order_count=Count("id"))
						sub_result = s_order.values('Company').\
								annotate(total_revenue=Sum('sub_total'),order_count=Count("id"))
						packing_result = s_order.values('Company').\
								annotate(total_revenue=Sum('packing_charge'),order_count=Count("id"))
						delivery_result = s_order.values('Company').\
								annotate(total_revenue=Sum('delivery_charge'),order_count=Count("id"))
						ta_value    =  tax_result[0]["total_revenue"]
						di_value    =  dis_result[0]["total_revenue"]
						su_value    =  sub_result[0]["total_revenue"]
						pac_value    =  packing_result[0]["total_revenue"]
						del_value    =  delivery_result[0]["total_revenue"]
						if ta_value !=None:
							tax_value = float(tax_value) + float(ta_value)
						else:
							tax_value = 0
						if di_value !=None:
							dis_value = float(dis_value) + float(di_value)
						else:
							dis_value = 0
						if su_value !=None:
							sub_value = float(sub_value) + float(su_value) 
						else:
							sub_value = 0
						if pac_value !=None:
							pack_value = float(pack_value) + float(pac_value)
						else:
							pack_value = 0
						if del_value !=None:
							deli_value = float(deli_value) + float(del_value)
						else:
							deli_value = 0
						o = dis_result[0]["order_count"]
						totaltax = float(tax_value) + totaltax
						totaldis = round(float(dis_value) + totaldis,2)
						totalsettleorder = totalsettleorder + o
					else:
						pass
				
				if sub_value > 0:
					sub_value = round(sub_value,2)
					Order_Value_Pre_tax = round(float(sub_value) - float(dis_value) + float(pack_value) + float(deli_value),2)
					order_value_post_tax = round(Order_Value_Pre_tax + float(tax_value),2)
				else:
					sub_value = 0
				
				return Response({"status":True,
							"orderdata"      :ord_data,
							"pending_orders" : pending_orders,
							"cancelled"      : int(ca_items),
							"gmv"		     : sub_value,
							"netsale"        : Order_Value_Pre_tax,
							"grosssale"      : order_value_post_tax,
							"totaltax"       : tax_value,
							"totaldis"       : dis_value,
							"totalorder"     : totalsettleorder
							})
			else:
				return Response({"status":True,
							"orderdata":[],
							"page_count" : []})
		except Exception as e:
			print(e)
			return Response(
						{"error":str(e)}
						)






