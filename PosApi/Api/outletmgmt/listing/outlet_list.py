from rest_framework.views import APIView
from rest_framework.response import Response
from Brands.models import Company
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from Outlet.models import OutletProfile,OutletTiming
from UserRole.models import * 
from Orders.models import Order,OrderTracking
from django.db.models import Q
from django.db.models import Count, Sum, Max, Avg, Case, When, Value, IntegerField, BooleanField
from History.models import OutletLogs
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class AllOutlet(APIView):

	"""
	All Outlet list GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of outlet within brand

	"""

	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			brand_id = request.GET.get('brand')
			user = request.user
			co_id = ManagerProfile.objects.filter(auth_user_id=user.id)[0].Company_id
			staff_data = ManagerProfile.objects.filter(auth_user_id=user.id,Company_id=co_id)
			if len(brand_id) > 0:
				brand = list(brand_id.split(","))
				final_outlet = []
				for index in brand:
					co_id = ManagerProfile.objects.filter(mobile=staff_data[0].mobile,Company_id=index)
					if co_id.count() > 0:
						for temp in co_id[0].outlet:
							final_outlet.append(temp)
			else:
				co_id = ManagerProfile.objects.filter(auth_user_id=user.id)[0].Company_id
				outlet_data = ManagerProfile.objects.filter(auth_user_id=user.id)
				final_outlet = outlet_data[0].outlet
			final_result = []
			now = datetime.now()
			month = now.month
			year = now.year
			today = now.day

			if final_outlet != None:
				for j in final_outlet:
					record = OutletProfile.objects.filter(id=j,active_status=1,is_hide=0)
					if record.count() > 0:
						for i in record:
							now = datetime.now()
							from datetime import date
							import calendar
							curr_date = date.today()
							dt = calendar.day_name[curr_date.weekday()]
							now = datetime.now()
							current_time = now.strftime("%H:%M:%S")
							to_let = 0
							chk_out = OutletTiming.objects.filter(day=dt,outlet_id=i.id)
							if chk_out.count() > 0:
								for index in chk_out:
									k = 1
									open_time = index.opening_time
									close_time = index.closing_time
									time = datetime.strptime(current_time, '%H:%M:%S').time()
									if open_time > close_time:
										c_tmp = open_time
										open_time = close_time
										close_time = c_tmp
										if time > open_time and time < close_time:
											pass
										else:
											to_let = 1
									else:
										if time > open_time and time < close_time:
											to_let = 1
										else:
											pass
							if to_let == 1:
								q_dict = {}
								q_dict["id"] = i.id
								q_dict["Outletname"] = i.Outletname
								q_dict["Company"] = i.Company_id
								q_dict["Company_name"] = Company.objects.filter(id=i.Company_id)[0].company_name
								ol = OutletLogs.objects.filter(outlet=i.id)
								if ol.count() > 0:
									if ol.last().opening_time !=None:
										o_time = ol.last().opening_time+timedelta(hours=5,minutes=30)
										ot = str(o_time.time())
										s = ot.split('.')
										q_dict["opening_time"] = s[0]
										if now.weekday() == 0:
											openingTime = OutletTiming.objects.filter(day='Monday')[0].opening_time
										elif now.weekday() == 1:
											openingTime = OutletTiming.objects.filter(day='Tuesday')[0].opening_time
										elif now.weekday() == 2:
											openingTime = OutletTiming.objects.filter(day='Wednesday')[0].opening_time
										elif now.weekday() == 3:
											openingTime = OutletTiming.objects.filter(day='Thursday')[0].opening_time
										elif now.weekday() == 4:
											openingTime = OutletTiming.objects.filter(day='Friday')[0].opening_time
										elif now.weekday() == 5:
											openingTime = OutletTiming.objects.filter(day='Saturday')[0].opening_time
										elif now.weekday() == 6:	
											openingTime = OutletTiming.objects.filter(day='Sunday')[0].opening_time

										format_list = str(openingTime).split(":")
										if len(format_list) == 2:
											opening_time = now + relativedelta(hour =int(format_list[0]),minute=int(format_list[1]))
										elif len(format_list)==3:
											opening_time = now + relativedelta(hour =int(format_list[0]),minute=int(format_list[1]),second=int(format_list[2]))

									if ol.last().closing_time !=None:
										c_time = ol.last().closing_time+timedelta(hours=5,minutes=30)
										ct = str(c_time.time())
										c = ct.split('.')
										q_dict["closing_time"] = c[0]
										if now.weekday() == 0:
											closingTime = OutletTiming.objects.filter(day='Monday')[0].closing_time
										elif now.weekday() == 1:
											closingTime = OutletTiming.objects.filter(day='Tuesday')[0].closing_time
										elif now.weekday() == 2:
											closingTime = OutletTiming.objects.filter(day='Wednesday')[0].closing_time
										elif now.weekday() == 3:
											closingTime = OutletTiming.objects.filter(day='Thursday')[0].closing_time
										elif now.weekday() == 4:
											closingTime = OutletTiming.objects.filter(day='Friday')[0].closing_time
										elif now.weekday() == 5:
											closingTime = OutletTiming.objects.filter(day='Saturday')[0].closing_time
										elif now.weekday() == 6:	
											closingTime = OutletTiming.objects.filter(day='Sunday')[0].closing_time
										format_list = str(closingTime).split(":")
										if len(format_list) == 2:
											closing_time = now + relativedelta(hour =int(format_list[0]),minute=int(format_list[1]))
										elif len(format_list)==3:
											closing_time = now + relativedelta(hour =int(format_list[0]),minute=int(format_list[1]),second=int(format_list[2]))
								else:
									q_dict["opening_time"] = ''
									q_dict["closing_time"] = ''
									q_dict["opening_status_color"] = ''
									q_dict["closing_status_color"] = ''

								q_dict["is_pos_open"] = i.is_pos_open
								order_record = Order.objects.filter(
												Q(outlet_id=i.id),Q(order_status=6))
								if order_record.count() > 0:
									c = order_record.filter(order_time__year=year,\
									order_time__month=month,order_time__day=today)
									if c.count() > 0:
										order_result = c.values('Company').\
											annotate(total_revenue=Sum('total_bill_value'),order_count=Count("id"))
										if len(order_result) > 0:
											q_dict["total_sale"] = order_result[0]["total_revenue"]
											q_dict["total_order"] = order_result[0]["order_count"]
										else:
											q_dict["total_sale"] = 0
											q_dict["total_order"] = 0
									else:
										q_dict["total_sale"] = 0
										q_dict["total_order"] = 0
								else:
									q_dict["total_sale"] = 0
									q_dict["total_order"] = 0
								final_result.append(q_dict)
			print("xxxxxxxxxxxxxxxxxxxx",final_result)
			return Response({
						"success": True, 
						"message": "Outlet Listing api worked well!!",
						"data": final_result,
						})
		except Exception as e:
			print("Outlet listing Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})

