from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import re
from Outlet.models import TempTracking, OutletProfile
from UserRole.models import ManagerProfile
from datetime import datetime


class TempAdd(APIView):
	"""
	Temperature Add Post API

		Authentication Required		 	: 		Yes
		Service Usage & Description	 	: 		This Api is used to add staff body temerature outletwise.

		Data Post: {

			"outlet_id"        : 	"21",
			"staff_temp"	   :	"[{'user_id': '51', 'body_temp': '95'},{'user_id' : '52', 'body_temp' : '94'}]"
		}

		Response: {

			"success"		:	True,
			"message"		:	"Temperature logged successfully!!"	

		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			err_message = {}
			err_message["outlet_id"] = \
				validation_master_anything(str(data["outlet_id"]),"Outlet",contact_re, 1)
			list1 = []
			for i in data["staff_temp"]:
				try:
					i['body_temp'] = float(i['body_temp'])
					list1.append(i)
				except Exception as e:
					pass
			data["staff_temp"] = list1
			if len(data["staff_temp"]) == 0:
				err_message["staff_temp"] = "No staff members are being tracked!!"
			else:
				for i in data["staff_temp"]:
					if 'user_id' in i and 'body_temp' in i:
						try:
							i['user_id'] = int(i['user_id'])
							i['body_temp'] = float(i['body_temp'])
						except Exception as e:
							err_message["staff_temp"] = \
							"Staff member and body temperature are not properly set!!"
							break
					else:
						err_message["staff_temp"] = \
						"Staff member and body temperature are not properly set!!"
			if any(err_message.values())==True:
				return Response({
								"success": False,
								"error" : err_message,
								"message" : "Please correct listed errors!!"
							})
			data['outlet_id'] = str(data['outlet_id'])
			latest_update = TempTracking.objects.filter(outlet_id=data['outlet_id']).update(is_latest=0)
			for i in data["staff_temp"]:
				record = ManagerProfile.objects.filter(outlet__contains=[data['outlet_id']], \
																	id = i['user_id'])
				if record.count() == 0:
					return Response({
						"success"	:	False,
						"message"	:	"No data found!!"	
						})
				else:
					company = record[0].Company_id
					if i['body_temp'] != "" and i['body_temp'] != None and i['body_temp'] != "None":
						temp_log_create = TempTracking.objects.create(Company_id=company, 
														outlet_id=data['outlet_id'],\
														staff_id=i['user_id'],body_temp=i['body_temp'])
					else:
						pass
			return Response({
				"success"		:	True,
				"message"		:	"Temperature logged successfully!!"	
				})
		except Exception as e:
			return Response({
				"success"	: 	False, 
				"message"	: 	"Error happened!!", 
				"errors"	: 	str(e)
				})