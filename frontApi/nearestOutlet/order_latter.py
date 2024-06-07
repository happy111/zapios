import calendar
from datetime import datetime

from django.db.models import Q
from django.db.models import Count

from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile,OutletTiming
from frontApi.serializer.restaurent_serializers import OutletDetailsSerializer
from Brands.models import Company
from googlegeocoder import GoogleGeocoder
from googlemaps import Client
from geopy.geocoders import Nominatim
from geopy.distance import great_circle
from Location.models import CityMaster,AreaMaster
from rest_framework_tracking.mixins import LoggingMixin
from datetime import datetime, timedelta
import time


class OrderLatter(LoggingMixin, APIView):
	"""
	Schedule order  POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used to Schedule order check outlet close / open

		Data Post: {

			"outlet"	    :	"64",
			"delivery_time"	:	"2020-09-18 08:25:00",
			"time"          : 

		}

		Response: {

			"status"				: True,
			"nearest_restaurants"	: self.customer_nearest_restaurent,
			"message"				: "Your nearest restaurant are sent successfully"
		}

	"""
	def post(self,request):
		try:
			data = request.data
			err_message = {}
			delivery_date = data['delivery_date']
			dt = datetime.strptime(delivery_date, '%Y-%m-%d')

			dt = datetime.strptime(delivery_date, '%Y-%m-%d')
			today = dt.strftime('%A')
			to_let = 0
			delivery_time = data['delivery_time'].split('-')
			range1 = delivery_time[0]
			range2 = delivery_time[1]
			
			chk_out = OutletTiming.objects.filter(day=today,outlet_id=data['outlet'])
			if chk_out.count() > 0:
				for index in chk_out:
					k = 1
					open_time = index.opening_time
					close_time = index.closing_time
					time = dt.time()
					time_str = range1.strip()
					time1 = datetime.strptime(time_str, '%H:%M').time()
					time_str2 = range2.strip()
					time2 = datetime.strptime(time_str2, '%H:%M').time()
					if open_time > close_time:
						c_tmp = open_time
						open_time = close_time
						close_time = c_tmp
						if time1 > open_time and time2 < close_time:
							pass
						else:
							to_let = 1
					else:
						if time1 >= open_time and time2 <= close_time:
							to_let = 1
						else:
							pass
					if to_let == 1:
						return Response({"success": True,
										 "message": "Order is Proceed",
							   })
					else:
						return Response({"success": False,
										 "message": "Outlet is closed",
							   })
			else:
				return Response({"success": False,
								 "message": "Outlet timing is not set",
							   })
		except Exception as e:
			print(e)