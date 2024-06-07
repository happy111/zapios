from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import re
from Outlet.models import TempTracking, OutletProfile
from UserRole.models import ManagerProfile
from datetime import datetime, timedelta


secret_token = "38e6d8b5269954e042cfda600f55a3ce2e1457ab560f24a5fa69335c167eaccd4a560c1e0fdfe7217013625a0f534414"


class TempRetrieve(APIView):
	"""
	Latest Temerature retrieval Post API

		Authentication Required		 	: 		Yes
		Service Usage & Description	 	: 		This Api is used to provide latest staff body temerature outletwise.

		Data Post: {

			"id"        : 	"21"
		}

		Response: {

			"success"	: 	True,
			"data"		:	result, 
			"message"	: 	"API worked well!!"

		}

	"""
	# permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			err_message = {}
			err_message["outlet"] = \
				validation_master_anything(str(data["id"]),"Outlet",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
								"success": False,
								"error" : err_message,
								"message" : "Please correct listed errors!!"
							})
			data['id'] = str(data['id'])
			today = datetime.now().date()
			record =  ManagerProfile.objects.filter(outlet__contains=[data['id']])
			temp_record = TempTracking.objects.filter(outlet=data['id'],created_at__date=today).\
															order_by('-created_at')
			if temp_record.count() == 0:
				track = 0
			else:
				track = 1
			result = []
			if record.count() == 0:
				return Response({
					"success"	:	False,
					"data"		:	result,
					"message"	:	"No staff member body temperature is logged today!!"	
					})
			else:
				last_time = []
				for i in record:
					data_dict = {}
					data_dict['user_id'] = i.id
					data_dict['manager_name'] = i.manager_name
					if track == 1:
						temp_record_user = temp_record.filter(staff_id=data_dict['user_id'],is_latest=1)
						if temp_record_user.count() == 0:
							data_dict['body_temp'] = None
						else:
							data_dict['body_temp'] = temp_record_user[0].body_temp
					else:
						data_dict['body_temp'] = None
					result.append(data_dict)
				if track == 1:
					t = temp_record[0].created_at+timedelta(hours=5,minutes=30)
					time_stamp = t.strftime("%Y-%m-%d %I:%M %p")
				else:
					time_stamp = None
				return Response({
					"success"		:	True,
					"data"			:	result,
					"time_stamp"	:	time_stamp,
					"message"		:	"API worked well!!"	
					})
		except Exception as e:
			return Response({
				"success"	: 	False, 
				"message"	: 	"Error happened!!", 
				"errors"	: 	str(e)
				})