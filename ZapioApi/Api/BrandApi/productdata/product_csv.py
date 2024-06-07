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
from Product.models import Product,ProductCategory,Variant
from urbanpiper.models import *
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user
from Configuration.models import Tax


class ProductReportCsv(APIView):
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
			data = Order.objects.filter(Q(order_time__lte=end_date),Q(order_time__gte=start_date)
					,Q(Company=cid)).order_by('-order_time')
			import xlwt
			response = HttpResponse(content_type='application/ms-excel')
			response['Content-Disposition'] = 'attachment; filename=product_reports.xls'
			wb = xlwt.Workbook(encoding='utf-8')
			ws = wb.add_sheet("product_reports")
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
			row_num = 3
			columns = [
				("Product Name", 12000),
				("Sum of quantity", 4000),
				("Sum of Total Price", 5000),
				("Product Mix (%)", 4000),
				("Sales Mix (%)", 3000),
			]
			font_style = xlwt.XFStyle()
			font_style.font.bold = True
			for col_num in range(len(columns)):
				ws.write(row_num, col_num, columns[col_num][0], font_style)
				ws.col(col_num).width = columns[col_num][1]
			font_style = xlwt.XFStyle()
			font_style.alignment.wrap = 1
			ord_data =[]  
			tprice = 0
			if data.count() > 0:
				for i in data:
					p_list = {}
					if i.order_description != None:
						for j in i.order_description:
							tprice = tprice + j['price']
							alls = {}
							if 'name' in j:
								if len(ord_data) > 0:
									flag = 0
									for index in ord_data:
										if index['product_name'] == j['name']:
											flag = 1
											index['quantity'] = int(j['quantity']) + int(index['quantity'])
											index['price'] = index['quantity'] * float(j['price'])
										else:
											pass
									if flag == 0:
										alls['product_name'] = j['name']
										alls['quantity'] = j['quantity']
										alls['price']    = j['price']
										alls['sprice'] = j['price']
								else:
									alls['sprice'] = j['price']
									alls['product_name'] = j['name']
									if 'quantity' in j:
										alls['quantity'] = j['quantity']
									if 'price' in j:
										alls['price'] = j['price']
							if len(alls):
								ord_data.append(alls)
			tp = 0
			qty = 0
			for obj in ord_data:
				qty = qty + obj['quantity']
				totalprice = obj['quantity'] * float(obj['sprice'])
				tp = tp + totalprice
			
			ws.write(0, 0, 'Start Date')
			ws.write(0, 1, s_date)
			ws.write(0, 2, 'End Date')
			ws.write(0, 3, e_date)


			ws.write(1, 0, 'Grand Total',)
			ws.write(1, 1, qty)
			ws.write(1, 2, tp)
			ws.write(1, 3, 1)
			ws.write(1, 4, 1)
			for obj in ord_data:
				row_num += 1
				pm = round(100 / qty * int(obj['quantity']),3)
				sm = round(100 / tp * int(obj['price']),3)
				totalprice = obj['quantity'] * float(obj['sprice'])
				tp = tp + totalprice
				row = [
					obj['product_name'],
					obj['quantity'],
					totalprice,
					pm,
					sm
				]
				for col_num in range(len(row)):
					ws.write(row_num, col_num, row[col_num], font_style)
			wb.save(response)
			return response


