import re
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
from UserRole.models import ManagerProfile,Attendance
from datetime import datetime
import dateutil.parser


def convert(seconds): 
	min, sec = divmod(seconds, 60) 
	hour, min = divmod(min, 60) 
	return "%d:%02d:%02d" % (hour, min, sec) 

class AttandanceCreate(APIView):
	"""
	Attandance Add Post API

		Authentication Required		 	: 		Yes
		Service Usage & Description	 	: 		This Api is used to add attandance for staff.

		Data Post: {

			"staff_id"         : "23",
			"temp"             : "67",
			'is_billprint'     : "true"
			"status"           : "login / logout / absent / weakoff / lwp/ cl / el / billprint"
		}

		Response: {

			"success"		:	True,
			"message"		:	"Login successfully!!"	

		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			staffdata = ManagerProfile.objects.filter(id=data['staff_id'])
			if staffdata.count() > 0:
				staff_name = staffdata[0].manager_name
				cid = staffdata[0].Company_id
			else:
				return Response({
							"success"		:	False,
							"message"		:	"Required Staff data is not valid to retrieve!!"	
						})
			err_message = {}
			now = datetime.now()
			todate = now.date()
			year = now.year
			month = now.month
			today = now.day
			hour = now.hour
			mins = now.minute
			if 'status' not in data:
				return Response({
							"success"		:	False,
							"message"		:	"Please send 'status' key!!"	
						})
			if 'temp' in data:
				if float(data['temp']) >= 95 and float(data['temp']) <= 105:
					pass
				else:
					return Response({
							"success"		:	False,
							"message"		:	"Temperature is required 95 F to 105 F!!"	
						})
			if data['status'] == 'login':
				otime = '00:00'
				itime = str(hour) +':'+str(mins)
				adata = Attendance.objects.filter(profile_id=data['staff_id'],created_at__year=year,\
					created_at__month=month,created_at__day=today,status='absent')
				if adata.count() > 0:
					return Response({
							"success"		:	True,
							"message"		:	"You have contact admin!!"	
						})
				adata = Attendance.objects.filter(profile_id=data['staff_id'],created_at__year=year,\
					created_at__month=month,created_at__day=today,status='weakoff')
				if adata.count() > 0:
					return Response({
							"success"		:	True,
							"message"		:	"You have contact admin!!"	
						})
				adata = Attendance.objects.filter(profile_id=data['staff_id'],created_at__year=year,\
					created_at__month=month,created_at__day=today,status='login')
				if adata.count() > 0:
					return Response({
							"success"		:	True,
							"message"		:	"You have already login now!!"	
						})
				else:
					if 'temp' in data and 'is_billprint' in data:
						attandance_data = Attendance.objects.create(auth_user_id=request.user.id,profile_id=data['staff_id'],\
							name = staff_name, in_time = itime, out_time = otime,\
							time_in=now,company_id=cid,temp=data['temp'],status='login',\
							is_billprint=data['is_billprint'])
					elif 'temp' in data:
						attandance_data = Attendance.objects.create(auth_user_id=request.user.id,profile_id=data['staff_id'],\
							name = staff_name, in_time = itime, out_time = otime,\
							time_in=now,company_id=cid,temp=data['temp'],status='login')
					elif 'is_billprint' in data:
						attandance_data = Attendance.objects.create(auth_user_id=request.user.id,profile_id=data['staff_id'],\
							name = staff_name, in_time = itime, out_time = otime,\
							time_in=now,company_id=cid,is_billprint=data['is_billprint'],status='login')
					else:
						attandance_data = Attendance.objects.create(auth_user_id=request.user.id,profile_id=data['staff_id'],\
							name = staff_name, in_time = itime, out_time = otime,\
							time_in=now,company_id=cid,status='login')
					return Response({
								"success"		:	True,
								"message"		:	"Login successfully!!"	
							})
			elif(data['status'] == 'logout'):
				otime = str(hour) +':'+str(mins)
				adata = Attendance.objects.filter(profile_id=data['staff_id'],created_at__year=year,\
					created_at__month=month,created_at__day=today)
				if adata.count() > 0:
					if otime =='00:00':
						err_message['time'] = "Please Enter out time"
					else:
						pass
					if any(err_message.values())==True:
						return Response({
										"success": False,
										"error"  : err_message,
										"message" : "Please correct listed errors!!"
									})
					if 'temp' in data:
						attandance_data = adata.update(out_time = otime,time_out = now,\
													company_id=cid,temp=data['temp'],status='logout')
					else:
						attandance_data = adata.update(out_time = otime,time_out = now,\
													company_id=cid,status='logout')
					date_format = "%H:%M:%S"
					t1 = datetime.strptime(str(adata[0].in_time),date_format)
					t2 = datetime.strptime(str(adata[0].out_time),date_format)
					f = t2 - t1
					sec = f.total_seconds()
					hour = convert(sec)
					message = staff_name.capitalize() +' works on ' + hour 
					return Response({
								"success"		:	True,
								"hour"          :   hour,
								"message"		:	"logout successfully"	
					})
				else:
					return Response({
								"success"		:	True,
								"message"		:	"You have not login today!!"	
					})

			elif(data['status'] == 'temp'):
				adata = Attendance.objects.filter(profile_id=data['staff_id'],created_at__year=year,\
					created_at__month=month,created_at__day=today,status='login')
				if adata.count() > 0:
					attandance_data = adata.update(temp=data['temp'])
					return Response({
									"success"		:	True,
									"message"		:	"Temperature Updated successfully"	
						})
				else:
					return Response({
									"success"		:	True,
									"message"		:	"You have login First!!"	
						})

			elif(data['status'] == 'absent'):
				adata = Attendance.objects.filter(profile_id=data['staff_id'],created_at__year=year,\
					created_at__month=month,created_at__day=today)
				if adata.count() > 0:
					attandance_data = adata.update(status='absent')
				else:
					attandance_data = Attendance.objects.create(auth_user_id=request.user.id,profile_id=data['staff_id'],\
												name=staff_name,company_id=cid,status='absent')
				return Response({
								"success"		:	True,
								"message"		:	"You are absent today"	
					        })
			elif(data['status'] == 'weakoff'):
				adata = Attendance.objects.filter(profile_id=data['staff_id'],created_at__year=year,\
					created_at__month=month,created_at__day=today)
				if adata.count() > 0:
					attandance_data = adata.update(status='weakoff')
				else:
					attandance_data = Attendance.objects.create(auth_user_id=request.user.id,profile_id=data['staff_id'],\
												name=staff_name,company_id=cid,status='weakoff')
				return Response({
								"success"		:	True,
								"message"		:	"You are weakoff today"	
					        })
			elif (data['status'] == 'lwp'):
				adata = Attendance.objects.filter(profile_id=data['staff_id'], created_at__year=year, \
												  created_at__month=month, created_at__day=today)
				if adata.count() > 0:
					attandance_data = adata.update(status='lwp')
				else:
					attandance_data = Attendance.objects.create(auth_user_id=request.user.id,
																profile_id=data['staff_id'], \
																name=staff_name, company_id=cid, status='lwp')
				return Response({
					"success"	:	True,
					"message"		:	"You are on Leave Without Pay today"
				})
			elif (data['status'] == 'cl'):
				adata = Attendance.objects.filter(profile_id=data['staff_id'], created_at__year=year, \
												  created_at__month=month, created_at__day=today)
				if adata.count() > 0:
					attandance_data = adata.update(status='cl')
				else:
					attandance_data = Attendance.objects.create(auth_user_id=request.user.id,
																profile_id=data['staff_id'], \
																name=staff_name, company_id=cid, status='cl')
				return Response({
					"success"	:	True,
					"message"		:	"You are on Casual Leave today"
				})
			elif (data['status'] == 'el'):
				adata = Attendance.objects.filter(profile_id=data['staff_id'], created_at__year=year, \
												  created_at__month=month, created_at__day=today)
				if adata.count() > 0:
					attandance_data = adata.update(status='el')
				else:
					attandance_data = Attendance.objects.create(auth_user_id=request.user.id,
																profile_id=data['staff_id'], \
																name=staff_name, company_id=cid, status='el')
				return Response({
					"success"	:	True,
					"message"		:	"You are on Earned Leave today"
				})
			elif(data['status'] == 'billprint'):
				if 'is_billprint' in data:
					pass
				else:
					return Response({
								"success"		:	True,
								"message"		:	"Please send 'is_billprint' key"	
					        })
				adata = Attendance.objects.filter(profile_id=data['staff_id'],created_at__year=year,\
					created_at__month=month,created_at__day=today,status='login')
				if adata.count() > 0:
					if adata[0].temp !=None:
						attandance_data = adata.update(is_billprint=data['is_billprint'])
						return Response({
									"success"		:	True,
									"message"		:	"Bill status is updated!!"	
						})
					else:
						return Response({
									"success"		:	True,
									"message"		:	"You have  First updated temperature!!"	
						})

				else:
					return Response({
								"success"		:	True,
								"message"		:	"You have login first!!"	
					})

			else:
				return Response({
								"success"		:	False,
								"message"		:	"Please choose status type"	
					})
		except Exception as e:
			return Response({
				"success"	: 	False, 
				"message"	: 	"Error happened!!", 
				"errors"	: 	str(e)
				})