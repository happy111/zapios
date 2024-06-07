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
	permission_classes = (IsAuthenticated,)
	def post(self, request):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			err_message = {}
			if data["start_date"] != '' and data["end_date"] != '':
				start_date = dateutil.parser.parse(data["start_date"])
				end_date = dateutil.parser.parse(data["end_date"])
				if start_date > end_date:
					err_message["from_till"] = "Validity dates are not valid!!"
			else:
				pass
			err_message["staff_id"] = only_required(data["staff_id"],"Staff")
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			user = request.user.id
			cid = get_user(user)
			query = StaffAttendance.objects.filter(Q(created_at__lte=end_date),\
							Q(created_at__gte=start_date),
							Q(profile_id=data['staff_id'])).order_by('created_at')
			final_result = []
			if query.count() > 0:
				for index in query:
					p_list ={}
					if index.time_out != None:
						out_time = index.time_out+timedelta(hours=5,minutes=30)
						p_list['clock_out'] = out_time.strftime("%I:%M %p")
					if index.time_in != None:
						in_time = index.time_in+timedelta(hours=5,minutes=30)
						p_list['clock_in'] = in_time.strftime("%I:%M %p")

					created_at = index.created_at+timedelta(hours=5,minutes=30)
					p_list['date'] = created_at.strftime("%d/%b/%y")
					hour,day = Calulate_present_staff(data['staff_id'],index.id)
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
					final_result.append(p_list)
					if query.count() > 0:
						hours,fday,hday = Calulate_present(data['staff_id'],start_date,end_date)
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
						present = 0
						week_off = 0
						earned_leave = 0
						casual_leave = 0
						without_pay_leave = 0
						total_days = 0
			if len(final_result) > 0:
				return Response({"status":True,
								 "result":final_result,
								 'half_day':hday,
								 'full_day' : fday,
								 'total_days': total_days,
								 'week_off': week_off,
								 'without_pay_leave':without_pay_leave,
								 'casual_leave' : casual_leave,
								 'earned_leave': earned_leave,
								 'hours_worked' : hours
							   })
			else:
				return Response({"status":True,
				 "result":final_result,
				 'half_day':0,
				 'full_day' : 0,
				 'total_days': 0,
				 'week_off': 0,
				 'without_pay_leave':0,
				 'casual_leave' : 0,
				 'earned_leave': 0,
				 'hours_worked' : 0
			   })
		except Exception as e:
			print(e)
			return Response(
						{"error":str(e)}
						)

