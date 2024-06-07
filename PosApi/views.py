import re
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Outlet.models import *
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
from rest_framework import serializers
from Location.models import CountryMaster
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user
from django.db.models import Q
from UserRole.models import *
from datetime import datetime, timedelta
from Orders.models import Order, OrderStatusType, OrderTracking
import dateutil.parser
from django.db.models import Count, Sum, Max, Avg, Case, When, Value, IntegerField, BooleanField
from Configuration.models import *


class PaymentList(APIView):
	"""
	Payment Method listing Configuration POST API
		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to provide all payment method.
		Data Post: {
			
		}
		Response: {
			"success": True,
			"data" :  serializer,
			"message": "Payment Method listing api worked well!!"
		}
	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			if 'outlet' in data:
				outlet = data['outlet']
				err_message = {}
				auth_id = request.user.id
				cid = get_user(auth_id)
				data['company'] = OutletProfile.objects.filter(id=outlet)[0].Company_id
				query = PaymentMethod.objects.filter(company_id=data['company'],active_status=1)
				outlet_data = OutletProfile.objects.filter(id=outlet)
				if query.count()==0:
					return Response(
						{
							"success": False,
		 					"message": "No Payment Method Found"
						}
						) 
				else:
					serializer = []
					for index in query:
						if outlet_data[0].payment_method != None:
							if str(index.id) in outlet_data[0].payment_method:
								q_dict = {}
								q_dict["id"] = index.id
								q_dict["country"] = index.country.country
								q_dict["symbol"] = index.symbol
								q_dict["payment_method"] = index.payment_method
								q_dict["keyid"] = index.keyid
								q_dict["keySecret"] = index.keySecret
								q_dict["active_status"] = index.active_status
								q_dict["created_at"] = index.created_at
								q_dict["updated_at"] = index.updated_at
								q_dict["wordLimit"] = index.word_limit
								q_dict["order_source"] = []
								ut = str(index.id)
								source_data = OrderSource.objects.filter(payment_method__contains=[index.id],
									company_id=data['company'])
								if source_data.count() > 0:
									for i in source_data:
										dic = {}
										source_id = i.id
										dic['id'] = source_id
										dic['order_source'] = i.source_name
										q_dict["order_source"].append(dic)
								domain_name = addr_set()
								if index.payment_logo != "" and index.payment_logo != None:
									full_path = domain_name + str(index.payment_logo)
									q_dict['payment_logo'] = full_path
								else:
									q_dict['payment_logo'] = ''
								serializer.append(q_dict)
						else:
							pass
				return Response(
						{
							"success": True,
							"data" : serializer,
		 					"message": "Payment Method listing api worked well!!"
						}
						)
			else:
				err_message = {}
				auth_id = request.user.id
				cid = get_user(auth_id)
				query = PaymentMethod.objects.filter(company_id=cid,active_status=1)
				if query.count()==0:
					return Response(
						{
							"success": False,
		 					"message": "No Payment Method Found"
						}
						) 
				else:
					serializer = []
					for index in query:
						q_dict = {}
						q_dict["id"] = index.id
						q_dict["country"] = index.country.country
						q_dict["symbol"] = index.symbol
						q_dict["payment_method"] = index.payment_method
						q_dict["keyid"] = index.keyid
						q_dict["keySecret"] = index.keySecret
						q_dict["active_status"] = index.active_status
						q_dict["created_at"] = index.created_at
						q_dict["updated_at"] = index.updated_at
						q_dict["wordLimit"] = index.word_limit
						domain_name = addr_set()
						if index.payment_logo != "" and index.payment_logo != None:
							full_path = domain_name + str(index.payment_logo)
							q_dict['payment_logo'] = full_path
						else:
							q_dict['payment_logo'] = ''
						serializer.append(q_dict)
				return Response(
						{
							"success": True,
							"data" : serializer,
		 					"message": "Payment Method listing api worked well!!"
						}
						)		
		except Exception as e:
			print("Payment Method listing api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})




class listSource(APIView):

	"""
	Order Source listing GET API
		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of Source data.
	"""
	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			user = request.user.id
			user = request.user.id
			cid = get_user(user)
			allsource = OrderSource.objects.filter(company_id=cid).order_by('priority')
			final_result = []
			if allsource.count() > 0:
				for i in allsource:
					dict_source = {}
					dict_source['source_name'] = i.source_name
					dict_source['id'] = i.id
					dict_source['active_status'] = i.active_status
					dict_source['is_edit'] = i.is_edit
					im = str(i.image)
					if im != "" and im != None and im != "null":
						domain_name = addr_set()
						full_path = domain_name + str(i.image)
						dict_source['image'] = full_path
					else:
						pass
					final_result.append(dict_source)
				return Response({
						"success": True, 
						"data": final_result})
			else:
				return Response({
						"success": True, 
						"data": []})
		except Exception as e:
			print("Source listing Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})

class EionOrderListingData(APIView):
	"""
	Order listing GET API for Eion Users
		Service Usage & Description	: This Api is used for providing listing all order of brand.
		Request Params
		{
			"api_key": "api_zzzzzzz",
			"eion_brand":10 or "eion_outlet":12
		}
	"""

	def get(self, request):
		api_key = self.request.GET.get('api_key')
		if api_key:
			try:
				eion_brand =self.request.GET.get('eion_brand')
				eion_outlet=self.request.GET.get('eion_outlet')
				mutable = request.POST._mutable
				request.POST._mutable = True
				if eion_brand:
					companies = Company.objects.filter(api_key=api_key)
					if companies.count():
						company = companies[0]
						company.eion_brand_id=int(eion_brand)
						company.save()
					else:
						return Response({"message":"API Key is invalid"},status=status.HTTP_400_BAD_REQUEST)
				if eion_outlet:
					outlets = OutletProfile.objects.filter(api_key=api_key)
					if outlets.count():
						outlet = outlets[0]
						outlet.eion_outlet_id=int(eion_outlet)
						outlet.save()
						company = outlet.Company
					else:
						return Response({"message":"API Key is invalid"},status=status.HTTP_400_BAD_REQUEST)

				now = datetime.now()
				today = now.date()
				ord_data =[]

				Received = 0
				Food_Ready= 0
				Delivered= 0
				Settled = 0
				Accepted= 0
				Dispatched= 0
				clogo = Company.objects.filter(id=company.id)[0].company_logo
				if clogo !=None:
					domain_name = addr_set()
					full_path = domain_name + str(clogo)
				else:
					full_path = ''
				orderdata = Order.objects.filter(
					Q(order_time__date__gte=today),Q(Company_id=company.id)).order_by('-order_time')
				for i in orderdata:
					p_list ={}
					add = i.address
					p_list['id'] = i.id
					p_list['delivery_address'] = i.address
					p_list['special_instructions'] = i.special_instructions
					p_list['customer'] = i.customer
					p_list['order_id'] = i.outlet_order_id
					p_list['order_status'] = i.order_status_id
					p_list["log"] = []
					orderlog = OrderTracking.objects.filter(order_id=p_list["id"]).order_by("id")
					if orderlog.count() > 0:
						for j in orderlog:
							r_list = {}
							r_list["id"] = j.id
							r_list["status_name"] = j.Order_staus_name.Order_staus_name
							created_at = j.created_at + timedelta(hours=5, minutes=30)
							r_list["created_at"] = created_at.strftime("%d/%b/%y %I:%M %p")
							r_list["key_person"] = j.key_person
							p_list["log"].append(r_list)
					else:
						pass
					p_list['delivery_type'] = i.delivery_type
					p_list['company_logo'] = full_path
					p_list['discount_value'] = i.discount_value
					p_list['sub_total'] = i.sub_total
					p_list['total_bill_value'] = i.total_bill_value
					p_list['tax'] = i.taxes
					p_list['urban_order_id'] = i.urban_order_id
					p_list['channel_order_id'] = i.channel_order_id
					p_list['source'] = i.order_source.source_name
					p_list['is_order_now'] = i.is_order_now
					p_list['rider_id'] = i.delivery_boy_id
					p_list['order_description'] = i.order_description
					full_path = addr_set()
					if i.order_source.image != None and i.order_source.image != "":
						p_list['pic'] = full_path+str(i.order_source.image)
					else:
						p_list['pic'] = ''
					o_time = i.order_time+timedelta(hours=5,minutes=30)
					# p_list['order_time'] = o_time.strftime("%d/%b/%y %I:%M %p")
					p_list['order_time'] =  o_time.isoformat()

					if i.schedule_delivery_time != None:
						s_time = i.schedule_delivery_time+timedelta(hours=5,minutes=30)
						p_list['schedule_date'] = s_time.isoformat()
					else:
						p_list['schedule_date'] = ''
					p_list['schedule_time'] = i.schedule_time
					p_list['delivery_time'] = i.delivery_time
					if p_list['delivery_time'] != None:
						d_time = i.delivery_time+timedelta(hours=5,minutes=30)
						p_list['delivery_time'] = d_time.isoformat()
					else:
						p_list['delivery_time'] = None
					if i.settlement_details !=None:
						if len(i.settlement_details) > 0:
							p_list['payment_mode'] = []
							for k in i.settlement_details:
								if 'mode' in k:
									if k['mode'] !=None:
										mode = {}
										mode['pmode'] = k['payment_name']
										p_list['payment_mode'].append(mode['pmode'])
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
							p_list['payment_mode'] = ''
					if i.is_aggregator == False:
						order_status_rec = OrderStatusType.objects.filter(id=i.order_status_id)
						if order_status_rec.count() != 0:
							p_list['order_status_name'] =\
							order_status_rec.first().Order_staus_name
							p_list['color_code'] = order_status_rec.first().color_code
						else:
							return Response(
								{"message":"Order Status Configuration data is not set in backend!!"})
					else:
						p_list['order_status_name'] = i.Aggregator_order_status
					p_list["can_process"] = True
					if i.order_status.can_process == 1:
						pass
					else:
						p_list["can_process"] = False
					if i.outlet != None:
						p_list["outlet_name"] = i.outlet.Outletname
						p_list["outlet_id"] = i.outlet_id
					else:
						p_list["outlet_name"] ='N/A'
					p_list["is_rider_assign"]  = i.is_rider_assign
					p_list["rider_detail"] = [] 
					if i.is_rider_assign == True:
						if i.is_aggregator == False:
							a = {}
							ad = ManagerProfile.objects.filter(id=i.delivery_boy_id)
							if ad.count() > 0:
								a['name'] = ad[0].manager_name
								a['email'] = ad[0].email
								a['mobile'] = ad[0].mobile
								p_list["rider_detail"].append(a)
						else:
							rider_detail = i.delivery_boy_details
							p_list["rider_detail"].append(rider_detail)
					else:
						a = {}
						a['name'] = ''
						a['email'] = ''
						a['mobile'] = ''
						p_list["rider_detail"].append(a)
					p_list['package_detail'] = []
					pdata = DeliverySetting.objects.filter(company_id=company.id)
					if pdata.count() > 0:
						dic = {}
						dic['price_type'] = pdata[0].price_type
						dic['is_tax'] = pdata[0].is_tax
						if dic['is_tax'] == 1:
							t = pdata[0].tax
							if t != None:
								if len(t) > 0:
									dic['tax'] = []
									for i in t:
										d = {}
										ta = Tax.objects.filter(id=i)
										if ta.count() > 0:
											d['tax_name'] = ta[0].tax_name
											d['percentage'] = ta[0].tax_percent
											dic['tax'].append(d)
										else:
											pass
								else:
									pass
							else:
								pass
						else:
							pass
						dic['delivery_charge'] = pdata[0].delivery_charge
						dic['packing_charge']  = pdata[0].package_charge
						p_list['package_detail'].append(dic)
						if p_list['order_status_name'] == "Received":
							Received += 1  
						if p_list['order_status_name'] == "Food Ready":
							Food_Ready += 1 
						if p_list['order_status_name'] == "Delivered":
							Delivered += 1  
						if p_list['order_status_name'] == "Settled":
							Settled += 1 
						if p_list['order_status_name'] == "Accepted":
							Accepted += 1
						if p_list['order_status_name'] == "Dispatched":
							Dispatched += 1	
							  		
					else:
						pass
					ord_data.append(p_list)
				return Response({"status":True,
								"orderdata":ord_data,"Received":Received,"Food Ready":Food_Ready,"Delivered":Delivered,"Settled":Settled,"Accepted":Accepted,"Dispatched":Dispatched})
			except Exception as e:
				print(e)
				return Response({"error":str(e)})
		return Response({"message":"Api key is Required"},status=status.HTTP_400_BAD_REQUEST)


class EionOrderListingDataReports(APIView):
	"""
	Order listing and searching POST API
		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for Order listng and searcing of Brand.
		Data Post: {
			"api_key"               : "api_zzzzzzz",
			"start_date"            : "2019-07-24 00:00:00:00",
			"end_date"              : "2019-07-29 00:00:00:00",
			"brand"                 : 1                   
		}
		Response: {
			"success": True, 
			"data": final_result
		}
	"""
	
	def post(self, request):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			companies = Company.objects.filter(api_key=data["api_key"])
			err_message = {}
			if data["start_date"] != '' and data["end_date"] != '':
				start_date = dateutil.parser.parse(data["start_date"])
				end_date = dateutil.parser.parse(data["end_date"])
				if start_date > end_date:
					err_message["from_till"] = "Validity dates are not valid!!"
			else:
				pass
			outlet =[]
			if companies.count():
				company = companies[0]
				outlet_unique_list = []
				outlet_objs = OutletProfile.objects.filter(Company=company)
				for i in outlet_objs:
					i = i.id
					outlet.append(i)
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
				
			cid = companies[0].id
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
								pm = PaymentMethod.objects.filter(id=i.payment_mode)
								if pm.count() > 0:
									p_list['payment_mode'] = pm[0].payment_method
								else:
									p_list['payment_mode'] = ''
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
							"orderdata":ord_data,
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

class AizotecEionUnlinkAPI(APIView):
	"""
	Aizotec Eion Unlink POST API
        Service Usage and Description : This API is used to unlink Aizotec Fetch of given Outlet ids.
        Authentication Required: YES
        Data Post: {
			"api_key"               : "api_zzzzzzz",
		}
	"""
	
	def post(self, request):
		try:
			data = request.data
			companies = Company.objects.filter(api_key=data["api_key"])
			if companies.count():
				obj = companies[0]
				obj.eion_brand_id = None 
				obj.save() 
				return Response(status=status.HTTP_200_OK)
			return Response({"message" : "Invalid API Key. No Company found with api key " + str(companies[0].api_key)},status=status.HTTP_404_NOT_FOUND)
		except Exception as e: 
			return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from Product.models import *
import random
from zapio.settings import Media_Path

class FullProductListEion(APIView):
	"""
	Product Listing POST API

		Authentication Required		: YES
		Service Usage & Description	: This Api is used to extract all product associated with outlet.

		Data Post: {
			"api_key" : "api_zzzzz"
		}

		Response: {

			"success": True,
			"credential" : True,
			"product_count" : product_count,
			"menu_data" : final_result
		}

	"""
	def post(self, request, format=None):

		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			companies = Company.objects.filter(api_key=data["api_key"])
			if companies.count() > 0:
				company = Company.objects.get(api_key=data["api_key"])
				outlet = OutletProfile.objects.filter(Company_id=company.id)
				final_result = []
				if outlet.count() > 0:
					Product_L= []
					for i in outlet:
						data["outlet_id"] = i.id
						record = Product_availability.objects.filter(outlet=data["outlet_id"])
						rating = [4,5,4.3,4.2]
						if record.count()!=0:
							avail_product = record[0].available_product
							if len(avail_product) != 0:
								for i in avail_product:
									query = Product.objects.filter(id=str(i),active_status=1)
									if query.count()!=0:
										s  = query[0]
										if s.id not in Product_L:
											menu_info = {}
											menu_info["outlet_availbility_id"] = data["outlet_id"]
											menu_info["name"] = s.product_name
											menu_info["product_id"] = s.id
											Product_L.append(s.id)
											menu_info["product_url"] = company.website
											menu_info["product_desc"] = s.product_desc
											menu_info["short_desc"] = s.short_desc
											menu_info["allergen"] = s.allergen_Information
											menu_info["company"] = s.Company_id
											p = s.product_schema
											fs = []
											if p !=None:
												if len(p) > 0:
													for k in p:
														dic = {}
														if 'unit' in k:
															pin = k['unit']
															uname = Unit.objects.filter(id=pin)[0].unit_name
															quantity = k['quantity']
															name = k['name']
															dic['name'] = name
															dic['qty'] = str(quantity)+' '+str(uname)
															fs.append(dic)
												else:
													pass
											else:
												pass
											menu_info["nutrition"] = fs
											menu_info["product_rating"] = random.choice(rating)
											menu_info["parent_category_id"] = s.product_categorys
											menu_info["parent_category_name"] = []
											if len(s.product_categorys) > 0:
												for index in s.product_categorys:
													cat_dict = {}
													category_name = ProductCategory.objects.filter(id=index)
													cat_dict['parent_category_name'] = category_name[0].category_name
													cat_dict['parent_category_id'] = index
													menu_info["parent_category_name"].append(cat_dict)
											else:
												menu_info["parent_category_name"] =[]
											chk_imag = ProductImage.objects.filter(product_id=i,primary_image=1)
											if chk_imag.count() > 0:
												menu_info['primary_image'] = Media_Path+str(chk_imag[0].product_image)
											else:
												menu_info['primary_image'] = None
											chk_img = ProductImage.objects.filter(product_id=i,primary_image=0)
											if chk_img.count() > 0:
												menu_info['multiple_image'] = []
												for index in chk_img:
													menu_info['multiple_image'].append(Media_Path+str(index.product_image))
													if index.video_url != None:
														menu_info['multiple_image'].append(str(index.video_url))
											else:
												menu_info['multiple_image'] = []
											menu_info["price"] = s.price
											final_result.append(menu_info)
										else:
											pass
									else:
										pass
							else:
								pass
						else:
							pass
					if len(final_result) != 0:
						p_count = len(final_result)
						result = {
									"success": True,
									"credential" : True,
									"product_count" : p_count,
									"menu_data" : final_result
									}
					else:
						result = {
									"success": False,
									"message" : "No menu found",
								}
					return Response(result)
				else:
					return Response({"message": "No Outlet found in the Company"},status=status.HTTP_404_NOT_FOUND)	
			else:
				return Response({"message" : "Invalid API Key. No Company found with api key"},status=status.HTTP_404_NOT_FOUND)	
		except Exception as e:
			print("Product Listing Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})

from frontApi.serializer.restaurent_serializers import OutletDetailsSerializer
from rest_framework_tracking.mixins import LoggingMixin
from Configuration.models import WebsiteStatistic
from geopy.distance import great_circle

class RestaurantMapViewEion(LoggingMixin, APIView):
	"""
	Nearest Restaurant POST API

		Authentication Required		: YES
		Service Usage & Description	: This Api is used to find nearest outlet on the basis of provided lat & 
		long.City and area are optional, request can be made by assigning values in city and area 
		as blank.

		Data Post: {
		
			"latitude"	:	"41.90278349999999",
			"longitude"	:	"12.4963655",
			"api_key" : "api_zzzzz"
		}

		Response: {

			"status"				: True,
			"nearest_restaurants"	: self.customer_nearest_restaurent,
			"message"				: "Your nearest restaurant are sent successfully"
		}

	"""

	def __init__(self):
		self.latitude = None
		self.longitude = None
		self.city = None
		self.area = None
		self.customer_location = None
		self.myLocation = None
		self.config_rule_name = None
		self.config_unloaded_miles = 0
		self.range_in_kilometer = None
		self.customer_nearest_restaurent = []
		self.response_api_message = None
		self.Errors = None
		self.Company = None

	def restaurant_miles_converter(self):
		self.customer_location = (self.latitude, self.longitude)
	
	def chk_open_restaurents(self, restaurant):
		try:
			print(restaurant)
		except Exception as e:
			print("merge_all_nearest_restaurents_exception")
			print(e)
			return None, e
	def restaurant_details_records(self):
		all_restaurant =\
		OutletProfile.objects.filter(active_status=1,is_pos_open=1,
			Company=self.Company).order_by('latitude')
		

		if all_restaurant.count() > 0:
			self.Restaurants = OutletDetailsSerializer(all_restaurant, many=True).data
		else:
			return Response({"status": True,
							"message": "Sorry, we do not currently deliver in your location.",
							})
		self.restaurant_miles_converter()
		if self.customer_nearest_restaurent == []:
			nearest = {}
			to_let = 0
			k = 0
			flag = 0
			for restaurant in self.Restaurants:
				now = datetime.now()
				today = now.strftime('%A')
				time = datetime.now().time()
				chk_out = OutletTiming.objects.filter(Q(day=today),Q(outlet_id=str(restaurant['id'])))
				if chk_out.count() > 0:
					flag = 1
					for index in chk_out:
						k = 1
						open_time = index.opening_time
						close_time = index.closing_time
						cur = time.strftime('%H:%M:%S')
						if open_time > close_time:
							c_tmp = open_time
							open_time = close_time
							close_time = c_tmp
							if time > open_time and time < close_time:
								pass
							else:
								to_let = 1
						else:
							if time > open_time and time < close_time:
								to_let = 1
								if restaurant['latitude'] != 'undefined' and restaurant['longitude'] != 'undefined':
									restaurant_locations = (restaurant['latitude'], restaurant['longitude'])
									unloaded_mile = great_circle(self.customer_location, restaurant_locations).miles
									if unloaded_mile == None:
										unloaded_mile = 0
									else:
										kilometers = round((unloaded_mile / 0.62137119), 2)
										nearest[restaurant['Outletname']] = kilometers
										a=min(zip(nearest.values(), nearest.keys()))
							else:
								pass
				else:
					pass
			if flag == 0:
				return 'Q'
			if to_let == 0:
				return 's'
	
			if len(nearest) > 0:
				for key, value in nearest.items():
					restaurant = OutletProfile.objects.filter(Outletname=key,).first()
					start = []
					end = []
					if restaurant.delivery_zone != None:
						if len(restaurant.delivery_zone) > 0:
							for index in restaurant.delivery_zone:
								start.append(int(index['start']))
								end.append(int(index['end']))
							start_km = min(start)
							end_km = max(end)
							if float(start_km) <= float(value) and float(end_km) >= float(value):
								restaurant_data = {}
								restaurant_data['id'] = restaurant.id
								restaurant_data['Outletname'] = restaurant.Outletname
								restaurant_data['distance'] = value
								restaurant_data['address'] = restaurant.address
								restaurant_data['latitude'] = restaurant.latitude
								restaurant_data['longitude'] = restaurant.longitude
								restaurant_data['latitude'] = restaurant.latitude
								cdata = CountryMaster.objects.filter(id=restaurant.country_id)
								if cdata.count() > 0:
									restaurant_data['country'] = cdata[0].country
								s = StateMaster.objects.filter(id=restaurant.state_id)
								if s.count() > 0:
									restaurant_data['state'] = StateMaster.objects.filter(id=restaurant.state_id)[0].state
								else:
									restaurant_data['state'] = ''
								restaurant_data['city'] = []
								cityDetail = restaurant.map_city
								if cityDetail !=None:
									for index in cityDetail:
										cat_dict = {}
										cat_dict["label"] = CityMaster.objects.filter(id=index)[0].city
										cat_dict['value'] = index
										restaurant_data['city'].append(cat_dict)
								else:
									pass
								areaDetail = restaurant.map_locality
								restaurant_data["area_detail"] = []
								if areaDetail !=None:
									for index in areaDetail:
										ara_dict = {}
										ara_dict["label"] = AreaMaster.objects.filter(id=index)[0].area
										ara_dict['value'] = index
										restaurant_data["area_detail"].append(ara_dict)
								else:
									pass
								self.customer_nearest_restaurent.append(restaurant_data)
			else:
				pass
			if len(self.customer_nearest_restaurent) == 0:
				return Response({
					"status": True,
				   "message": "Sorry, we do not currently deliver in your location.",
				})

	def post(self,request):
		from Outlet.models import OutletMilesRules
		try:
			self.latitude = request.data['latitude']
			self.longitude = request.data['longitude']
			companies = Company.objects.filter(api_key=request.data["api_key"])
			if companies.count():
				self.Company = companies[0].id
				company_check = Company.objects.filter(id=self.Company,active_status=1)
				if company_check.count()==0:
					return Response({"success"  : False,
									"message" : "Company is not active!!",
									})
				else:
					pass
				company_check = Company.objects.filter(id=self.Company,is_open=1)
				if company_check.count()==0:
					return Response({"success"  : False,
									"message" : "Sorry we are closed now!!",
									})
				else:
					pass
				outlet_data = OutletProfile.objects.filter(Company_id=self.Company)
				if outlet_data.count()==0:
					return Response({"success"  : False,
									"message" : "No outlet is linked to company!!",
									})
				else:
					pass
				if self.longitude != "" and self.longitude != "":
					time = datetime.time(datetime.now())
					chk_com = OutletProfile.objects.filter(active_status=1,is_open=1,\
						Company=self.Company).order_by('latitude')
					if chk_com.count() > 0:
						pass
					else:
						return Response({"success": False,
										"message": "Outlet is closed or inactive!!",
									})
					a = self.restaurant_details_records()
					if a == "s":
						return Response({"success": False,
										"message": "Restaurants is closed",
										})
					else:
						pass
					if a == "Q":
						return Response({"success": False,
										"message": "Outlet timing is not set",
										})
					if self.customer_nearest_restaurent:
						for i in self.customer_nearest_restaurent:
							outlet_id = i['id']
						outlet_data = OutletProfile.objects.filter(id=outlet_id)
						if outlet_data.count() > 0:
							cid = outlet_data[0].Company_id
							name = outlet_data[0].Company.company_name
							save_wev = WebsiteStatistic.objects.create(name=name,\
							menu_views=1,company_id=cid)
						return_json_response = {
							"success": True,
							"nearest_restaurants": self.customer_nearest_restaurent,
							"message": "Your nearest restaurant are send successfully"
						}
						return Response(return_json_response)
					
					return Response({"success": False,
									"message": "Sorry, we do not currently deliver in your location.",
									"range"  : self.range_in_kilometer})
				else:
					pass
			return Response({"message" : "Invalid API Key. No Company found with api key"},status=status.HTTP_404_NOT_FOUND)		
		except Exception as e:
			print(e)
