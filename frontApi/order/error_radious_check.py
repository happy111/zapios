from Outlet.models import OutletProfile, OutletMilesRules
from Brands.models import Company
from googlegeocoder import GoogleGeocoder
from googlemaps import Client
from geopy.geocoders import Nominatim
from geopy.distance import great_circle
from ZapioApi.api_packages import *



def check_circle(data):
	err_message = {} 
	err_message["shop_id"] = \
			validation_master_anything(str(data["shop_id"]),
			"Shop Id", contact_re, 1)
	err_message["lat"] = \
			validation_master_anything(str(data["lat"]),
			"Latitude", lat_long_re, 3)
	err_message["long"] = \
			validation_master_anything(str(data["long"]),
			"Longitude", lat_long_re, 3)
	if any(err_message.values())==True:
		err = {
			"success": False,
			"error" : err_message,
			"message" : "Please correct listed errors!!"
			}
		return err
	else:
		pass
	shop_check = OutletProfile.objects.filter(id=data["shop_id"])
	if shop_check.count()==0:
		err = {
			"success": False,
			"message" : "Shop Id data is not valid!!"
			}
		return err
	else:
		pass
	shop_lat = shop_check[0].latitude
	shop_long = shop_check[0].longitude
	restaurant_location = (shop_lat, shop_long)
	customer_location = (data["lat"],data["long"])
	miles = great_circle(customer_location, restaurant_location).miles
	km_distance = 0
	if miles == None:
		km_distance = 0
	else:
		km_distance = round((miles / 0.62137119), 2)
	company_id = shop_check[0].Company_id
	service_q = OutletMilesRules.objects.filter(Company=company_id,active_status=1)
	if service_q.count() == 0:
		err = {
			"success": False,
			"message" : "Service radious is not set for this outlet at super-admin level!!"
			}
		return err
	else:
		pass
	service_in_kms = service_q[0].unloaded_miles
	

	if km_distance <= service_in_kms:
		return None
	else:
		err = {
			"success": False,
			"message" : "Please change your delivery address..Sorry for inconvenience!!"
		}
		return err






