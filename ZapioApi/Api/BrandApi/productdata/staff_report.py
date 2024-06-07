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
from . staff_fun import *




class StaffCSVReport(APIView):
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
			s_date = request.GET.get('start_date')
			e_date = request.GET.get('end_date')
			start_date = dateutil.parser.parse(s_date)
			end_date = dateutil.parser.parse(e_date)
			token = request.GET.get('token')
			user = Token.objects.filter(key=token)[0].user_id
			cid = get_user(user)
			report_type = request.GET.get('type')


			if report_type == 'Consoledate':
				import xlwt
				response = HttpResponse(content_type='application/ms-excel')
				response['Content-Disposition'] = 'attachment; filename=attendance_report.xls'
				wb = xlwt.Workbook(encoding='utf-8')
				ws = wb.add_sheet("attendance_report")
				row_num = 0
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
				row_num = 2
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
					ws.write(row_num, col_num, columns[col_num][0],xlwt.easyxf('align:horiz centre; pattern: pattern solid, fore_color orange;  font: color white,bold on,height 200'))
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
						query = StaffAttendance.objects.filter(Q(created_at__lte=e_date),\
										Q(created_at__gte=s_date),
										Q(profile_id=index.id))
						if query.count() > 0:
							p = query.filter(status='present')
							hour,fday,hday = Calulate_present(index.id,s_date,e_date)
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
							str(hour)
						]
						for col_num in range(len(row)):
							ws.write(row_num, col_num, row[col_num])
				wb.save(response)
				return response
			if report_type == 'Detailed':
				import xlwt
				response = HttpResponse(content_type='application/ms-excel')
				response['Content-Disposition'] = 'attachment; filename=attendance_report.xls'
				wb = xlwt.Workbook(encoding='utf-8')
				ws = wb.add_sheet("attendance_report")
				row_num = 0
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

				row_num = 2
				columns = [
					("Date", 3000),
					("Staff ID", 3000),
					("Staff Name", 6000),
					("Designation", 6000),
					("Outlet", 9000),
					("Clock In", 3000),
					("Clock Out", 3000),
					("Status", 5000),
					("Hours",3000),
				]
				font_style = xlwt.XFStyle()
				font_style.font.bold = True
				for col_num in range(len(columns)):
					ws.write(row_num, col_num, columns[col_num][0],xlwt.easyxf('align:horiz centre; pattern: pattern solid, fore_color orange;  font: color white,bold on,height 200'))
					ws.col(col_num).width = columns[col_num][1]
				staff_data = ManagerProfile.objects.filter(Q(is_attandance=1),
					Q(active_status=1),\
					Company_id=cid).order_by('manager_name')
				if staff_data.count() > 0:
					for i in staff_data:
						outlet = i.outlet
						if len(outlet) > 0:
							outlet_name = OutletProfile.objects.filter(id=outlet[0])[0].Outletname
						else:
							outlet_name = ''
						query = StaffAttendance.objects.filter(Q(created_at__lte=e_date),\
							Q(created_at__gte=s_date),
							Q(profile_id=i.id)).order_by('created_at')
						for index in query:
							p_list = {}
							if index.time_out != None:
								out_time = index.time_out+timedelta(hours=5,minutes=30)
								p_list['clock_out'] = out_time.strftime("%I:%M %p")
							else:
								p_list['clock_out'] = '' 
							if index.time_in != None:
								in_time = index.time_in+timedelta(hours=5,minutes=30)
								p_list['clock_in'] = in_time.strftime("%I:%M %p")
							else:
								p_list['clock_in'] = ''
							created_at = index.created_at+timedelta(hours=5,minutes=30)
							p_list['date'] = created_at.strftime("%d/%b/%y")
							if index.status == 'present':
								hour,day = Calulate_present_staff(i.id,index.id)
								if day == 'Full day':
									p_list['status'] = 'Full day'
								elif day == 'Half day':
									p_list['status'] = 'Half day'
								else:
									p_list['status'] = 'Quarter day'
							elif index.status == 'lwp':
								p_list['status'] = 'Leave without pay'
								hour = str(0)
							elif index.status == 'cl':
								p_list['status'] = 'Casual leave'
								hour = str(0)
							elif index.status == 'el':
								p_list['status'] = 'Earned leave'
								hour = str(0)
							elif index.status == 'weeklyoff':
								p_list['status'] = 'Weekly Off'
								hour = str(0)
							else:
								pass
							row_num += 1
							row = [
								p_list['date'],
								i.id,
								str(i.manager_name) + str(i.last_name),
								i.user_type.user_type,
								outlet_name,
								p_list['clock_in'],
								p_list['clock_out'],
								p_list['status'],
								str(hour)
							]
							for col_num in range(len(row)):
								if row[col_num] == 'Weekly Off' or row[col_num] == 'Leave without pay' or \
								 row[col_num] == 'Casual leave' or row[col_num] == 'Earned leave':
									ws.write(row_num, col_num, row[col_num],xlwt.easyxf('align:horiz left; pattern: pattern solid, fore_color red;  font: color white,bold on,height 200'))
								else:
									ws.write(row_num, col_num, row[col_num])

				wb.save(response)
				return response
			if report_type == 'Individual':
				staff_id = request.GET.get('staff_id')
				staff_data = ManagerProfile.objects.filter(id=staff_id)
				outlet = staff_data[0].outlet
				if len(outlet) > 0:
					outlet_name = OutletProfile.objects.filter(id=outlet[0])[0].Outletname
				else:
					outlet_name = ''
				
				query = StaffAttendance.objects.filter(Q(created_at__lte=e_date),\
							Q(created_at__gte=s_date),
							Q(profile_id=staff_id)).order_by('created_at')
				if query.count() > 0:
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
					hour,fday,hday = Calulate_present(staff_id,s_date,e_date)
				else:
					pass
				import xlwt
				response = HttpResponse(content_type='application/ms-excel')
				response['Content-Disposition'] = 'attachment; filename=attendance_report.xls'
				wb = xlwt.Workbook(encoding='utf-8')
				ws = wb.add_sheet("attendance_report")
				row_num = 0
				ws.write(0, 0, 'Start Date',xlwt.easyxf('align:horiz centre; pattern: pattern solid, fore_color lime;  font: color black,bold on,height 200'))
				ws.write(0, 1, s_date)

				ws.write(0, 2, 'End Date',xlwt.easyxf('align:horiz centre; pattern: pattern solid, fore_color lime;  font: color black,bold on,height 200'))
				ws.write(0, 3, e_date)

				ws.write(0, 4, 'Staff Name',xlwt.easyxf('align:horiz centre; pattern: pattern solid, fore_color lime;  font: color black,bold on,height 200'))
				ws.write(0, 5, str(staff_data[0].manager_name+''+str(staff_data[0].last_name)))

				ws.write(2, 0, 'Staff ID',xlwt.easyxf('align:horiz centre; pattern: pattern solid, fore_color lime;  font: color black,bold on,height 200'))
				ws.write(2, 1, str(staff_data[0].id))

				ws.write(2, 2, 'Designation',xlwt.easyxf('align:horiz centre; pattern: pattern solid, fore_color lime;  font: color black,bold on,height 200'))
				ws.write(2, 3, staff_data[0].user_type.user_type)

				ws.write(2, 4, 'Total days',xlwt.easyxf('align:horiz centre; pattern: pattern solid, fore_color lime;  font: color black,bold on,height 200'))
				ws.write(2, 5, query.count())

				ws.write(4, 0, 'Full day',xlwt.easyxf('align:horiz centre; pattern: pattern solid, fore_color lime;  font: color black,bold on,height 200'))
				ws.write(4, 1, fday)

				ws.write(4, 2, 'Half days',xlwt.easyxf('align:horiz centre; pattern: pattern solid, fore_color lime;  font: color black,bold on,height 200'))
				ws.write(4, 3, hday)

				ws.write(4, 4, 'Weekly off',xlwt.easyxf('align:horiz centre; pattern: pattern solid, fore_color lime;  font: color black,bold on,height 200'))
				ws.write(4, 5, week_off)


				ws.write(6, 0, 'Earned Leave',xlwt.easyxf('align:horiz centre; pattern: pattern solid, fore_color lime;  font: color black,bold on,height 200'))
				ws.write(6, 1, earned_leave)

				ws.write(6, 2, 'LWP',xlwt.easyxf('align:horiz centre; pattern: pattern solid, fore_color lime;  font: color black,bold on,height 200'))
				ws.write(6, 3, without_pay_leave)

				ws.write(6, 4, 'Casual Leaves',xlwt.easyxf('align:horiz centre; pattern: pattern solid, fore_color lime;  font: color black,bold on,height 200'))
				ws.write(6, 5, casual_leave)


				ws.write(8, 0, 'Outlet Name',xlwt.easyxf('align:horiz centre; pattern: pattern solid, fore_color lime;  font: color black,bold on,height 200'))
				ws.write(8, 1, outlet_name)

				font_style = xlwt.XFStyle()
				font_style.font.bold = True
				pattern = xlwt.Pattern()
				pattern.pattern = xlwt.Pattern.SOLID_PATTERN
				pattern.pattern_fore_colour = xlwt.Style.colour_map['blue']  # Set the cell background color to yellow
				font_style.pattern = pattern

				row_num = 10
				columns = [
					("S.No", 3000),
					("Date", 3000),
					("Clock In", 3000),
					("Clock Out", 3000),
					("Status", 3000),
					("Hours",3000),
				]
				font_style = xlwt.XFStyle()
				font_style.font.bold = True
				for col_num in range(len(columns)):
					ws.write(row_num, col_num, columns[col_num][0],xlwt.easyxf('align:horiz centre; pattern: pattern solid, fore_color brown;  font: color white,bold on,height 200'))
					ws.col(col_num).width = columns[col_num][1]

				query = StaffAttendance.objects.filter(Q(created_at__lte=e_date),\
							Q(created_at__gte=s_date),
							Q(profile_id=staff_id))
				i = 1
				for index in query:
					p_list = {}
					if index.time_out != None:
						out_time = index.time_out+timedelta(hours=5,minutes=30)
						p_list['clock_out'] = out_time.strftime("%I:%M %p")
					else:
						p_list['clock_out'] = '' 
					if index.time_in != None:
						in_time = index.time_in+timedelta(hours=5,minutes=30)
						p_list['clock_in'] = in_time.strftime("%I:%M %p")
					else:
						p_list['clock_in'] = ''

					created_at = index.created_at+timedelta(hours=5,minutes=30)
					p_list['date'] = created_at.strftime("%d/%b/%y")
					hour,day = Calulate_present_staff(staff_id,index.id)
					if index.status == 'present':
						if day == 'Full day':
							p_list['status'] = 'Full day'
						elif day == 'Quarter day':
							p_list['status'] = 'Quarter day'
						else:
							p_list['status'] = 'Half day'
					elif index.status == 'lwp':
						p_list['status'] = 'Leave without pay'
						hour = str(0)
					elif index.status == 'cl':
						p_list['status'] = 'Casual leave'
						hour = str(0)
					elif index.status == 'el':
						p_list['status'] = 'Earned leave'
						hour = str(0)
					elif index.status == 'weeklyoff':
						p_list['status'] = 'Weekly Off'
						hour = str(0)
					else:
						pass
					row_num += 1
					row = [
						i,
						p_list['date'],
						p_list['clock_in'],
						p_list['clock_out'],
						p_list['status'],
						str(hour)
					]
					i = i + 1
					for col_num in range(len(row)):
						if row[col_num] == 'Weekly Off' or row[col_num] == 'Leave without pay' or \
						 row[col_num] == 'Casual leave' or row[col_num] == 'Earned leave':
							ws.write(row_num, col_num, row[col_num],xlwt.easyxf('align:horiz left; pattern: pattern solid, fore_color red;  font: color white,bold on,height 200'))
						else:
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
			user = request.user.id
			cid = get_user(user)
			final_result = []
			staff_data = ManagerProfile.objects.filter(Q(is_attandance=1),\
				Q(active_status=1),Q(Company_id=cid)).order_by('manager_name')
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


