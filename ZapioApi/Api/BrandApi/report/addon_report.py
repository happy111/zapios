import json,math
import dateutil.parser 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from ZapioApi.Api.BrandApi.profile.profile import CompanySerializer
from Brands.models import Company
from rest_framework import serializers
from Product.models import Variant, FoodType, AddonDetails, Product, ProductsubCategory,\
FeatureProduct
from Orders.models import Order,OrderStatusType, OrderTracking
from rest_framework.authtoken.models import Token
from Location.models import CityMaster, AreaMaster
from Outlet.models import DeliveryBoy,OutletProfile
from Outlet.Api.serializers.order_serializers import OrderSerializer
from django.db.models import Q
from datetime import datetime, timedelta

from UserRole.models import ManagerProfile
from django.db.models import Count, Sum, Max, Avg, Case, When, Value, IntegerField, BooleanField
from ZapioApi.api_packages import *
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user



class AddonReport(APIView):
	"""
	Addon Report  POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for addon report for brand.

		Data Post: {
			"start_date"            : "2019-07-24 00:00:00:00",
			"end_date"              : "2019-07-29 00:00:00:00" ,
                     
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
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			user = request.user.id
			cid = get_user(user)
			if data["start_date"] != '' and data["end_date"] != '':
				d = Order.objects.filter(Q(order_time__lte=end_date),Q(order_time__gte=start_date)
					,Q(Company=cid)).order_by('-order_time')
			else:
				pass
			ord_data =[]  
			ord_data1 =[]  
			ord_data3 = []
			q_count = d.count()
			if q_count > 0:
				for i in d:
					if i.is_aggregator==True:
						if i.order_description !=None:
							for j in i.order_description:
								if 'add_ons' in j:
									k = j['add_ons']
									for p in k:
										alls = {}
										price = p['price']
										if 'addon_name' in p:
											alls['addon_name']  = p['addon_name']
										else:
											pass
										if 'title' in p:
											alls['addon_name']  = p['title']
										else:
											pass	
										if 'quantity' in p:
											alls['quantity']  = p['quantity']
										else:
											alls['quantity']  = 1											
										alls['order_id'] = i.outlet_order_id
										alls['price'] = p['price']
										alls['source'] = i.payment_source
										o = i.order_time
										o_time = o+timedelta(hours=5,minutes=30)
										alls['time'] = str(o_time.strftime("%I:%M %p"))
										alls['dt'] = str(o_time.strftime("%d/%b/%y"))
										alls['outlet'] =  OutletProfile.objects.filter(id=i.outlet_id)[0].Outletname
										# print("vvvvvvvvvvvvvvv",alls)
										ord_data.append(alls)
								else:
									pass
						else:
							pass
					else:
						if i.order_description !=None:
							for j in i.order_description:
								if 'add_ons' in j:
									k = j['add_ons']
									for p in k:
										alls = {}
										price = p['price']
										if 'addon_name' in p:
											alls['addon_name']  = p['addon_name']
										else:
											pass
										if 'title' in p:
											alls['addon_name']  = p['title']
										else:
											pass
										if 'quantity' in p:
											alls['quantity']  = p['quantity']
										else:
											alls['quantity'] = 1	
										alls['order_id'] = i.outlet_order_id
										alls['price'] = p['price']
										alls['source'] = i.payment_source
										o = i.order_time
										o_time = o+timedelta(hours=5,minutes=30)
										alls['time'] = str(o_time.strftime("%I:%M %p"))
										alls['dt'] = str(o_time.strftime("%d/%b/%y"))
										alls['outlet'] =  OutletProfile.objects.filter(id=i.outlet_id)[0].Outletname
										ord_data1.append(alls)
								else:
									pass
						else:
							pass
			else:
				pass


			ord_data3 = ord_data + ord_data1

			if len(ord_data3) > 0:
				return Response({"status":True,
								"orderdata":ord_data3,
							})
			else:
				return Response({"status":True,
								"orderdata":[],
							   })
		except Exception as e:
			print(e)
			return Response(
						{"error":str(e)}
						)


