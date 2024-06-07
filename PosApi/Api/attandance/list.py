import re
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
from Outlet.models import TempTracking, OutletProfile
from UserRole.models import ManagerProfile,Attendance,UserType
from datetime import datetime, timedelta
from Brands.models import Company
from django.db.models import Q

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
					di['is_attandance'] = s.is_attandance
					staffdata = Attendance.objects.filter(profile_id=s.id,\
								active_status=1,created_at__year=year,\
								created_at__month=month,created_at__day=today)
					
					if staffdata.count() > 0:
						for st in staffdata:
							if st.time_in != None:
								i = st.time_in+timedelta(hours=5,minutes=30)
								i_time = i.strftime("%d/%b/%y %I:%M %p")
							else:
								i_time = ''
							if st.time_out != None:
								t = st.time_out+timedelta(hours=5,minutes=30)
								o_time = t.strftime("%d/%b/%y %I:%M %p")
							else:
								o_time = ''
							di['in_time']  = i_time
							di['out_time'] = o_time
							di['temp']     = st.temp
							di['status']   = st.status
							di['is_billprint']   = st.is_billprint
					else:
						di['in_time']  = ''
						di['out_time'] = ''
						di['temp']     = ''
						di['status']   = ''
						di['is_billprint']   = ''
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



			



