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
from Outlet.models import *
from rest_framework.authtoken.models import Token
from UserRole.models import ManagerProfile
from datetime import datetime, timedelta
from History.models import OutletLogs

class AllLogCsv(APIView):
	"""
	Outlet open/close log data GET API

		Authentication Required		: Yes
		Service Usage & Description	: .Download Outlet open/close csv file

		Data Post: {
		}

		Response: {

			"success": True, 
			"data": final_result
		}

	"""
	def get(self, request, format=None):
			s_date = request.GET.get('start_date')
			e_date = request.GET.get('end_date')
			start_date = dateutil.parser.parse(s_date)
			end_date = dateutil.parser.parse(e_date)
			token = request.GET.get('token')
			user = Token.objects.filter(key=token)[0].user_id
			st = request.GET.get('outlet_id')
			outletss = list(st.split(",")) 
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
			import xlwt
			response = HttpResponse(content_type='application/ms-excel')
			response['Content-Disposition'] = 'attachment; filename=outlet_log.xls'
			wb = xlwt.Workbook(encoding='utf-8')
			ws = wb.add_sheet("outlet_log")
			row_num = 0
			columns = [
				("Order & Invoice Details", 10000),
				("Order Value Details", 10000),
			]
			font_style = xlwt.XFStyle()
			font_style.font.bold = True
			pattern = xlwt.Pattern()
			pattern.pattern = xlwt.Pattern.SOLID_PATTERN
			pattern.pattern_fore_colour = xlwt.Style.colour_map['black']  # Set the cell background color to yellow
			font_style.pattern = pattern
			font_style.alignment.wrap = 1
			row_num = 0
			columns = [
				("OUTLET NAME", 3000),
				("DATE", 3000),
				("OPENING TIME", 3000),
				("CLOSING TIME", 3000),
				("STATUS", 3000),
				("RESPONSE USER", 3000),
			]
			for col_num in range(len(columns)):
				ws.write(row_num, col_num, columns[col_num][0], font_style)
				ws.col(col_num).width = columns[col_num][1]
			font_style = xlwt.XFStyle()
			font_style.alignment.wrap = 1	
			query = OutletLogs.objects.filter(Q(created_at__lte=e_date),Q(created_at__gte=s_date),\
					   Q(Company=cid))
			q_count = query.count()
			if q_count > 0:
				ord_data =[] 	
				for k in outletss:
					logdata = query.filter(outlet_id=k)
					for i in logdata:
						p_list ={}
						if i.opening_time !=None:
							o_time = i.opening_time+timedelta(hours=5,minutes=30)
							ot = str(o_time.time())
							s = ot.split('.')
							p_list['opening_time'] = s[0]
						else:
							p_list['opening_time'] = ''
						if i.closing_time !=None:
							o_time = i.closing_time+timedelta(hours=5,minutes=30)
							ot = str(o_time.time())
							s = ot.split('.')
							p_list['closing_time'] = s[0]
						else:
							p_list['closing_time'] = ''
						if i.created_at !=None:
							c_time = i.created_at+timedelta(hours=5,minutes=30)
							p_list['created_at'] = c_time.strftime("%Y-%m-%d")
						else:
							p_list['created_at'] = ''
						p_list['outlet'] = i.outlet.Outletname
						cid = ManagerProfile.objects.filter(auth_user_id=i.auth_user)
						p_list['user'] = cid[0].username
						st = i.is_open
						if st == True:
							p_list['status'] = 'Open'
						else:
							p_list['status'] = 'Closed'
						ord_data.append(p_list)
			else:
				ord_data = []
			for obj in ord_data:
				oname    = obj['outlet']
				dt       = obj['created_at']
				otime    = obj['opening_time']
				ctime    = obj['closing_time']
				st       = obj['status']
				user     = obj['user']
				row_num += 1
				row = [
					oname,
					dt,
					otime,
					ctime,
					st,
					user
				]
				for col_num in range(len(row)):
					ws.write(row_num, col_num, row[col_num], font_style)
			wb.save(response)
			return response
