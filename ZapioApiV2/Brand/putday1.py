from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.Api.BrandApi.Validation.outlet_error_check import *
from _thread import start_new_thread
from django.db.models import Avg, Max, Min, Sum
#Serializer for api
from rest_framework import serializers
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user
from Brands.models import Company
from UserRole.models import *
from django.db.models import Q
from History.models import Logs
from Event.models import PrimaryEventType
from Orders.models import *
from Location.models import *
from geopy.geocoders import Nominatim
from geopy.distance import great_circle


class LogSerializer(serializers.ModelSerializer):
	class Meta:
		model = Logs
		fields = '__all__'

def FindLatitude(area):
	import requests
	GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'
	params = {
	    'address': area,
	    'sensor': 'false',
	    'region': 'india',
	    'key': "AIzaSyCIDUSBqHPfkEssENT_X9vuWt5nzca8_W4"
	}
	req = requests.get(GOOGLE_MAPS_API_URL, params=params)
	res = req.json()

	result = res['results'][0]
	geodata = dict()
	geodata['lat'] = result['geometry']['location']['lat']
	geodata['lng'] = result['geometry']['location']['lng']
	geodata['address'] = result['formatted_address']
	return geodata['lat'],geodata['lng']


class Putday(APIView):
	"""
	Brand Creation POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create new brand.

		Data Post: {
			
			"event_name"  : "kot/bill"
			"order_id"    : "32432432432432"
		}

		Response: {

			"success": True,
			"message": "Outlet is registered successfully under your brand!!"
		}

	"""

	# def post(self, request, format=None):
	# 	try:
	# 		from Brands.models import Company
			
	# 		outledata = OutletProfile.objects.filter()
	# 		for i in outledata:
	# 			alldata = {}
	# 			latitude,longitude = FindLatitude(i.address)
	# 			alldata['latitude'] = latitude
	# 			alldata['longitude'] = longitude
	# 			data = OutletProfile.objects.filter(id=i.id)
	# 			data.update(latitude=latitude,longitude=longitude)
	# 		return response({
	# 			"success" :"yes"
	# 			})

	# 	except Exception as e:
	# 		print("Brand Creation Api Stucked into exception!!")
	# 		print(e)
	# 		return Response({"success": False, "message": "Error happened!!", "errors": str(e)})



	def post(self, request, format=None):
			try:
				from Brands.models import Company
				orderdata = Order.objects.filter()
				for index in orderdata:
					address = index.address
					
					outledata = OutletProfile.objects.filter(id=index.outlet_id)
					if outledata.count() > 0:
						outletdetails = outledata[0]
					else:
						continue
					for i in address:
						if len(i) > 0:
							if 'address' in i:
								if i['address'] != '':
									print("sssssssssssssssssssss",i['address'])
									alldata = {}
									latitude,longitude = FindLatitude(i['address'])
									alldata['latitude'] = latitude
									alldata['longitude'] = longitude
									print("llllllllllllllllllllllllll",alldata['latitude'])

									print("llllllllllllllllllllllllll",alldata['longitude'])

									if (
										alldata["latitude"] != None
										and alldata["longitude"] != None
										and alldata["latitude"] != ""
										and alldata["longitude"] != ""
										and outletdetails.latitude != None
										and outletdetails.longitude != None
										and outletdetails.latitude != ""
										and outletdetails.longitude != ""
										and outletdetails.latitude != "undefined"
										and outletdetails.longitude != "undefined"
									):
										customer_location = (alldata["latitude"], alldata["longitude"])
										outlet_location = (outletdetails.latitude, outletdetails.longitude)
										unloaded_mile = great_circle(outlet_location, customer_location).miles
										kilometers = round((unloaded_mile // 0.62137119), 2)
										distancd = kilometers
										print("ssssssssssssssssssssss",distancd)

										data = Order.objects.filter(id=index.id)
										data.update(distance=distancd)


				return response({
					"success" :"yes"
					})

			except Exception as e:
				print("Brand Creation Api Stucked into exception!!")
				print(e)
				return Response({"success": False, "message": "Error happened!!", "errors": str(e)})