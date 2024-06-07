from datetime import datetime
import requests
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_tracking.mixins import LoggingMixin
import dateutil.parser
from rest_framework import serializers
from django.http import HttpResponse
from Orders.models import Order,OrderStatusType
from rest_framework.permissions import IsAuthenticated
from Brands.models import Company
from Outlet.models import OutletProfile
from datetime import datetime, timedelta
from datetime import datetime, timedelta
from Product.models import Product,ProductCategory,Variant
from rest_framework.authtoken.models import Token
from UserRole.models import ManagerProfile
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user


class AddonReportCsv(APIView):
	"""
	Product Report  data GET API

		Authentication Required		: Yes
		Service Usage & Description	: .Download Product csv file

		Data Post: {
		}

		Response: {

			"success": True, 
			"message": "Product Report Download api worked well!!",
			"data": final_result
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
			cid = get_user(user)
			data = Order.objects.filter(Q(order_time__lte=e_date),Q(order_time__gte=s_date)
					,Q(Company=cid)).order_by('-order_time')
			import xlwt
			response = HttpResponse(content_type='application/ms-excel')
			response['Content-Disposition'] = 'attachment; filename=addon_reports.xls'
			wb = xlwt.Workbook(encoding='utf-8')
			ws = wb.add_sheet("addon_reports")
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
			font_style = xlwt.XFStyle()
			font_style.alignment.wrap = 1
			date_format = xlwt.XFStyle()
			date_format.num_format_str = 'dd/mm/yyyy'
			row_num = 0
			columns = [
				("id", 3000),
				("Add On Name", 3000),
				("Sold Quantity", 3000),
				("Price", 3000),
				("Outlet", 3000),
				("Invoice No", 3000),
				("Source", 3000),
				("Order_Date", 3000),
				("Order_Time", 3000),
				("Is canceled", 3000),
			]
			font_style = xlwt.XFStyle()
			font_style.font.bold = True
			for col_num in range(len(columns)):
				ws.write(row_num, col_num, columns[col_num][0], font_style)
				ws.col(col_num).width = columns[col_num][1]
			font_style = xlwt.XFStyle()
			font_style.alignment.wrap = 1
			ord_data =[]  
			ord_data1 =[]  
			ord_data3 = []
			q_count = data.count()
			if q_count > 0:
				for i in data:
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
										if 'final_addon_id' in p:
											alls['id']  = p['final_addon_id']
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
										chk_cancel = i.order_status_id
										if str(chk_cancel) == str(7):
											alls['c_canel'] = 'Yes'
										else:
											alls['c_canel'] = 'No'
										o = i.order_time
										o_time = o+timedelta(hours=5,minutes=30)
										alls['time'] = str(o_time.strftime("%I:%M %p"))
										alls['dt'] = str(o_time.strftime("%d/%b/%y"))
										alls['outlet'] =  OutletProfile.objects.filter(id=i.outlet_id)[0].Outletname
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
										if 'add_on_id' in p:
											alls['id']  = p['add_on_id']
										else:
											pass
										if 'addon_id' in p:
											alls['id']  = p['addon_id']
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
										chk_cancel = i.order_status_id
										if str(chk_cancel) == str(7):
											alls['c_canel'] = 'Yes'
										else:
											alls['c_canel'] = 'No'
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
			for obj in ord_data3:
				if 'order_id' in obj:
					order_id = obj['order_id']
				else:
					order_id = 'N/A'
				if 'addon_name' in obj:
					addon_name = obj['addon_name']
				else:
					addon_name = 'N/A'
				if 'id' in obj:
					ids = obj['id']
				else:
					ids = 'N/A'
				if 'quantity' in obj:
					quantity = obj['quantity']
				else:
					quantity = 'N/A'
				if 'price' in obj:
					price = obj['price']
				else:
					price = 'N/A'
				if 'source' in obj:
					source = obj['source']
				else:
					source = 'N/A'
				if 'outlet' in obj:
					outlet_name = obj['outlet']
				else:
					outlet_name = 'N/A'
				t = obj['time']
				d = obj['dt']
				canc = obj['c_canel']
				row_num += 1
				row = [
					ids,
					addon_name,
					quantity,
					price,
					outlet_name,
					order_id,
					source,
					d,
					t,
					canc
				]
				for col_num in range(len(row)):
					ws.write(row_num, col_num, row[col_num], font_style)
			wb.save(response)
			return response



