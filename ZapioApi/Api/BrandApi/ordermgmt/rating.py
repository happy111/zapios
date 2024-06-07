from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime, timedelta
from Orders.models import Order
from rest_framework import serializers
import dateutil.parser
from django.shortcuts import render
from django.http import HttpResponse
import csv
from django.db.models import Q
from rest_framework.authtoken.models import Token
from Brands.models import Company
from UserRole.models import ManagerProfile


class RatingCSV(APIView):
	"""
	Order Csv data GET API

		Authentication Required		: No
		Service Usage & Description	: Download Order csv file

		Data Post: {

		"start_date"    : "2020-04-01",
		"end_date"      : "2020-04-05"
			
		}

		Response: {

		}

	"""
	def get(self, request, format=None):
			s_date = request.GET.get('start_date')
			start_date = dateutil.parser.parse(s_date)
			token = request.GET.get('token')
			user = Token.objects.filter(key=token)[0].user_id
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
			datas = Order.objects.filter(Q(order_time__gte=s_date),Q(Company=cid)).order_by('-order_time')
			import xlwt
			response = HttpResponse(content_type='application/ms-excel')
			response['Content-Disposition'] = 'attachment; filename=rating_report.xls'
			wb = xlwt.Workbook(encoding='utf-8')
			ws = wb.add_sheet("rating_reports")
			font_style = xlwt.XFStyle()
			font_style.font.bold = True
			pattern = xlwt.Pattern()
			pattern.pattern = xlwt.Pattern.SOLID_PATTERN
			row_num = 0
			columns = [
				("S.No", 2000),
				("Outlet Name",8000),
				("Order Id", 4000),
				("Total Bill Value", 4000),
				("Source", 4000),
				("Rating", 4000),
				("Order Time", 6000)
			]
			font_style = xlwt.XFStyle()
			font_style.font.bold = True
			for col_num in range(len(columns)):
				ws.write(row_num, col_num, columns[col_num][0], font_style)
				ws.col(col_num).width = columns[col_num][1]
			font_style = xlwt.XFStyle()
			font_style.alignment.wrap = 1

			for i in datas:
				row_num += 1
				row = [
					row_num,
					i.outlet.Outletname,
					i.order_id,
					i.total_bill_value,
					i.get_payment_mode_display(),
					i.rating,
					(i.order_time).strftime('%Y/%m/%d %H:%M')
				]
				for col_num in range(len(row)):
					ws.write(row_num, col_num, row[col_num], font_style)
			wb.save(response)
			return response