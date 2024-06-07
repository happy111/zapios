from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_201_CREATED, \
	HTTP_406_NOT_ACCEPTABLE, HTTP_200_OK, HTTP_503_SERVICE_UNAVAILABLE
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.sites.shortcuts import get_current_site
from ZapioApi.Api.BrandApi.profile.profile import CompanySerializer
from Brands.models import Company
from django.db import transaction

#Serializer for api
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from Product.models import FeatureProduct,Product
from Outlet.models import OutletProfile,OutletTiming
from Customers.models import CustomerProfile
from Location.models import *
from google.oauth2 import id_token
from google.auth.transport import requests
from datetime import datetime
from Product.models import Menu

def addr_set():
	domain_name = "http://zapio-admin.com/media/"
	return domain_name



class FeatureListing(APIView):
	"""
	User listing GET API

		Authentication Required		: No
		Service Usage & Description	: This Api is used for listing of User data within brand.
	"""
	# permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		url = request.data['wurl']
		company_data = Company.objects.filter(website=url).first()
		if company_data:
			featureData = FeatureProduct.objects.filter(company=company_data.id).first()
			feature_product_id = featureData.feature_product
			pro_data =[]
			domain_name = addr_set()
			for i in feature_product_id:
				p_list ={}
				product_data = Product.objects.filter(id=i).first()
				p_list['product_name'] = product_data.product_name
				p_list['product_code'] = product_data.product_code
				p_list['product_desc'] = product_data.product_desc
				if product_data.product_image != "" and product_data.product_image != None:
					full_path = domain_name + str(product_data.product_image)
					p_list['product_image'] = full_path
				pro_data.append(p_list)
			return Response({"status":True,
							"data":pro_data})


class LogoBanner(APIView):
	"""
	User listing GET API

		Authentication Required		: No
		Service Usage & Description	: This Api is used for listing of User data within brand.
	"""
	# permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		url = request.data['wurl']
		company_data = Company.objects.filter(website=url).first()
		domain_name = addr_set()
		p_list={}
		pdata = []
		if company_data.company_logo != "" and company_data.company_logo != None:
			full_path = domain_name + str(company_data.company_logo)
			p_list['logo'] = full_path
		if company_data.company_landing_imge != "" and company_data.company_landing_imge != None:
			full_path1 = domain_name + str(company_data.company_landing_imge)
			p_list['banner'] = full_path1
		pdata.append(p_list)
		return Response({"status":True,
							"data":pdata})








class FrontLogin(APIView):

	"""	
	Google Signup/ Signin POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used to provide google signup/signin services to users.

		Data Post: {
				"token"         :"token",
				"company_id"    : 1
		}

		Response: {

			"success"				: true,
			"message"				: "Register Successfully!!",

		}

	"""
	
	def post(self, request, format=None):
		try:
			data = request.data
			CLIENT_ID = "435927262966-kd4rrlpflk2an87qi1qblbet4v871n16.apps.googleusercontent.com"
			try:
			    idinfo = id_token.verify_oauth2_token(data['token'], requests.Request(), CLIENT_ID)
			    userid = idinfo['sub']
			    data["email"] = idinfo['email']
			    data['first_name'] = idinfo['given_name']
			    data['last_name'] = idinfo['family_name']
			    data['full_name'] = data['first_name'] + ' ' + data['last_name']
			except ValueError:
				raise Exception("Invalid token!!")
			cus_data = CustomerProfile.objects.filter(email=data['email'],company_id=data['company_id'])
			final_result = []
			if cus_data.count() > 0:
				update_data = cus_data.update(is_google=1)
				adress_data = cus_data[0].address1
				if adress_data != None and len(adress_data) > 0:
					adress_data = cus_data[0].address1
					for k in adress_data:
						di = {}
						if cus_data[0].name != None:
							di['first_name'] = cus_data[0].name.split(' ')[0]
							if len(cus_data[0].name.split(' ')) >= 2:
								di['last_name'] = cus_data[0].name.split(' ')[1]
							else:
								di['last_name'] = ''
						di['email']  = cus_data[0].email
						di['phone']  = cus_data[0].mobile
						if 'city' in k:
							di['city']  = k['city']
						else:
							di['city'] = ''
						if 'state' in k:
							di['state']  = k['state']
						else:
							di['state'] = ''
						if 'address' in k:
							di['address'] = k['address']
						else:
							di['address'] = ''
						if 'pincode' in k:
							di['pincode'] = k['pincode']
						else:
							di['pincode'] = ''
						di['locality'] = k['locality']
						di['address_type'] = k['address_type']
						final_result.append(di)
				if len(final_result) > 0:
					pass
				else:
					di={}
					di['first_name'] = data['first_name']
					di['last_name'] = data['last_name']
					di['email'] = data['email']
					final_result.append(di)
				return Response({
							"status": True,
							"message": "login Successfully!!",
							"data" : final_result
							},status=HTTP_200_OK,)
			else:
				cus_data = CustomerProfile.objects.create(email=data['email'],
					company_id=data['company_id'],\
					username=data['email'],is_google=1,name=data['full_name'])
				di={}
				di['first_name'] = data['first_name']
				di['last_name'] = data['last_name']
				di['email'] = data['email']
				final_result.append(di)
				if cus_data:
					return Response({
							"status": True,
							"message": "Register Successfully!!",
							"data" : final_result
							},status=HTTP_200_OK,)
		except Exception as e:
			return Response({"message": str(e)}, status=HTTP_406_NOT_ACCEPTABLE)








