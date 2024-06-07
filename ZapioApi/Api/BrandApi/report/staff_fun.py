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

def Calulate_present(id,s_date,e_date):
	query = StaffAttendance.objects.filter(Q(created_at__lte=e_date),\
							Q(created_at__gte=s_date),
							Q(profile_id=id))
	fsec = 0
	fday = 0
	hday = 0

	for index in query:
		if index.time_in == None and index.time_out == None:
			fday = fday + 0
			hday = hday + 0
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
			if sec >= 30420:
				fday = fday + 1
			else:
				pass
			if sec < 30420:
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


def Calulate_present_staff(staff_id,ids):
	query = StaffAttendance.objects.filter(Q(profile_id=staff_id),Q(id=ids))[0]
	if query.time_in == None and query.time_out == None:
		hour = 0
		day = ''
		return hour,day
	if query.time_in != None and query.time_out != None:
		intime = query.time_in +timedelta(hours=5,minutes=30)
		ihour = intime.hour
		imin = intime.minute
		itime = str(ihour) +':'+str(imin)

		outtime = query.time_out +timedelta(hours=5,minutes=30)
		ohour = outtime.hour
		omin = outtime.minute
		otime = str(ohour) +':'+str(omin)

		date_format = "%H:%M"
		t1 = datetime.strptime(str(itime),date_format)
		t2 = datetime.strptime(str(otime),date_format)
		f = t2 - t1
		sec = abs(f.total_seconds())
	else:
		pass

	if query.time_in != None and query.time_out == None:
		day = 'Full day'
		sec = 32400
	if sec > 3600:
		hour = convert(sec)
	else:
		hour = 0
	if sec >= 30420:
		day = 'Full day'
	else:
		pass
	if sec < 30420:
		day = 'Half day'
	else:
		pass
	#print(hour,day)
	return hour,day



