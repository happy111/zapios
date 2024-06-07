import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from ZapioApi.Api.BrandApi.profile.profile import CompanySerializer
from Brands.models import Company

#Serializer for api
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
from UserRole.models import * 
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import RetrievalData
from ZapioApi.api_packages import *
import dateutil.parser
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user
from django.db.models import Count, Sum, Max, Avg, Case, When, Value, IntegerField, BooleanField
from Configuration.models import *
from Customers.models import CustomerProfile


class OrderListingData(APIView):
	"""
	Order listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for providing listing all order of brand.
	"""
	permission_classes = (IsAuthenticated,)
	def get(self, request):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			brand_id = request.GET.get('brand')
			user = request.user
			co_id = ManagerProfile.objects.filter(auth_user_id=user.id)[0].Company_id
			staff_data = ManagerProfile.objects.filter(auth_user_id=user.id,Company_id=co_id)
			if len(brand_id) > 0:
				brand = list(brand_id.split(","))
				finaloutlet = []
				for index in brand:
					co_id = ManagerProfile.objects.filter(mobile=staff_data[0].mobile,Company_id=index)
					if co_id.count() > 0:
						for temp in co_id[0].outlet:
							finaloutlet.append(temp)
					else:
						pass
			else:
				outlet_data = ManagerProfile.objects.filter(auth_user_id=user.id)
				outlet = outlet_data[0].outlet
				finaloutlet = []
				for index in outlet:
					if index in finaloutlet:
						pass
					else:
						finaloutlet.append(index)
			now = datetime.now()
			today = now.date()
			ord_data =[]
			#print(finaloutlet)
			for k in finaloutlet:
				co_id =  OutletProfile.objects.filter(id=k)[0].Company_id
				clogo = Company.objects.filter(id=co_id)[0].company_logo
				if clogo !=None:
					domain_name = addr_set()
					full_path = domain_name + str(clogo)
				else:
					full_path = ''
				orderdata = Order.objects.filter(
					Q(order_time__date__gte=today),Q(outlet_id=k)).order_by('-order_time')
				
				for i in orderdata:
					p_list ={}
					add = i.address
					p_list['id'] = i.id
					p_list['urban_detail'] = {}
					if i.is_aggregator == True:
						p_list['urban_detail']['is_aggregator'] = True
						p_list['urban_detail']['urban_order_id'] = i.urban_order_id
						urban_record = UrbanOrders.objects.filter(order_id=i.urban_order_id)
						p_list['urban_detail']['next_states'] = urban_record[0].next_states
					else:
						p_list['urban_detail']['is_aggregator'] = False
						p_list['urban_detail']['urban_order_id'] = "N/A"
						p_list['urban_detail']['next_states'] = "N/A"
					p_list['delivery_address'] = i.address
					p_list['special_instructions'] = i.special_instructions
					p_list['customer'] = i.customer
					p_list['order_id'] = i.outlet_order_id
					p_list['order_status'] = i.order_status_id
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
					
					standard_acceptance_time = 60
					standard_processing_time = 120
					standard_dispatch_time  = 120



					track_order = OrderTracking.objects.filter(Q(order_id=i.id),\
								Q(Order_staus_name_id=1))
					
					# Received Time
					if track_order.count() > 0:
						o = track_order[0].created_at
						q = o+timedelta(hours=5,minutes=30)
						s = q.time()
						a = str(s).split('.')
						frd = a[0]
					else:
						frd = 1

					# Accepted Time
					atimes = OrderTracking.objects.filter(Q(order_id=i.id),\
									Q(Order_staus_name_id=2))
					
					if atimes.count() > 0:
						o = atimes[0].created_at
						q = o+timedelta(hours=5,minutes=30)
						s = q.time()
						a = str(s).split('.')
						act = a[0]
					else:
						act = 'N/A'

					# Food Ready
					fready = OrderTracking.objects.filter(Q(order_id=i.id),\
									Q(Order_staus_name_id=3))
					if fready.count() > 0:
						o = fready[0].created_at
						q = o+timedelta(hours=5,minutes=30)
						s = q.time()
						a = str(s).split('.')
						fredy = a[0]
					else:
						fredy = 'N/A'

					# Dispatch
					disp = OrderTracking.objects.filter(Q(order_id=i.id),\
									Q(Order_staus_name_id=4))
					if disp.count() > 0:
						o = disp[0].created_at
						q = o+timedelta(hours=5,minutes=30)
						s = q.time()
						a = str(s).split('.')
						dredy = a[0]
					else:
						dredy = 'N/A'






					# Calculate Accepted Time
					if track_order.count() > 0 and atimes.count() > 0:
						date_format = "%H:%M:%S"
						t1 = datetime.strptime(str(frd),date_format)
						t2 = datetime.strptime(str(act),date_format)
						dif = t2 - t1
						sec = dif.total_seconds()
						if 	p_list['order_status'] == 2:
							### Calculate super value
							acceptance_pto = int(standard_acceptance_time) - int(sec)
							s =  standard_acceptance_time * 30 / 100
							flag = acceptance_pto > s
							if flag == True:
								p_list['color'] = 'blue'
							
							### Calculate good value
							st = standard_acceptance_time * 0 / 100
							acceptance_pto = int(standard_acceptance_time) - int(sec)
							s =  standard_acceptance_time * 30 / 100
							g =  st < acceptance_pto < (standard_acceptance_time * 30 / 100)

							if g == True:
								p_list['color'] = 'green'
							
							### Calculate Yellow value
							acceptance_pto = int(standard_acceptance_time) - int(sec)
							st = standard_acceptance_time * 0 / 100
							y = standard_acceptance_time * -30 / 100
							acceptance_pto = int(standard_acceptance_time) - int(sec)
							yc = st > acceptance_pto > y
							if yc == True:
								p_list['color'] = 'yellow'
							
							### Calculate Warning value
							acceptance_pto = int(standard_acceptance_time) - int(sec)
							st = standard_acceptance_time * 0 / 100
							y = standard_acceptance_time * -30 / 100
							acceptance_pto = int(standard_acceptance_time) - int(sec)
							ycc = acceptance_pto < y
							if ycc == True:
								p_list['color'] = 'red'

					else:
						pass
					
					# Calculate Processing Time
					if fready.count() > 0 and atimes.count() > 0:
						date_format = "%H:%M:%S"
						t1 = datetime.strptime(str(act),date_format)
						t2 = datetime.strptime(str(fredy),date_format)
						f = t2 - t1
						sec = f.total_seconds()
						if 	p_list['order_status'] == 3:
							### Calculate super value
							processing_pto = int(standard_processing_time) - int(sec)
							s =  standard_processing_time * 15 / 100
							flag = processing_pto > s 
							if flag == True:
								p_list['color'] = 'blue'

							### Calculate good value
							processing_pto = int(standard_processing_time) - int(sec)
							st = standard_processing_time * 0 / 100
							s =  standard_processing_time * 15 / 100
							g =  st < processing_pto < s
							if g == True:
								p_list['color'] = 'green'
							
							### Calculate Yellow value
							processing_pto = int(standard_processing_time) - int(sec)
							st = standard_processing_time * 0 / 100
							y = standard_processing_time * -15 / 100
							acceptance_pto = int(standard_acceptance_time) - int(sec)
							yc = st > processing_pto > y
							if yc == False:
								p_list['color'] = 'yellow'
							
							### Calculate Warning value
							processing_pto = int(standard_processing_time) - int(sec)
							st = standard_processing_time * 0 / 100
							y = standard_processing_time * -15 / 100
							yc = processing_pto < y
							if yc == False:
								p_list['color'] = 'red'
					else:
						pass


					# Calculate dispatch Time
					if fready.count() > 0 and disp.count() > 0:
						date_format = "%H:%M:%S"
						t1 = datetime.strptime(str(fredy),date_format)
						t2 = datetime.strptime(str(dredy),date_format)
						f = t2 - t1
						sec = f.total_seconds()
						if 	p_list['order_status'] == 4:
							### Calculate super value
							dispatch_pto = int(standard_dispatch_time) - int(sec)
							s =  standard_dispatch_time * 20 / 100
							flag = dispatch_pto > s 
							if flag == True:
								p_list['color'] = 'blue'

							### Calculate good value
							dispatch_pto = int(standard_dispatch_time) - int(sec)
							st = standard_dispatch_time * 0 / 100

							s =  standard_dispatch_time * 20 / 100
							g =  st < dispatch_pto < s
							if g == True:
								p_list['color'] = 'green'
							
							### Calculate Yellow value
							dispatch_pto = int(standard_dispatch_time) - int(sec)
							st = standard_dispatch_time * 0 / 100
							y = standard_dispatch_time * -20 / 100
							acceptance_pto = int(standard_acceptance_time) - int(sec)
							yc = st > dispatch_pto > y
							if yc == False:
								p_list['color'] = 'yellow'
							
							### Calculate Warning value
							dispatch_pto = int(standard_dispatch_time) - int(sec)
							st = standard_dispatch_time * 0 / 100
							y = standard_dispatch_time * -20 / 100
							yc = st < y
							if dispatch_pto == False:
								p_list['color'] = 'red'
					else:
						pass


					# print("mmmmmmmmmmmmmmmmmmm",p_list['color'])
					full_path = addr_set()
					if i.order_source.image != None and i.order_source.image != "":
						p_list['pic'] = full_path+str(i.order_source.image)
					else:
						p_list['pic'] = ''
					o_time = i.order_time+timedelta(hours=5,minutes=30)
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
						if i.order_source.source_name == 'Website Order':
							p_list["payment_mode"] = i.payment_mode
						else:
							p_list["payment_mode"] = ""
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
					pdata = DeliverySetting.objects.filter(company_id=co_id)
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
					else:
						pass


					ord_data.append(p_list)
			return Response({"status":True,
							"orderdata":ord_data})
		except Exception as e:
			print(e)
			return Response(
						{"error":str(e)}
						)

	
	permission_classes = (IsAuthenticated,)
	def post(self, request):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			err_message = {}
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
			outlet = data['outlet_id']
			cid = OutletProfile.objects.filter(id=outlet[0])[0].Company_id
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
				print("vvvvvvvvvvvvvvv",outlet)
				for i in outlet:
					querydata = query.filter(outlet_id=i).order_by('-order_time')
					orderdatas = que.filter(outlet_id=i)
					res = res1.filter(outlet_id=i)
					csale = csale1.filter(outlet_id=i)
					c_item = c_item1.filter(outlet_id=i)
					s_order = settle_order.filter(outlet_id=i)
					cod = 0 
					cod_count = 0
					google_pay = 0
					google_pay_count = 0
					online_paid = 0
					online_paid_count = 0
					paytm = 0
					paytm_count = 0
					razorpay = 0
					razorpay_count = 0
					payu = 0
					payu_count = 0
					upi = 0
					upi_count = 0
					edc_machine = 0
					edc_machine_count = 0
					zonline = 0
					zonline_count = 0
					sonline = 0
					sonline_count = 0
					total_amount =0
					order_count =0
					for i in querydata:
						print(i.id)
						p_list ={}
						if i.settlement_details !=None and len(i.settlement_details) > 0:
							k = 1
							for k in i.settlement_details:
								pdata = PaymentMethod.objects.filter(id=k['mode'])
								if pdata.count() > 0:
									pmode = pdata[0].payment_method
									if pmode == 'Swiggy Online':
										c = k['amount']
										sonline = round(sonline + float(c),2)
										sonline_count = sonline_count + 1
									else:
										pass
									if pmode == 'Zomato Online':
										c = k['amount']
										zonline = round(zonline + float(c),2)
										zonline_count = zonline_count + 1
									else:
										pass
									if pmode == 'EDC Machine':
										c = k['amount']
										edc_machine = round(edc_machine + float(c),2)
										edc_machine_count = edc_machine_count + 1
									else:
										pass
									if pmode == 'UPI':
										c = k['amount']
										upi = round(upi + float(c),2)
										upi_count = upi_count + 1
									else:
										pass
									if pmode == 'Razorpay':
										c = k['amount']
										razorpay = round(razorpay + float(c),2)
										razorpay_count = razorpay_count + 1
									else:
										pass
									if pmode == 'Cash':
										c = k['amount']
										cod = round(cod + float(c),2)
										cod_count = cod_count + 1
									else:
										pass
									if pmode == 'Online Paid':
										c = k['amount']
										online_paid = round(online_paid + float(c),2)
										online_paid_count = online_paid_count + 1
									else:
										pass
									if pmode == 'PayU':
										c = k['amount']
										payu = round(payu + float(c),2)
										payu_count = payu_count + 1
									else:
										pass
									if pmode == 'Paytm':
										c = k['amount']
										paytm = round(paytm + float(c),2)
										paytm_count = paytm_count + 1
									else:
										pass
						else:
							print("ddddddddddddddddd",i.id)
						add = i.address
						p_list['id'] = i.id
						p_list['order_id'] = i.outlet_order_id
						p_list['order_status'] = i.order_status_id
						p_list['discount_value'] = i.discount_value
						p_list['order_source'] = i.order_source.source_name
						p_list['sub_total'] = i.sub_total
						p_list['distance'] = i.distance
						p_list['customer'] = []
						if i.users_id != None:
							customer_data = CustomerProfile.objects.filter(id=i.users_id)
							if customer_data.count() > 0:
								customer_temp = {}
								customer_temp['mobile'] = customer_data[0].mobile
								customer_temp['name'] = customer_data[0].first_name
								customer_temp['email'] = customer_data[0].email
								customer_temp['address'] = customer_data[0].address
								p_list['customer'].append(customer_temp)
						p_list['total_bill_value'] = i.total_bill_value
						o_time = i.order_time+timedelta(hours=5,minutes=30)
						p_list['order_time'] = o_time.isoformat()
						p = i.delivery_time
						if p != None:
							d_time = i.delivery_time+timedelta(hours=5,minutes=30)
							p_list['delivery_time'] = d_time.isoformat()
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
								try:
									pm = PaymentMethod.objects.filter(id=i.payment_mode)
									if pm.count() > 0:
										p_list['payment_mode'] = pm[0].payment_method
									else:
										p_list['payment_mode'] = ''
								except Exception as e:
									p_list['payment_mode'] = i.payment_mode

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
							"totalorder"     : totalsettleorder,
							"cod" : cod,
							"cod_count" : cod_count,
							"google_pay" : google_pay,
							"google_pay_count": google_pay_count,
							"online_paid": online_paid,
							"online_paid_count" : online_paid_count,
							"paytm" : paytm,
							"paytm_count" : paytm_count,
							"razorpay" : razorpay,
							"razorpay_count" : razorpay_count,
							"payu" : payu,
							"payu_count" : payu_count,
							"upi" : upi,
							"upi_count" : upi_count,
							"edc_machine" : edc_machine,
							"edc_machine_count" : edc_machine_count,
							"zonline" : zonline,
							"zonline_count" :zonline_count,
							"sonline" : sonline,
							"sonline_count" : sonline_count
						
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