class AllOutletsView(APIView):
	"""
	Nearest Restaurant POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used to find nearest outlet on the basis of provided lat & 
		long.City and area are optional, request can be made by assigning values in city and area 
		as blank.

		Data Post: {
			"company"   :   "1"
		}

		Response: {

			"status"				: True,
			"nearest_restaurants"	: self.customer_nearest_restaurent,
			"message"				: "Your nearest restaurant are sent successfully"
		}

	"""

	def __init__(self):
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
	
	def chk_open_restaurents(self, restaurant):
		try:
			print(restaurant)
		except Exception as e:
			print("merge_all_nearest_restaurents_exception")
			print(e)
			return None, e

	def restaurant_details_records(self):
		all_restaurant =\
		OutletProfile.objects.filter(active_status=1,is_pos_open=1,
			Company=self.Company,is_hide=0)
		

		if all_restaurant.count() > 0:
			for restaurant in all_restaurant:
				restaurant_data = {}
				restaurant_data['id'] = restaurant.id
				restaurant_data['Outletname'] = restaurant.Outletname
				# restaurant_data['distance'] = value
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
				# if len(restaurant.delivery_zone) > 0:
				# 	for index in restaurant.delivery_zone:
				# 		temp = {}
						# if float(index['start']) <= float(restaurant_data['distance']) and float(index['end']) >= float(restaurant_data['distance']):
						# 	temp['price_type'] = index['price_type']['label']
						# 	temp['amount'] = float(index['amount'])
						# 	temp['tax_detail'] = []
						# 	if index['isTax'] == False:
						# 		pass
						# 	else:
						# 		for k in index['taxes']:
						# 			ta = Tax.objects.filter(id=str(k['value']))
						# 			if ta.count() > 0:
						# 				d = {}
						# 				d['tax_name']  = ta[0].tax_name
						# 				d['percentage'] = float(ta[0].tax_percent)
						# 				temp['tax_detail'].append(d)
						# 	restaurant_data['delivery_charge'].append(temp)
				self.customer_nearest_restaurent.append(restaurant_data)

		else:
			return Response({"status": True,
							"message": "Sorry, we do not currently deliver in your location.",
							})

		




	def post(self,request):
		from Outlet.models import OutletMilesRules
		try:
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

			time = datetime.time(datetime.now())
			chk_com = OutletProfile.objects.filter(active_status=1,is_open=1,\
				Company=self.Company)

			if chk_com.count() > 0:
				pass
			else:
				return Response({"success": False,
								 "message": "Outlet is closed or inactive!!",
							})
			a = self.restaurant_details_records()
			
			return_json_response = {
				"success": True,
				"nearest_restaurants": self.customer_nearest_restaurent,
				"message": "Your nearest restaurant are send successfully"
			}
			return Response(return_json_response)
			


		except Exception as e:
			print(e)




class listMenu(APIView):

	def post(self, request, format=None):
		try:
			data = request.data
			allsource = Menu.objects.filter(company_id=data['company'],is_hide=0).order_by('id')
			final_result = []
			if allsource.count() > 0:
				for i in allsource:
					dict_source = {}
					dict_source['menu_name'] = i.menu_name
					dict_source['id'] = i.id
					dict_source['active_status'] = i.active_status
					dict_source['img'] = i.base_code
					im = str(i.menu_image)
					if im != "" and im != None and im != "null":
						domain_name = addr_set()
						full_path = domain_name + str(i.menu_image)
						dict_source['menu_image'] = full_path
					else:
						pass
					bc = str(i.barcode_pic)
					if bc != "" and bc != None and bc != "null":
						domain_name = addr_set()
						full_path = domain_name 
						dict_source['qr_code'] = full_path + str('barcode') +'/' + str(i.barcode_pic)
					else:
						dict_source['qr_code']  = ''
					final_result.append(dict_source)
				return Response({
						"success": True, 
						"data": final_result})
			else:
				return Response({
						"success": True, 
						"data": []})
		except Exception as e:
			print("Menu listing Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})