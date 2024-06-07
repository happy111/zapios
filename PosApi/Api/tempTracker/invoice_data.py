 
import re
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
from Outlet.models import TempTracking, OutletProfile
from UserRole.models import ManagerProfile,UserType
from attendance.models import StaffAttendance
from datetime import datetime, timedelta
from .latest_temp import secret_token 
from Brands.models import Company
from django.db.models import Q


class InovoiceData(APIView):
	"""
	Invoice data retrieval Post API
		Authentication Required		 	: 		Yes
		Service Usage & Description	 	: 		This Api is used to provide invoice data outletwise.
		Data Post: {
			"id"        : 	"21"
		}
		Response: {
			"success"	: 	True,
			"data"		:	result, 
			"message"	: 	"API worked well!!"
		}
	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			cid = ManagerProfile.objects.filter(auth_user_id=request.user.id)[0].Company_id
			err_message = {}
			now = datetime.now()
			todate = now.date()
			year = now.year
			month = now.month
			today = now.day
			data = request.data
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
			check_company = OutletProfile.objects.filter(active_status=1,id=data['id'])
			clogo = Company.objects.filter(id=check_company[0].Company_id)[0].company_logo
			if clogo != '':
				domain_name = addr_set()
				full_path = domain_name + str(clogo)
			else:
				domain_name = addr_set()
				full_path = ''
			if check_company.count()==0:
				return Response(
					{
						"success": False,
	 					"message": "This Company is not active yet !!"
					}
					) 
			else:
				today = datetime.now().date()
				final_result = []
				for outlet in check_company:
					out_dict = {}
					row_id  = outlet.id
					out_dict["id"] = outlet.id
					out_dict["Outletname"] = outlet.Outletname
					out_dict["company_logo"] = full_path
					out_dict["company_name"] = Company.objects.filter(id=outlet.Company_id)[0].company_name
					out_dict["address"] = outlet.address
					out_dict["temp_detail"] = []
					staff_data = ManagerProfile.objects.filter(Q(is_attandance=1),Q(active_status=1),\
						outlet__icontains=data['id']).order_by('manager_name')
					if staff_data.count() > 0:
						for s in staff_data:
							di = {}
							di['name'] = s.manager_name +' '+ s.last_name
							di['id'] = s.id
							today = now.day
							staffdata = StaffAttendance.objects.filter(profile_id=s.id,\
										active_status=1,created_at__date=datetime.now().date(), is_billprint=1)
							if staffdata.count() > 0:
								for st in staffdata:
									di['temp']     = st.temperature
							if "temp" in di:
								out_dict["temp_detail"].append(di)
					final_result.append(out_dict)
			return Response({
							"success"	:	True,
							"message"	:	"API worked well!!",
							"data"		:	final_result,
							"company_logo" : full_path
							 })
		except Exception as e:
			return Response({
				"success"	: 	False, 
				"message"	: 	"Error happened!!", 
				"errors"	: 	str(e)
				})
