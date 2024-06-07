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


class NearestMapView(LoggingMixin, APIView):
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

	def restaurant_details_records(self):
		all_restaurant =\
		OutletProfile.objects.filter(active_status=1,is_pos_open=1,
			Company=self.Company,is_hide=0).order_by('latitude')

		if all_restaurant.count() > 0:
			self.Restaurants = OutletDetailsSerializer(all_restaurant, many=True).data
		else:
			return Response({"status": True,
							"message": "The location you entered is outside of our service area.",
							})
		self.restaurant_miles_converter()
		if self.customer_nearest_restaurent == []:
			nearest = {}
			for restaurant in self.Restaurants:
				if restaurant['latitude'] != 'undefined' and restaurant['longitude'] !='undefined':
					restaurant_locations = (restaurant['latitude'], restaurant['longitude'])
					unloaded_mile = great_circle(self.customer_location, restaurant_locations).miles
					if unloaded_mile == None:
						unloaded_mile = 0
					else:
						kilometers = round((unloaded_mile / 0.62137119), 2)
						nearest[restaurant['Outletname']] = kilometers
			if len(nearest) > 0:
				for key, value in nearest.items():
					restaurant = OutletProfile.objects.filter(Outletname=key).first()
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
								restaurant_data['temperature_check'] = restaurant.temperature_check
								restaurant_data['clean_kitchen'] = restaurant.clean_kitchen
								restaurant_data['sanitized_restaurant'] = restaurant.sanitized_restaurant
								restaurant_data['distance'] = value
								restaurant_data['address'] = restaurant.address
								restaurant_data['is_open'] = restaurant.is_open
								restaurant_data['min_order'] = restaurant.min_value
								restaurant_data['delivery_time'] = restaurant.average_delivery_time
								full_path = addr_set()
								if restaurant.outlet_image != None and restaurant.outlet_image !="":
									restaurant_data["outlet_image"] = full_path+str(restaurant.outlet_image)
								else:
									restaurant_data["outlet_image"] = None
								restaurant_data['latitude'] = restaurant.latitude
								restaurant_data['longitude'] = restaurant.longitude
								restaurant_data['latitude'] = restaurant.latitude
								cdata = CountryMaster.objects.filter(id=restaurant.country_id)
								if cdata.count() > 0:
									restaurant_data['country'] = cdata[0].country
								s = StateMaster.objects.filter(id=restaurant.state_id)
								if s.count() > 0:
									restaurant_data['state'] = StateMaster.objects.filter(id=restaurant.state_id)[0].state
								else:
									restaurant_data['state'] = ''
								restaurant_data['city'] = []
								cityDetail = restaurant.map_city
								if cityDetail !=None:
									for index in cityDetail:
										cat_dict = {}
										cat_dict["label"] = CityMaster.objects.filter(id=index)[0].city
										cat_dict['value'] = index
										restaurant_data['city'].append(cat_dict)
								else:
									pass
								areaDetail = restaurant.map_locality
								restaurant_data["area_detail"] = []
								if areaDetail !=None:
									for index in areaDetail:
										ara_dict = {}
										ara_dict["label"] = AreaMaster.objects.filter(id=index)[0].area
										ara_dict['value'] = index
										restaurant_data["area_detail"].append(ara_dict)
								else:
									pass
								restaurant_data['no_of_days'] = restaurant.no_of_days
								if restaurant.time_range != None:
									restaurant_data['time_range'] = restaurant.time_range.split(" ")[0]
								else:
									restaurant_data['time_range'] = ''
								now = datetime.now()
								today = now.strftime('%A')
								tdata = OutletTiming.objects.filter(Company_id=self.Company,outlet_id=restaurant.id)
								if tdata.count() > 0:
									restaurant_data["outlet_time"] = []
									for index in tdata:
										di = {}
										di['open_time'] = str(index.opening_time).split(":")[0] + ":"  +str(index.opening_time).split(":")[1]
										di['close_time'] = str(index.closing_time).split(":")[0] + ":"+  str(index.closing_time).split(":")[1]
										di['day'] = index.day
										restaurant_data['outlet_time'].append(di)
								else:
									pass
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
				   "message": "The location you entered is outside of our service area."
				})

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
				time = datetime.time(datetime.now())
				chk_com = OutletProfile.objects.filter(active_status=1,is_open=1,\
					Company=self.Company).order_by('latitude')
				if chk_com.count() > 0:
					pass
				else:
					return Response({"success": False,
									 "message": "Outlet is closed or inactive!!",
								})
				a = self.restaurant_details_records()
				if a == "s":
					return Response({"success": False,
									 "message": " Our restaurant is closed at the moment, if you would like to place an order in advance, please use the 'order for later' button to place your order",
									})
				else:
					pass

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
								 "message": "The location you entered is outside of our service area.",
								 "range"  : self.range_in_kilometer})
			else:
				pass
		except Exception as e:
			print(e)


