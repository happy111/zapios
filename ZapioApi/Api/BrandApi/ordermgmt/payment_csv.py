import requests
import dateutil.parser

from datetime import datetime
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_tracking.mixins import LoggingMixin
from rest_framework import serializers
from django.http import HttpResponse
from Orders.models import Order,OrderStatusType,OrderTracking
from rest_framework.permissions import IsAuthenticated
from Brands.models import Company
from Outlet.models import OutletProfile
from rest_framework.authtoken.models import Token
from UserRole.models import ManagerProfile
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user

from datetime import datetime, timedelta
from django.db.models import Count, Sum, Max, Avg, Case, When, Value, IntegerField, BooleanField
from Configuration.models import PaymentMethod

class PaymentReportCsv(APIView):
	"""
	Payment Csv data GET API

		Authentication Required		: Yes
		Service Usage & Description	: .Download Payment csv file

		Data Post: {
		}

		Response: {

		}

	"""
	# permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
			s_date = request.GET.get('start_date')
			e_date = request.GET.get('end_date')
			start_date = dateutil.parser.parse(s_date)
			end_date = dateutil.parser.parse(e_date)
			token = request.GET.get('token')
			user = Token.objects.filter(key=token)[0].user_id
			st = request.GET.get('outlet_id')
			outletss = list(st.split(",")) 
			cid = get_user(user)
			import xlwt
			response = HttpResponse(content_type='application/ms-excel')
			response['Content-Disposition'] = 'attachment; filename=payment_report.xls'
			wb = xlwt.Workbook(encoding='utf-8')
			ws = wb.add_sheet("payment_report")
			ws.write(0, 0, 'Start Date',xlwt.easyxf('align:horiz centre; pattern: pattern solid, fore_color orange;  font: color white,bold on,height 200'))
			ws.write(0, 1, s_date)
			ws.write(0, 2, 'End Date',xlwt.easyxf('align:horiz centre; pattern: pattern solid, fore_color orange;  font: color white,bold on,height 200'))
			ws.write(0, 3, e_date)


			font_style = xlwt.XFStyle()
			font_style.font.bold = True
			pattern = xlwt.Pattern()
			pattern.pattern = xlwt.Pattern.SOLID_PATTERN
			pattern.pattern_fore_colour = xlwt.Style.colour_map['blue']  # Set the cell background color to yellow
			font_style.pattern = pattern
			font_style = xlwt.XFStyle()
			font_style.alignment.wrap = 1
			date_format = xlwt.XFStyle()
			date_format.num_format_str = 'dd/mm/yyyy'
			row_num = 2
			columns = [
				("Outlet", 9000),
				("Orders", 3000),
				("COD", 3000),
				("COD ORDERS", 4000),
				("GOOGLE PAY", 4000),
				("GOOGLE PAY ORDERS", 5000),
				("ONLINE PAID", 4000),
				("ONLINE PAID ORDERS", 5500),
				("PAYTM", 3000),
				("PAYTM ORDERS", 4000),
				("RAZORPAY", 3000),
				("RAZORPAT_ORDERS", 5000),
				("PAYU", 3000),
				("PAYU_ORDERS", 4000),
				("UPI", 3000),
				("UPI ORDERS", 4000),
				("EDC MACHINE", 4000),
				("EDC MACHINE ORDERS", 5500),
				("SWIGGY ONLINE", 4000),
				("SWIGGY ONLINE ORDERS", 6000),
				("Z0MATO ONLINE", 4000),
				("Z0MATO ONLINE ORDERS", 6500),
				("TOTAL ORDERS AMOUNT", 6000),
			]

			font_style = xlwt.XFStyle()
			font_style.font.bold = True
			for col_num in range(len(columns)):
				ws.write(row_num, col_num, columns[col_num][0], font_style)
				ws.col(col_num).width = columns[col_num][1]
			font_style = xlwt.XFStyle()
			font_style.alignment.wrap = 1
			# outlet = outlet
			orderdata = []

			que = Order.objects.filter(Q(order_time__lte=end_date),Q(order_time__gte=start_date),\
									Q(Company=cid)).distinct('outlet')
			orderdata = []
			for j in outletss:
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
						adata['google_count'] = 0

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

											if pmode == 'Google Pay':
												c = k['amount']
												adata['google_pay'] = round(adata['google_pay'] + float(c),2)
												adata['google_count'] = adata['google_count'] + 1
											else:
												pass

											if pmode == 'Online Paid':
												c = k['amount']
												adata['online_paid'] = round(adata['online_paid'] + float(c),2)
												adata['online_paid_count'] = adata['online_paid_count'] + 1
											else:
												pass

											if pmode == 'PayTm':
												c = k['amount']
												adata['paytm'] = round(adata['paytm'] + float(c),2)
												adata['paytm_count'] = adata['paytm_count'] + 1
											else:
												pass

											if pmode == 'PayU':
												c = k['amount']
												adata['payu'] = round(adata['payu'] + float(c),2)
												adata['payu_count'] = adata['payu_count'] + 1
											else:
												pass
									



									adata['total_amount'] = adata['cod']+ \
															adata['razorpay'] +\
															adata['upi']+\
															adata['edc_machine']+\
															adata['zonline']+\
															adata['sonline']+\
															adata['google_pay']+\
															adata['online_paid']+\
															adata['paytm']+\
															adata['payu']

									adata['order_count'] = adata['cod_count']+ \
															adata['razorpay_count'] +\
															adata['upi_count']+\
															adata['edc_machine_count']+\
															adata['zonline_count']+\
															adata['sonline_count']+\
															adata['google_count']+\
															adata['online_paid_count']+\
															adata['paytm_count']+\
															adata['payu_count'] 
						
						orderdata.append(adata)
				else:
					pass

			for i in orderdata:
				Orders = i['order_count']

				total_amount = i['total_amount']
				sn = 0
				sno= 0
				zo = 0
				zoo = 0
				row_num += 1
				row = [
						i['outlet_name'],
						Orders,
						i['cod'],
						i['cod_count'],
						i['google_pay'],
						i['google_count'],
						i['online_paid'],
						i['online_paid_count'],
						i['paytm'],
						i['paytm_count'],
						i['razorpay'],
						i['razorpay_count'],
						i['payu'],
						i['payu_count'],
						i['upi'],
						i['upi_count'],
						i['edc_machine'],
						i['edc_machine_count'],
						i['sonline'],
						i['sonline_count'],
						i['zonline'],
						i['zonline_count'],
						total_amount

				]
				for col_num in range(len(row)):
					ws.write(row_num, col_num, row[col_num], font_style)
			wb.save(response)
			return response

			