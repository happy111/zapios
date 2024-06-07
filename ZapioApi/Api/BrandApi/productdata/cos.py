import json
import math
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from ZapioApi.Api.BrandApi.profile.profile import CompanySerializer
from Brands.models import Company

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from Outlet.Api.serializers.order_serializers import OrderSerializer
from django.db.models import Q
from datetime import datetime, timedelta
from UserRole.models import ManagerProfile,UserType
import dateutil.parser
from django.http import HttpResponse

from django.db.models import (Count, 
								Sum, 
								Max, 
								Avg, 
								Case, 
								When, 
								Value, 
								IntegerField, 
								BooleanField)

from ZapioApi.api_packages import *
from attendance.models import StaffAttendance
from Outlet.models import OutletProfile
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user

def convert(seconds): 
	min, sec = divmod(seconds, 60) 
	hour, min = divmod(min, 60) 
	return "%d:%02d" % (hour, min) 

def Calulate_present(id):
	query = StaffAttendance.objects.filter(Q(profile_id=id))
	fsec = 0
	fday = 0
	hday = 0
	for index in query:
		if index.time_in != None and index.time_out != None:
			intime =index.time_in +timedelta(hours=5,minutes=30)
			ihour = intime.hour
			imin = intime.minute
			itime = str(ihour) +':'+str(imin)

			outtime =index.time_out +timedelta(hours=5,minutes=30)
			ohour = outtime.hour
			omin = outtime.minute
			otime = str(ohour) +':'+str(omin)

			date_format = "%H:%M"
			t1 = datetime.strptime(str(itime),date_format)
			t2 = datetime.strptime(str(otime),date_format)
			f = t2 - t1
			sec = abs(f.total_seconds())
			fsec = sec + fsec

			if sec >= 32400:
				fday = fday + 1
			else:
				pass
			if sec >= 18000 and sec < 32400:
				hday = hday + 1
			else:
				pass
		else:
			pass
		if index.time_in != None and index.time_out == None:
			fsec = fsec + 32400
			fday = fday + 1
		if fsec > 3600:
			hour = convert(fsec)
		else:
			hour = 0
	return hour,fday,hday











class StaffReport(APIView):
	"""
	Staff Report  POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for staff report for brand.

		Data Post: {
			"start_date"            : "2019-07-24 00:00:00:00",
			"end_date"              : "2019-07-29 00:00:00:00",
			"outlet_id"             : '',
			"staff_id"				: ''                 
		}

		Response: {

			"success": True, 
			"data": final_result
		}

	"""
	def get(self, request,format=None):
		try:
			# s_date = request.GET.get('start_date')
			# e_date = request.GET.get('end_date')
			# start_date = dateutil.parser.parse(s_date)
			# end_date = dateutil.parser.parse(e_date)
			token = request.GET.get('token')
			user = Token.objects.filter(key=token)[0].user_id
			cid = get_user(user)
			import xlwt
			response = HttpResponse(content_type='application/ms-excel')
			response['Content-Disposition'] = 'attachment; filename=attendance_report.xls'
			wb = xlwt.Workbook(encoding='utf-8')
			ws = wb.add_sheet("attendance_report")
			row_num = 0
			columns = [
				("Start date", 10000),
				("End Date", 10000),
			]
			font_style = xlwt.XFStyle()
			font_style.font.bold = True
			pattern = xlwt.Pattern()
			pattern.pattern = xlwt.Pattern.SOLID_PATTERN
			pattern.pattern_fore_colour = xlwt.Style.colour_map['blue']  # Set the cell background color to yellow
			font_style.pattern = pattern

			row_num = 1
			columns = [
				("Staff ID", 3000),
				("Staff Name", 6000),
				("Designation", 6000),
				("Outlet", 9000),
				("Full Days", 3000),
				("Half Days", 3000),
				("LWP", 3000),
				("CL", 2000),
				("Weekly Off", 3000),
				("Earned Leaves", 3500),
				("Total Hours",3000),
			]
			font_style = xlwt.XFStyle()
			font_style.font.bold = True
			for col_num in range(len(columns)):
				ws.write(row_num, col_num, columns[col_num][0],xlwt.easyxf('align:horiz centre; pattern: pattern solid, fore_color gray25;  font: color black,bold on,height 200'))
				ws.col(col_num).width = columns[col_num][1]

			staff_data = ManagerProfile.objects.filter(Q(is_attandance=1),
				Q(active_status=1),\
				Company_id=cid).order_by('manager_name')
			if staff_data.count() > 0:
				for index in staff_data:
					outlet = index.outlet
					if len(outlet) > 0:
						outlet_name = OutletProfile.objects.filter(id=outlet[0])[0].Outletname
					else:
						outlet_name = ''
					query = StaffAttendance.objects.filter(Q(profile_id=index.id))
					if query.count() > 0:
						p = query.filter(status='present')
						hour,fday,hday = Calulate_present(index.id)
						total_days = query.count()
						w = query.filter(status='weeklyoff')
						if w.count() > 0:
							week_off = w.count()
						else:
							week_off = 0
						wl = query.filter(status='lwp')
						if wl.count() > 0:
							without_pay_leave = wl.count()
						else:
							without_pay_leave = 0
						cl = query.filter(status='cl')
						if cl.count() > 0:
							casual_leave = cl.count()
						else:
							casual_leave = 0
						el = query.filter(status='el')
						if el.count() > 0:
							earned_leave = el.count()
						else:
							earned_leave = 0
					else:
						week_off = 0
						earned_leave = 0
						casual_leave = 0
						without_pay_leave = 0
						total_days = 0

					row_num += 1
					row = [
						index.id,
						str(index.manager_name) + str(index.last_name),
						index.user_type.user_type,
						outlet_name,
						fday,
						hday,
						week_off,
						earned_leave,
						casual_leave,
						without_pay_leave,
						hour
					]
					for col_num in range(len(row)):
						ws.write(row_num, col_num, row[col_num])
			wb.save(response)
			return response
		except Exception as e:
			print(e)
			return Response(
						{"error":str(e)}
						)


class AllAttandanceList(APIView):
	"""
	Attandance data post API

		Authentication Required		 	: 		Yes
		Service Usage & Description	 	: 		This Api is used to provide listing staff all information.

		Data Get: {
				"outlet_id"  : "1"
		}

		Response: {

			"success"	: 	True,
			"data"		:	result, 

		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			user_id = request.user.id 
			data = request.data
			now = datetime.now()
			todate = now.date()
			year = now.year
			month = now.month
			today = now.day
			final_result = []
			staff_data = ManagerProfile.objects.filter(Q(is_attandance=1),Q(active_status=1),\
				outlet__icontains=data['outlet_id']).order_by('manager_name')
			if staff_data.count() > 0:
				staff_outlet = staff_data[0].outlet
				for s in staff_data:
					di = {}
					di['name'] = s.manager_name +' '+ s.last_name
					di['user_type'] = UserType.objects.filter(id=s.user_type_id)[0].user_type
					di['id'] = s.id
					final_result.append(di)
			return Response({
				"success"	: 	True, 
				"data"	    : 	final_result
				})
		except Exception as e:
			return Response({
				"success"	: 	False, 
				"message"	: 	"Error happened!!", 
				"errors"	: 	str(e)
				})


