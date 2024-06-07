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
from Location.models import *
from rest_framework_tracking.mixins import LoggingMixin
from datetime import datetime, timedelta
from ZapioApi.api_packages import *
from Configuration.models import *
from rest_framework.permissions import IsAuthenticated
from UserRole.models import ManagerProfile, UserType

class RestaurantMapView(LoggingMixin, APIView):
	"""
	Nearest Restaurant POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used to find nearest outlet on the basis of provided lat & 
		long.City and area are optional, request can be made by assigning values in city and area 
		as blank.

		Data Post: {
		
			"latitude"	:	"41.90278349999999",
			"longitude"	:	"12.4963655",
			"company"   :   "1"
		}

		Response: {

			"status"				: True,
			"nearest_restaurants"	: self.customer_nearest_restaurent,
			"message"				: "Your nearest restaurant are sent successfully"
		}

	"""

	def __init__(self):
		self.latitude = None
		self.longitude = None
		self.city = None
		self.area = None
		self.customer_location = None
		self.myLocation = None
		self.config_rule_name = None
		self.config_unloaded_miles = 0
		self.range_in_kilometer = None
		self.customer_nearest_restaurent = []
		self.response_api_message = None
		self.Errors = None
		self.Company = None

	def restaurant_miles_converter(self):
		self.customer_location = (self.latitude, self.longitude)


	def restaurant_details_records(self,outlet):
		all_restaurant =\
		OutletProfile.objects.filter(active_status=1,is_pos_open=1,
			id__in=outlet,).order_by('latitude')
		if all_restaurant.count() > 0:
			self.Restaurants = OutletDetailsSerializer(all_restaurant, many=True).data
		else:
			return Response({"status": True,
							"message": "Sorry, we do not currently deliver in your location.",
							})
		self.restaurant_miles_converter()
		if self.customer_nearest_restaurent == []:
			nearest = {}
			to_let = 0
			k = 0
			flag = 0
			for restaurant in self.Restaurants:
				now = datetime.now()
				today = now.strftime('%A')
				time = datetime.now().time()
				chk_out = OutletTiming.objects.filter(day=today,outlet_id=restaurant['id'])
				if chk_out.count() > 0:
					flag = 1
					for index in chk_out:
						k = 1
						open_time = index.opening_time
						close_time = index.closing_time
						cur = time.strftime('%H:%M:%S')
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
								if restaurant['latitude'] != 'undefined' and restaurant['longitude'] != 'undefined':
									restaurant_locations = (restaurant['latitude'], restaurant['longitude'])
									unloaded_mile = great_circle(self.customer_location, restaurant_locations).miles
									if unloaded_mile == None:
										unloaded_mile = 0
									else:
										kilometers = round((unloaded_mile / 0.62137119), 2)
										nearest[restaurant['Outletname']] = kilometers
										a=min(zip(nearest.values(), nearest.keys()))
							else:
								pass
				else:
					pass
			if flag == 0:
				return 'Q'
			if to_let == 0:
				return 's'
			if len(nearest) > 0:
				for key, value in nearest.items():
					restaurant = OutletProfile.objects.filter(Outletname=key,).first()
					start = []
					end = []
					if restaurant.delivery_zone != None:
						if len(restaurant.delivery_zone) > 0:
							for index in restaurant.delivery_zone:
								start.append(int(index['start']))
								end.append(int(index['end']))
							start_km = min(start)
							end_km = max(end)
							if float(start_km) <= float(value) and float(end_km) >= float(value):
								restaurant_data = {}
								restaurant_data['id'] = restaurant.id
								restaurant_data['Outletname'] = restaurant.Outletname
								restaurant_data['distance'] = value
								restaurant_data['address'] = restaurant.address
								restaurant_data['is_open'] = restaurant.is_pos_open
								full_path = addr_set()
								if restaurant.outlet_image != None and restaurant.outlet_image !="":
									restaurant_data["outlet_image"] = full_path+str(restaurant.outlet_image)
								else:
									restaurant_data["outlet_image"] = None
								restaurant_data['delivery_charge'] = []
								if len(restaurant.delivery_zone) > 0:
									for index in restaurant.delivery_zone:
										temp = {}
										if float(index['start']) <= float(restaurant_data['distance']) and float(index['end']) >= float(restaurant_data['distance']):
											temp['price_type'] = index['price_type']['label']
											temp['amount'] = float(index['amount'])
											if 'min_order' in index:
												temp['min_order'] = index['min_order']
											else:
												temp['min_order'] = 0
											temp['tax_detail'] = []
											if index['isTax'] == False:
												pass
											else:
												for k in index['taxes']:
													ta = Tax.objects.filter(id=str(k['value']))
													if ta.count() > 0:
														d = {}
														d['tax_name']  = ta[0].tax_name
														d['percentage'] = float(ta[0].tax_percent)
														temp['tax_detail'].append(d)
											restaurant_data['delivery_charge'].append(temp)
								self.customer_nearest_restaurent.append(restaurant_data)
			else:
				pass
			if len(self.customer_nearest_restaurent) == 0:
				return Response({
					"status": True,
				   "message": "Sorry, we do not currently deliver in your location.",
				})


	permission_classes = (IsAuthenticated,)
	def post(self,request):
		from Outlet.models import OutletMilesRules
		try:
			self.latitude = request.data['latitude']
			self.longitude = request.data['longitude']
			self.Company = request.data['company']
			company_check = Company.objects.filter(id=self.Company,active_status=1)
			if company_check.count()==0:
				return Response({"success"  : False,
								 "message" : "Sorry Company is not active!!",
								})
			else:
				pass
			company_check = Company.objects.filter(id=self.Company,is_open=1)
			if company_check.count()==0:
				return Response({"success"  : False,
								 "message" : "Sorry we are closed now!!",
								})
			else:
				pass
			outlet_data = OutletProfile.objects.filter(Company_id=self.Company)
			if outlet_data.count()==0:
				return Response({"success"  : False,
								 "message" : "No outlet is linked to company!!",
								})
			else:
				pass
			if self.longitude != "" and self.longitude != "":
				outlet_data = ManagerProfile.objects.filter(auth_user_id=self.request.user.id,Company_id=self.Company)
				if outlet_data.count() > 0:
					outlet = outlet_data[0].outlet
				else:
					return Response({
						"success": False,
						"message": "No outlet linked!!",
								})
				chk_com = OutletProfile.objects.filter(active_status=1,is_open=1,\
					id__in=outlet).order_by('latitude')
				if chk_com.count() > 0:
					pass
				else:
					return Response({"success": False,
									 "message": "Outlet is closed or inactive!!",
								})

				a = self.restaurant_details_records(outlet)
				if a == "s":
					return Response({"success": False,
									 "message": "Restaurants is closed",
									})
				else:
					pass
				if a == "Q":
					return Response({"success": False,
									 "message": "Outlet timeing is not set",
									})
				if self.customer_nearest_restaurent:
					for i in self.customer_nearest_restaurent:
						outlet_id = i['id']
					outlet_data = OutletProfile.objects.filter(id=outlet_id)
					if outlet_data.count() > 0:
						cid = outlet_data[0].Company_id
						name = outlet_data[0].Company.company_name
						save_wev = WebsiteStatistic.objects.create(name=name,\
						menu_views=1,company_id=cid)
					return_json_response = {
						"success": True,
						"nearest_restaurants": self.customer_nearest_restaurent,
						"message": "Your nearest restaurant are send successfully"
					}
					return Response(return_json_response)
				return Response({"success": False,
								 "message": "Out of service area!!",
								 "range"  : self.range_in_kilometer})
			else:
				pass
		except Exception as e:
			print(e)
