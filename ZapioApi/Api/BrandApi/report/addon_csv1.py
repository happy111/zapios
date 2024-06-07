from datetime import datetime
import requests
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_tracking.mixins import LoggingMixin
from rest_framework import serializers
from django.http import HttpResponse
from Orders.models import Order,OrderStatusType
from rest_framework.permissions import IsAuthenticated
import dateutil.parser
from Brands.models import Company
from Outlet.models import OutletProfile
from datetime import datetime, timedelta

from datetime import datetime, timedelta
from Product.models import Product,ProductCategory,Variant,Addons,AddonDetails

class Addoncsv(APIView):
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
			data = Addons.objects.filter(Company_id=1)
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
				("ID", 3000),
				("Addon Name", 3000),
				("Addon Price", 3000),
				("Addon Group Name",3000),
				("Addon Group Status",3000),
				("Addon Group Id",3000),
				("Varient Name",3000),
				("Varient ID",3000)
			]

			font_style = xlwt.XFStyle()
			font_style.font.bold = True
			for col_num in range(len(columns)):
				ws.write(row_num, col_num, columns[col_num][0], font_style)
				ws.col(col_num).width = columns[col_num][1]

			font_style = xlwt.XFStyle()
			font_style.alignment.wrap = 1


			q_count = data.count()
			ord_data =[]  
			if q_count > 0:
				for i in data:
					alls = {}
					a = i.name
					if a in ord_data:
						print("ffffffffffff")
					else:
						alls['id'] = i.id
						alls['name'] = i.name
						alls['price'] = i.addon_amount
						alls['gr'] = i.addon_group_id
					ord_data.append(alls)

			# print("hhhhhhhhhhhhhhhhhhhhhh",ord_data)
			for obj in ord_data:
				row_num += 1
				addon_group_name = AddonDetails.objects.filter(id=str(obj['gr']))[0].addon_gr_name
				st = AddonDetails.objects.filter(id=str(obj['gr']))[0].active_status
				v = AddonDetails.objects.filter(id=str(obj['gr']))[0].product_variant_id
				vn = Variant.objects.filter(id=v)
				if vn.count() > 0:
					a = vn[0].id
					b = vn[0].variant
				else:
					b = 'N/A'
					a ='N/A'
				if st == 0:
					s = "Inactive"
				else:
					s = "Active"
				row = [
					obj['id'],
					obj['name'],
					obj['price'],
					addon_group_name,
					s,
					str(obj['gr']),
					b,
					a
				]
				# print(row)
				for col_num in range(len(row)):
					ws.write(row_num, col_num, row[col_num], font_style)
			wb.save(response)
			return response

