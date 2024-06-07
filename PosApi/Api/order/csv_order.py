import requests
from datetime import datetime
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
from Outlet.models import *
from rest_framework.authtoken.models import Token
from UserRole.models import ManagerProfile
from datetime import datetime, timedelta
from Configuration.models import PaymentMethod



class Ordercsv(APIView):
	"""
	Order data GET API

		Authentication Required		: Yes
		Service Usage & Description	: .Download Order csv file

		Data Post: {
		}

		Response: {

			"success": True, 
			"message": "Dashboard card analysis api worked well!!",
			"data": final_result
		}

	"""
	#permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		s_date = request.GET.get('start_date')
		e_date = request.GET.get('end_date')
		start_date = dateutil.parser.parse(s_date)
		end_date = dateutil.parser.parse(e_date)
		st = request.GET.get('outlet_id')
		outletss = list(st.split(",")) 
		token = request.GET.get('token')
		user = Token.objects.filter(key=token)[0].user_id
		is_cashier = ManagerProfile.objects.filter(auth_user_id=user)
		if is_cashier.count() > 0:
			cid =  OutletProfile.objects.filter(id=outletss[0])[0].Company_id
		else:
			pass
		import xlwt
		response = HttpResponse(content_type='application/ms-excel')
		response['Content-Disposition'] = 'attachment; filename=order_report.xls'
		wb = xlwt.Workbook(encoding='utf-8')
		ws = wb.add_sheet("order_report")
		row_num = 0
		columns = [
			("Order & Invoice Details", 10000),
			("Order Value Details", 10000),
		]
		font_style = xlwt.XFStyle()
		font_style.font.bold = True
		pattern = xlwt.Pattern()
		pattern.pattern = xlwt.Pattern.SOLID_PATTERN
		pattern.pattern_fore_colour = xlwt.Style.colour_map['blue']  # Set the cell background color to yellow
		font_style.pattern = pattern
		ws.write_merge(0, 0, 0, 13, 'Order & Invoice Details',xlwt.easyxf('align:horiz centre; pattern: pattern solid, fore_color gray25;  font: color black,bold on,height 200'))
		ws.write_merge(0, 0, 14, 19, 'Order Value Details',xlwt.easyxf('align:horiz centre; pattern: pattern solid, fore_color orange;  font: color white,bold on,height 200'))
		ws.write_merge(0, 0, 20, 24, 'Order Status Details',xlwt.easyxf('align:horiz centre; pattern: pattern solid, fore_color blue;  font: color white,bold on,height 200'))
		ws.write_merge(0, 0, 25, 26, 'Rider Details',xlwt.easyxf('align:horiz centre; pattern: pattern solid, fore_color orange;  font: color white,bold on,height 200'))
		ws.write_merge(0, 0, 27, 29, 'Payment Modes',xlwt.easyxf('align:horiz centre; pattern: pattern solid, fore_color blue;  font: color white,bold on,height 200'))
		font_style = xlwt.XFStyle()
		font_style.alignment.wrap = 1
		date_format = xlwt.XFStyle()
		date_format.num_format_str = 'dd/mm/yyyy'
		row_num = 1
		columns = [
			("Outlet ID", 3000),
			("Outlet Name", 3000),
			("User", 3000),
			("IP_Invoice", 3000),
			("Order_Date", 3000),
			("Order_Time", 3000,date_format),
			("Order Type", 3000),
			("Customer_Name", 3000),
			("Customer_Contact", 3000),
			("Order_Source", 3000),
			("Order_Value_Subtotal",3000),
			("Total_Discount", 3000),
			("Discount Name", 3000),
			("Discount Reason", 3000),
			("Packaging_Charges", 3000),
			("Service_Charges", 3000),
			("Tax", 3000),
			("Total_Bill_Value", 3000),
			("Order_Status", 3000),
			("Cancellation_Responsible", 3000),
			("Cancellation_Reson", 3000),
			("Received Time", 3000),
			("Accepted in Time", 3000),
			("Food Ready in Time", 3000),
			("Dispatched in Time", 3000),
			("Rider Name", 3000),
			("Mobile", 3000),
			("PAYMENT METHOD", 3000),
			("Transaction ID", 3000),
		]

		font_style = xlwt.XFStyle()
		font_style.font.bold = True
		for col_num in range(len(columns)):
			ws.write(row_num, col_num, columns[col_num][0], font_style)
			ws.col(col_num).width = columns[col_num][1]
		font_style = xlwt.XFStyle()
		font_style.alignment.wrap = 1
		cdata = Order.objects.filter(Q(order_time__lte=e_date),Q(order_time__gte=s_date)
				,Q(Company_id=cid))
		for i in outletss:
			data = cdata.filter(outlet_id=i).order_by('-order_time')
			for obj in data:
				track_order = OrderTracking.objects.filter(Q(order_id=obj.id),\
								Q(Order_staus_name_id=1))
				if track_order.count() > 0:
					o = track_order[0].created_at
					q = o+timedelta(hours=5,minutes=30)
					s = q.time()
					a = str(s).split('.')
					frd = a[0]
				else:
					frd = 'N/A'
				atimes = OrderTracking.objects.filter(Q(order_id=obj.id),\
								Q(Order_staus_name_id=2))
				if atimes.count() > 0:
					o = atimes[0].created_at
					q = o+timedelta(hours=5,minutes=30)
					s = q.time()
					a = str(s).split('.')
					act = a[0]
				else:
					act = 'N/A'
				fready = OrderTracking.objects.filter(Q(order_id=obj.id),\
								Q(Order_staus_name_id=3))
				if fready.count() > 0:
					o = fready[0].created_at
					q = o+timedelta(hours=5,minutes=30)
					s = q.time()
					a = str(s).split('.')
					fredy = a[0]
				else:
					fredy = 'N/A'
				disp = OrderTracking.objects.filter(Q(order_id=obj.id),\
								Q(Order_staus_name_id=4))
				if disp.count() > 0:
					o = disp[0].created_at
					q = o+timedelta(hours=5,minutes=30)
					s = q.time()
					a = str(s).split('.')
					dredy = a[0]
				else:
					dredy = 'N/A'
				if track_order.count() > 0 and atimes.count() > 0:
					date_format = "%H:%M:%S"
					t1 = datetime.strptime(str(frd),date_format)
					t2 = datetime.strptime(str(act),date_format)
					dif = t2 - t1
					sec = dif.total_seconds()
					diff = dif
				else:
					diff = 'N/A'
				if fready.count() > 0 and atimes.count() > 0:
					date_format = "%H:%M:%S"
					t1 = datetime.strptime(str(act),date_format)
					t2 = datetime.strptime(str(fredy),date_format)
					f = t2 - t1
					sec = f.total_seconds()
					#fdiff = sec // 60
					fdiff = f
				else:
					fdiff = 'N/A'
				if fready.count() > 0 and disp.count() > 0:
					date_format = "%H:%M:%S"
					t1 = datetime.strptime(str(fredy),date_format)
					t2 = datetime.strptime(str(dredy),date_format)
					f = t2 - t1
					sec = f.total_seconds()
					ddiff = f
				else:
					ddiff = 'N/A'

				outlet_id = obj.outlet_id
				if outlet_id !=None:
					outlet_name = OutletProfile.objects.filter(id=outlet_id)[0].Outletname
				else:
					outlet_name = 'N/A'
				if obj.is_rider_assign == True:
					if obj.is_aggregator == False:
						ad = DeliveryBoy.objects.filter(id=obj.delivery_boy_id)
						if ad.count() > 0:
							rname = ad[0].name
							rmobile = ad[0].mobile
							remail = 'N/A'
						else:
							rname = 'N/A'
							rmobile = 'N/A'
							remail = 'N/A'
					else:
						r = obj.delivery_boy_details
						if r !=None:
							rname = r['name']
							rmobile = r['mobile']
							remail = r['email']
						else:
							rname = 'N/A'
							rmobile = 'N/A'
							remail = 'N/A'
				else:
					rname = 'N/A'
					rmobile = 'N/A'
					remail = 'N/A'
				if obj.customer !=None:
					user = obj.customer
					if 'first_name' in user:
						users = user['first_name']
					else:
						users = 'N/A'

					if 'mobile' in user:
						mobile = user['mobile']
					else:
						mobile = 'N/A'
				else:
					users = 'N/A'

				if obj.taxes:
					tax = round(obj.taxes / 2,2)
				else:
					tax = 0
				modes = []
				if obj.tax_detail !=None:
					if 'CGST' in obj.tax_detail:
						cgst = obj.tax_detail['CGST']
					else:
						cgst = 0
					if 'SGST' in obj.tax_detail:
						sgst = obj.tax_detail['SGST']
					else:
						sgst = 0
					if 'CESS' in obj.tax_detail:
						cess = obj.tax_detail['CESS']
					else:
						cess = 0
				else:
					cgst = round(obj.taxes / 2,2)
					sgst = round(obj.taxes / 2,2)
					cess = 0
				pm = ''
				if obj.settlement_details !=None:
					if len(obj.settlement_details) > 0:
						for k in obj.settlement_details:
							if k['mode'] !=None:
								p = PaymentMethod.objects.filter(id=k['mode'])
								if p.count() > 0:
									pm = p[0].payment_method
								else:
									pm = ''
							else:
								pass
					else:
						pass
				else:
					pm = obj.payment_mode

				o_time = obj.order_time+timedelta(hours=5,minutes=30)
				order_time = str(o_time.isoformat())
				order_date = str(o_time.isoformat())
				if obj.sub_total != None:
					tv = obj.sub_total
				else:
					tv =0
				if obj.discount_value != None:
					dv = obj.discount_value
				else:
					dv =0
				if obj.packing_charge != None:
					pc = obj.packing_charge
				else:
					pc =0
				if obj.delivery_charge != None:
					dc = obj.delivery_charge
				else:
					dc =0
				Order_Value_Pre_tax = round(float(tv) - float(dv)+\
				  float(pc) + float(dc),2)
				if obj.taxes != None:
					t = obj.taxes
				else:
					t =0

				if obj.sub_total != None:
					ts = obj.sub_total
				else:
					ts =0
				order_GMV =  round(float(ts) + float(t),2)
				or_post_tax = round(Order_Value_Pre_tax + float(t),2)
				dreason = ''
				row_num += 1
				row = [
					outlet_id,
					outlet_name,
					obj.user,
					obj.outlet_order_id,
					order_date,
					order_time,
					obj.order_type,
					users,
					mobile,
					str(obj.order_source),
					obj.sub_total,
					obj.discount_value,
					obj.discount_name,
					obj.discount_reason,
					str(pc),
					str(dc),
					obj.taxes,
					obj.total_bill_value,
					str(obj.order_status),
					obj.cancel_responsibility,
					obj.order_cancel_reason,
					frd,
					str(diff),
					str(fdiff),
					str(ddiff),
					rname,
					rmobile,
					pm,
					obj.transaction_id
				]
				for col_num in range(len(row)):
					ws.write(row_num, col_num, row[col_num], font_style)
		wb.save(response)
		return response

