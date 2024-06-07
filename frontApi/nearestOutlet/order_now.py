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



class DeliveryView(LoggingMixin, APIView):
	"""
	Schedule order  POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used to Schedule order check outlet close / open

		Data Post: {

			"outlet"	    :	"64",
			"delivery_time"	:	"2020-09-18 08:25:00"

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
			delivery_time = data['delivery_time']
			dt = datetime.strptime(delivery_time, '%Y-%m-%d %H:%M:%S')
			if data['delivery_time'] == '':
				err_message["delivery_time"] = "Please Enter delivery_time!!"
			else:
				now = datetime.now()
				if dt < now:
					err_message["delivery_time"] = "Delivery time is smaller than present datetime!!"
				else:
					pass
			if any(err_message.values())==True:
				return Response({
					"success"   : False,
					"error"     : err_message,
					"message"   : "Please correct listed errors!!"
					})
			dt = datetime.strptime(delivery_time, '%Y-%m-%d %H:%M:%S')
			today = dt.strftime('%A')
			to_let = 0
			chk_out = OutletTiming.objects.filter(day=today,outlet_id=data['outlet'])
			if chk_out.count() > 0:
				for index in chk_out:
					k = 1
					open_time = index.opening_time
					close_time = index.closing_time
					time = dt.time()
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