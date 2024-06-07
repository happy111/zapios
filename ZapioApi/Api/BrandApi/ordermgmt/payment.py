from datetime import datetime
import requests
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_tracking.mixins import LoggingMixin
from rest_framework import serializers
from django.http import HttpResponse
from Orders.models import Order,OrderStatusType,OrderTracking
from rest_framework.permissions import IsAuthenticated
import dateutil.parser
from Brands.models import Company
from Outlet.models import OutletProfile
from rest_framework.authtoken.models import Token
from UserRole.models import ManagerProfile

from datetime import datetime, timedelta
from django.db.models import Count, Sum, Max, Avg, Case, When, Value, IntegerField, BooleanField
from ZapioApi.api_packages import *
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user
from Configuration.models import PaymentMethod

class PaymentReport(APIView):
	"""
	Order data GET API

		Authentication Required		: Yes
		Service Usage & Description	: .Download Order csv file

		Data Post: {
			"start_date" :""
			"end_date" : ""
			"outlet_id" : []
		}

		Response: {

			"success": True, 
			"message": "Dashboard card analysis api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
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
			cid = get_user(user)
			outlet = data['outlet_id']
			orderdata = []
			que = Order.objects.filter(Q(order_time__lte=end_date),Q(order_time__gte=start_date),\
									Q(Company=cid)).distinct('outlet')
			
			orderdata = []
			for j in outlet:
				query = que.filter(outlet_id=j)
				if query.count() > 0:
					for i in query:
						adata = {}
						cname = Company.objects.filter(id=cid)[0].company_name
						adata['outlet_id'] = i.outlet_id
						adata['id'] = i.id
						if i.outlet_id != None:
							outlet_name = OutletProfile.objects.filter(id=i.outlet_id)[0].Outletname
							adata['outlet_name'] = str(cname)+' '+str(outlet_name)
						else:
							pass
						pdetail = Order.objects.filter(Q(order_time__lte=end_date),\
														Q(order_time__gte=start_date),\
														Q(Company=cid),\
														Q(outlet_id=i.outlet_id),
														Q(order_status_id=6))
						
						adata['cod'] = 0
						adata['cod_count'] = 0

						adata['google_pay'] = 0
						adata['google_pay_count'] = 0

						adata['online_paid'] = 0
						adata['online_paid_count'] = 0

						adata['paytm'] = 0
						adata['paytm_count'] = 0

						adata['razorpay'] = 0
						adata['razorpay_count'] = 0

						adata['payu'] = 0
						adata['payu_count'] = 0

						adata['upi'] = 0
						adata['upi_count'] = 0

						adata['edc_machine'] = 0
						adata['edc_machine_count'] = 0

						adata['zonline'] = 0
						adata['zonline_count'] = 0

						adata['sonline'] = 0
						adata['sonline_count'] = 0
			

						adata['total_amount'] =0
						adata['order_count'] =0
						
						for j in pdetail:
							if j.settlement_details !=None:
								if len(j.settlement_details) > 0:
									k = 1
									for k in j.settlement_details:
										pdata = PaymentMethod.objects.filter(id=k['mode'])
										if pdata.count() > 0:
											pmode = pdata[0].payment_method
											if pmode == 'Swiggy Online':
												c = k['amount']
												adata['sonline'] = round(adata['sonline'] + float(c),2)
												adata['sonline_count'] = adata['sonline_count'] + 1
											else:
												pass
											if pmode == 'Zomato Online':
												c = k['amount']
												adata['zonline'] = round(adata['zonline'] + float(c),2)
												adata['zonline_count'] = adata['zonline_count'] + 1
											else:
												pass
											if pmode == 'EDC Machine':
												c = k['amount']
												adata['edc_machine'] = round(adata['edc_machine'] + float(c),2)
												adata['edc_machine_count'] = adata['edc_machine_count'] + 1
											else:
												pass
											if pmode == 'UPI':
												c = k['amount']
												adata['upi'] = round(adata['upi'] + float(c),2)
												adata['upi_count'] = adata['upi_count'] + 1
											else:
												pass
											if pmode == 'Razorpay':
												c = k['amount']
												adata['razorpay'] = round(adata['razorpay'] + float(c),2)
												adata['razorpay_count'] = adata['razorpay_count'] + 1
											else:
												pass
											if pmode == 'Cash':
												c = k['amount']
												adata['cod'] = round(adata['cod'] + float(c),2)
												adata['cod_count'] = adata['cod_count'] + 1
											else:
												pass
											if pmode == 'Online Paid':
												c = k['amount']
												adata['online_paid'] = round(adata['online_paid'] + float(c),2)
												adata['online_paid_count'] = adata['online_paid_count'] + 1
											else:
												pass
									adata['total_amount'] = adata['cod']+ \
															adata['razorpay'] +\
															adata['upi']+\
															adata['edc_machine']+\
															adata['zonline']+\
															adata['sonline']+\
															adata['online_paid']
									adata['order_count'] = adata['cod_count']+ \
															adata['razorpay_count'] +\
															adata['upi_count']+\
															adata['edc_machine_count']+\
															adata['zonline_count']+\
															adata['sonline_count']+\
															adata['online_paid_count'] 

						orderdata.append(adata)
				else:
					pass
			if len(orderdata) > 0:
				return Response({
							"success": True,
							"data" : orderdata
							})
			else:
				return Response({
							"success": True,
							"data" : []
							})

		except Exception as e:
			print(e)
			return Response(
						{"error":str(e)}
						)
			
