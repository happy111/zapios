from datetime import datetime
import requests
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_tracking.mixins import LoggingMixin
from rest_framework import serializers
from django.http import HttpResponse
from pos.models import POSOrder


class Customercsv(APIView):
	"""
	Custopmer data GET API

		Authentication Required		: Yes
		Service Usage & Description	: .Download Customer csv file

		Data Post: {
		}

		Response: {

			"success": True, 
			"message": "Dashboard card analysis api worked well!!",
			"data": final_result
		}

	"""
	def get(self, request, format=None):
			data = POSOrder.objects.all()
			import xlwt
			response = HttpResponse(content_type='application/ms-excel')
			response['Content-Disposition'] = 'attachment; filename=customer_report.xls'
			wb = xlwt.Workbook(encoding='utf-8')
			ws = wb.add_sheet("Customer_report")

			row_num = 0

			columns = [
				("S.No", 2000),
				("Customer Name", 2000),
				("Customer Number", 2000),
				("Discount Value", 8000),
				("External_id", 10000),
				("ids", 2000),
				("Invoice Number", 2000),
				("Order Type", 2000),
				("Outlet", 2000),
				("Payment Mode", 2000),
				("Ride Name", 2000),
				("Rider Number", 2000),
				("Source", 2000),
				("Status Name", 8000),
				("Sub_total", 10000),
				("Total", 2000),
				("Total_tax", 2000),
			]

			font_style = xlwt.XFStyle()
			font_style.font.bold = True

			for col_num in range(len(columns)):
				ws.write(row_num, col_num, columns[col_num][0], font_style)
				# set column width
				ws.col(col_num).width = columns[col_num][1]

			font_style = xlwt.XFStyle()
			font_style.alignment.wrap = 1

			for obj in data:
				row_num += 1
				row = [
					row_num,
					obj.customer_name,
					obj.customer_number,
					obj.discount_value,
					obj.external_id,
					obj.ids,
					obj.invoice_number,
					obj.order_type,
					obj.outlet,
					obj.payment_mode,
					obj.rider_name,
					obj.rider_number,
					obj.source,
					obj.status_name,
					obj.sub_total,
					obj.total,
					obj.total_tax

				]
				for col_num in range(len(row)):
					ws.write(row_num, col_num, row[col_num], font_style)

			wb.save(response)
			return response

# class SearchResultSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = POSOrder
# 		fields = '__all__' 


# def export_xls():
# 	data = POSOrder.objects.all()
# 	import xlwt
# 	response = HttpResponse(content_type='application/ms-excel')
# 	response['Content-Disposition'] = 'attachment; filename=SearchResult.xls'
# 	wb = xlwt.Workbook(encoding='utf-8')
# 	ws = wb.add_sheet("SearchReport")

# 	row_num = 0

# 	columns = [

# 		("Customer Name", 2000),
# 		("Customer Number", 8000),

# 		("Discount Value", 2000),
# 		("External ID", 2000),
# 		("IDS", 2000),
# 		("Invoice Number", 2000),
# 	]

# 	font_style = xlwt.XFStyle()
# 	font_style.font.bold = True

# 	for col_num in range(len(columns)):
# 		ws.write(row_num, col_num, columns[col_num][0], font_style)
# 		ws.col(col_num).width = columns[col_num][1]

# 	font_style = xlwt.XFStyle()
# 	font_style.alignment.wrap = 1

# 	for obj in data:
# 		row_num += 1
# 		row = [
# 			row_num,

# 			obj.customer_name,
# 			obj.customer_number,
		
# 			obj.discount_value,
# 			obj.external_id,
# 			obj.ids,
# 			obj.invoice_number,
# 		]
# 		for col_num in range(len(row)):
# 			ws.write(row_num, col_num, row[col_num], font_style)

# 	wb.save(response)
# 	return response


# # def view_export_xls(request):
# # 	data = SearchResult.objects.all()
# # 	import xlwt
# # 	response = HttpResponse(content_type='application/ms-excel')
# # 	response['Content-Disposition'] = 'attachment; filename=SearchResult.xls'
# # 	wb = xlwt.Workbook(encoding='utf-8')
# # 	ws = wb.add_sheet("SearchReport")

# # 	row_num = 0

# # 	columns = [
# # 		("S.No", 2000),
# # 		("Channel Id", 2000),
# # 		("Title", 8000),
# # 		("Description", 10000),
# # 		("Video Id", 2000),
# # 		("Views", 2000),
# # 		("Likes", 2000),
# # 		("Dislikes", 2000),
# # 	]

# # 	font_style = xlwt.XFStyle()
# # 	font_style.font.bold = True

# # 	for col_num in range(len(columns)):
# # 		ws.write(row_num, col_num, columns[col_num][0], font_style)
# # 		# set column width
# # 		ws.col(col_num).width = columns[col_num][1]

# # 	font_style = xlwt.XFStyle()
# # 	font_style.alignment.wrap = 1

# # 	for obj in data:
# # 		row_num += 1
# # 		row = [
# # 			row_num,
# # 			obj.pk,
# # 			obj.channelId,
# # 			obj.title,
# # 			obj.description,
# # 			obj.video_id,
# # 			obj.viewCount,
# # 			obj.likeCount,
# # 			obj.dislikeCount,
# # 		]
# # 		for col_num in range(len(row)):
# # 			ws.write(row_num, col_num, row[col_num], font_style)

# # 	wb.save(response)
# # 	return Response(response)

