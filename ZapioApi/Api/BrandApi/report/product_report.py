from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from ZapioApi.Api.BrandApi.profile.profile import CompanySerializer
from Brands.models import Company
import json,math,dateutil.parser
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
from datetime import datetime, timedelta
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ZapioApi.Api.paginate import pagination
from UserRole.models import ManagerProfile
from django.db.models import Count, Sum, Max, Avg, Case, When, Value, IntegerField, BooleanField
from ZapioApi.api_packages import *



class ProductReport(APIView):
	"""
	Product Report  POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for product report for brand.

		Data Post: {
			"start_date"            : "2019-07-24 00:00:00:00",
			"end_date"              : "2019-07-29 00:00:00:00",
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
					record_check = OutletProfile.objects.filter(Q(id=i),Q(active_status=1))
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
			is_outlet = OutletProfile.objects.filter(auth_user_id=user)
			is_brand = Company.objects.filter(auth_user_id=user)
			is_cashier = ManagerProfile.objects.filter(auth_user_id=user)
			if is_cashier.count() > 0:
				cid = ManagerProfile.objects.filter(auth_user_id=user)[0].Company_id
			else:
				pass
			if is_outlet.count() > 0:
				outlet = OutletProfile.objects.filter(auth_user_id=user)
				cid = outlet[0].Company_id
			else:
				pass
			if is_brand.count() > 0:
				outlet = Company.objects.filter(auth_user_id=user)
				cid = outlet[0].id
			else:
				pass
			if data["start_date"] != '' and data["end_date"] != '':
				e = end_date.date()
				s = start_date.date()
				orderdata = Order.objects.filter(Q(order_time__lte=end_date),Q(order_time__gte=start_date)
					,Q(Company=cid)).order_by('-order_time')
			else:
				pass
			outlet = data['outlet_id']
			ord_data =[]    
			for k in outlet:
				d = orderdata.filter(outlet_id=k)
				q_count = d.count()
				if q_count > 0: 
					for i in d:
						p_list ={}
						add = i.address
						p_list['id'] = i.id
						p_list['product_detail'] = []
						if i.is_aggregator == True:
							if i.order_description !=None:
								for j in i.order_description:
									alls = {}
									alls['order_id'] = i.outlet_order_id
									if 'name' in j:
										alls['name'] = j['name']
									if 'final_product_id' in j:
										alls['id'] = j['final_product_id']
									else:
										pass
									alls['price'] = j['price']
									if 'quantity' in j:
										alls['qty'] = j['quantity']
									else:
										alls['qty'] = 0
									alls['outlet'] = OutletProfile.objects.filter(id=i.outlet_id)[0].Outletname
									if 'food_type' in j:
										alls['food_type'] = j['food_type']
									ord_data.append(alls)
							else:
								pass
						else:
							if i.order_description !=None:
								for j in i.order_description:
									alls = {}
									alls['order_id'] = i.outlet_order_id
									if 'name' in j:
										alls['name'] = j['name']
									if 'product_id' in j:
										pid  = j['product_id']
									else:
										pass
									if 'id' in j:
										pid  = j['id']
									else:
										pass
									alls['price'] = j['price']
									if 'quantity' in j:
										alls['qty'] = j['quantity']
									else:
										alls['qty'] = 0
									alls['outlet'] = OutletProfile.objects.filter(id=i.outlet_id)[0].Outletname
									ch_p = Product.objects.filter(id=pid)
									if ch_p.count() > 0:
										ft = FoodType.objects.filter(id=ch_p[0].food_type_id)[0].food_type
										alls['food_type'] = ft
									else:
										alls['food_type'] = ''
									if 'varients' in j:
										if type(j['varients']) == str:
											alls['varients'] = j['varients']
										else:
											v = Variant.objects.filter(id=j['varients'])
											if v.count() > 0:
												alls['varients'] = v[0].variant
												alls['vid'] = v[0].id
											else:
												alls['varients'] = ''
									else:
										alls['varients'] = ''
										alls['vid'] = ''
									if 'size' in j:
										alls['varients'] = j['size']
										if j['size'] !='N/A':
											v = Variant.objects.filter(variant=j['size'])
											if v.count() > 0:
												alls['vid'] = v[0].id
											else:
												alls['vid'] = ''
									else:
										alls['varients'] = ''
										alls['vid'] = ''
									if alls['vid'] !='':
										sp = ProductSync.objects.filter(product_id = pid,variant_id=alls['vid'])
										if sp.count() > 0:
											alls['id'] = sp[0].id
										else:
											alls['id'] =''
									else:
										sp = ProductSync.objects.filter(product_id = pid)
										if sp.count() > 0:
											alls['id'] = sp[0].id
										else:
											alls['id'] =''
									ord_data.append(alls)
							else:
								pass
				else:
					pass
			if len(ord_data) > 0:
				return Response({"status":True,
								"orderdata":ord_data,
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




