import re
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from ZapioApi.Api.BrandApi.Validation.outlet_error_check import *
from _thread import start_new_thread
from django.db.models import Avg, Max, Min, Sum
from rest_framework import serializers
from Outlet.models import OutletProfile
from Product.models import *
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user
from Brands.models import Company
from Configuration.models import HeaderFooter
from Outlet.models import OutletTiming,OutletTimingMaster
from datetime import datetime
import dateutil.parser
from Location.models import *
from rest_framework.status import (
	HTTP_200_OK,
	HTTP_406_NOT_ACCEPTABLE,
	HTTP_400_BAD_REQUEST,
	HTTP_404_NOT_FOUND,
	HTTP_500_INTERNAL_SERVER_ERROR,
	HTTP_204_NO_CONTENT,
)
from django.db import transaction
from django.http import Http404
from django.utils.translation import gettext_lazy


class OutletProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = OutletProfile
		fields = '__all__'


def map_products_to_outlet(outlet_id, auth_id):
	cdata = Company.objects.filter(auth_user_id=auth_id)[0].id
	product = Product.objects.filter(active_status=1,Company_id=cdata)
	
	category = ProductCategory.objects.filter(active_status=1,Company__auth_user=auth_id)
	now = datetime.now()
	available_category = []
	for i in category:
		available_category.append(i.id)
	cat_availability = Category_availability.objects.filter(outlet_id=outlet_id)
	if cat_availability.count() == 0:
		availability_create = Category_availability.objects.\
		create(outlet_id=outlet_id,available_cat=available_category,created_at=now)
	else:
		pass
	available_product = []
	for i in product:
		available_product.append(i.id)
	outlet_availability = Product_availability.objects.filter(outlet_id=outlet_id)
	if outlet_availability.count() == 0:
		availability_create = Product_availability.objects.\
		create(outlet_id=outlet_id,available_product=available_product,created_at=now)
	else:
		pass
	return "Products & Categories are Mapped!!"


class OutletSerializer(serializers.ModelSerializer):
	class Meta:
		model = OutletProfile
		fields = '__all__'



class OutletCreation(APIView):
	"""
	Outlet Creation POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create new outlets within brand.

		Data Post: {
			

			"Outletname" 			: "Adarsh Nagar, Jalandhar",
			"company_auth_id" 	    : "3",
			"latitude"              : "31.32990749999999",
			"longitude"             : "75.56381729999998",
			"address"               : "Punjab 144002, India",
			"country"               : "1",
			"city"                  : "delhi",
			"location"              : 'hari nagar ashram'
			"landmark"              : "delhi",
			"pincode"               : '110016'
			"outlet_image"          : "a.jpg",
			"min_order_value"       : "200",
			"average_delivery_time" : "1.15",
			"outlet_instagram"      : '',
			"map_city"              : [],
			"map_locality"          : [],
			"prefecture"					: "1",
			"no_of_days"            : "5",
			"time_range"            : "15",
			"sanitized_restaurant"  : 0,
			"temperature_check"     : 0,
			"clean_kitchen"         : 0
		}

		Response: {

			"success": True,
			"message": "Outlet is registered successfully under your brand!!"
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			auth_id = request.user.id
			cid = get_user(auth_id)
			if 'sanitized_restaurant' in data:
				pass
			else:
				data['sanitized_restaurant'] = 0
			if 'temperature_check' in data:
				pass
			else:
				data['temperature_check'] = 0
			if 'clean_kitchen' in data:
				pass
			else:
				data['clean_kitchen'] = 0
			if data['tab'] == str(0):
				validation_check = err_check(data)
				if validation_check != None:
					return Response(validation_check)
				maxp = OutletProfile.objects.filter(Company=cid).aggregate(Max('priority'))
				if maxp['priority__max'] !=None:
					priority = maxp['priority__max']
				else:
					priority = 0
				data['priority'] = priority + 1
				if data['id']:
					pass
				else:
					outlet_name_check = \
					OutletProfile.objects.filter(Outletname__iexact=data["Outletname"],Company=cid)
					if outlet_name_check.count() == 1:
						err_message = {}
						err_message["Outletname"] = \
						gettext_lazy("Outlet with this name already exists..Please try other!!")
						if any(err_message.values())==True:
							return Response({
								"success": False,
								"error" : err_message,
								"message" : "Please correct listed errors!!"
								})

				company_query = Company.objects.filter(id=cid)
				if company_query.count() != 0:
					data["Company"] = company_query[0].id
				else:
					return Response(
						{
							"success": False,
							"message": "Company is not valid!!"
						}
						)
				data['is_company_active'] =  1
				data['is_open'] =  1
				data['active_status'] =  1
				data['is_pos_open'] =  1
				data['min_value'] = data['min_order_value']
				if type(data['min_value']) == str:
					data['min_value'] = 0
				else:
					data['min_value'] = data['min_order_value']
				if data['id']:
					record = OutletProfile.objects.filter(id=data['id'])
					p_query = \
						record.update(Company_id=cid,\
						outlet_image=data["outlet_image"],
						Outletname=data["Outletname"],\
						address=data["address"],
						ip_address = data['ip_address'],
						priority=data["priority"],
						country_id=data["country"],\
						prefecture=data['prefecture'],\
						city=data["city"],
						pincode=data["pincode"],\
						landmark=data['landmark'],\
						active_status=data["active_status"],
						created_at=datetime.now(),\
						is_company_active=data["is_company_active"],\
						is_open=data["is_open"],
						is_pos_open=data["is_pos_open"],
						min_value=data['min_value'],
						radius = data['radius'],
						sanitized_restaurant = data['sanitized_restaurant'],
						temperature_check = data['temperature_check'],
						clean_kitchen = data['clean_kitchen'],
						acceptance = data['acceptance'],
						processing = data['processing'],
						dispatch = data['dispatch']
						)
					if data["outlet_image"] != None and data["outlet_image"] != "":
						outlet = OutletProfile.objects.get(id=data["id"])
						outlet.outlet_image = data["outlet_image"]
						outlet.save()
					return Response(
								{
						"success": True,
						"message": gettext_lazy("Outlet is updated successfully under your brand!!"),
						"outlet_id": data['id']
								}
								)

				else:
					p_query = \
						OutletProfile.objects.create(Company_id=cid,\
						outlet_image=data["outlet_image"],
						Outletname=data["Outletname"],\
						address=data["address"],
						priority=data["priority"],
						country_id=data["country"],\
						prefecture=data['prefecture'],\
						city=data["city"],
						ip_address = data['ip_address'],
						pincode=data["pincode"],\
						landmark=data['landmark'],\
						active_status=data["active_status"],
						created_at=datetime.now(),\
						is_company_active=data["is_company_active"],\
						is_open=data["is_open"],
						is_pos_open=data["is_pos_open"],
						min_value=data['min_value'],
						radius = data['radius'],
						sanitized_restaurant = data['sanitized_restaurant'],
						temperature_check = data['temperature_check'],
						clean_kitchen = data['clean_kitchen'],
						acceptance = data['acceptance'],
						processing = data['processing'],
						dispatch = data['dispatch']
						)
					outlet_id = p_query.id
					start_new_thread(map_products_to_outlet, (outlet_id,auth_id))
					return Response(
								{
						"success": True,
						"message": gettext_lazy("Outlet is registered successfully under your brand!!"),
						"outlet_id": outlet_id
								}
								)
			if data['tab'] == str(1):
				err_message = {}
				if any(err_message.values())==True:
					return Response({
						"success": False,
						"error" : err_message,
						"message" : "Please correct listed errors!!"
						})
				if data['average_delivery_time'] == '':
					date_time_str = '0:00'
					data['average_delivery_time'] = datetime.strptime(date_time_str, '%H:%M')
				else:
					pass
				record = OutletProfile.objects.filter(id=data['id'])
				p_query = record.update(
				# map_city=data["map_city"],
				# map_locality=data["map_locality"],\
				average_delivery_time=data['average_delivery_time']
				)
				if p_query:
					return Response(
							{
					"success": True,
					"message": "Outlet is registered successfully under your brand!!",
					"outlet_id": data['id']
							}
							)
			# if data['tab'] == str(2):
			# 	record = OutletProfile.objects.filter(id=data['id'])
			# 	p_query = record.update(
			# 	no_of_days=data["no_of_days"],
			# 	time_range=data["time_range"],\
			# 	)
			# 	if p_query:
			# 		return Response(
			# 				{
			# 		"success": True,
			# 		"message": "Outlet is registered successfully under your brand!!",
			# 		"outlet_id": data['id']
			# 				}
			# 				)
			# if data['tab'] == str(2):
			# 	unique_check = HeaderFooter.objects.filter(outlet_id=data["id"])
			# 	if unique_check.count() > 0:
			# 		data["updated_at"] = datetime.now()
			# 		p_query = \
			# 		unique_check.update(header_text=data["header"],\
			# 			footer_text=data["footer"],\
			# 			gst=data["gst"],\
			# 			updated_at=datetime.now())
			# 	else:
			# 		p_query = \
			# 		HeaderFooter.objects.create(outlet_id=data['id'],
			# 		header_text=data["header"],footer_text=data["footer"],\
			# 		gst=data["gst"],company_id=cid)
			# 	if p_query:
			# 		data_info=p_query
			# 		info_msg = gettext_lazy("Receipt Configuration is created successfully!!")
			# 		return Response({
			# 			"success": True, 
			# 			"message": info_msg,
			# 			"outlet_id": data['id']
			# 			})
			if data['tab'] == str(2):
				auth_id = request.user.id
				Company_id = get_user(auth_id)
				err_message = {}
				mflag = 0
				tuflag = 0
				wflag = 0
				thflag = 0
				fflag = 0
				sflag = 0
				suflag = 0
				if data['id'] == None:
					err_message["outlet"] = "Please Select outlet!!"
				else:
					pass
				unique_check = OutletTimingMaster.objects.filter(outlet_id=str(data['id']))
				if unique_check.count() > 0:
					err_message["unique_check"] = gettext_lazy("Outlet name already exists!!")
				data1 = json.loads(data["monday"])
				data['monday'] = data1
				data2 = json.loads(data["tuesday"])
				data['tuesday'] = data2
				data3 = json.loads(data["wednesday"])
				data['wednesday'] = data3
				data4 = json.loads(data["thursday"])
				data['thursday'] = data4
				data5 = json.loads(data["friday"])
				data['friday'] = data5
				data6 = json.loads(data["saturday"])
				data['saturday'] = data6
				data7 = json.loads(data["sunday"])
				data['sunday'] = data7


				if len(data['monday']) == 0 and  len(data['tuesday']) == 0 and len(data['wednesday']) == 0 and \
						len(data['thursday']) == 0 and len(data['friday']) == 0 and len(data['saturday']) == 0 and \
						len(data['sunday']) == 0:
					err_message["fill"] = "Please Fill Enter time!!"
				if any(err_message.values())==True:
					return Response({
						"success": False,
						"error" : err_message,
						"message" : "Please correct listed errors!!"
						})
				if "monday" in data and len(data['monday']) > 0:
					mdata = data['monday']
					i = 0
					for index in mdata:
						if index["openingTime"] == '':
							err_message["opentime"] = "Please Enter opening time for monday!!"
						if index["closingTime"] == '':
							err_message["closetime"] = "Please Enter closing time for monday!!"
						if index['openingTime'] != '' and index['closingTime'] !='' and i == 0:
							i = 1
							mot = dateutil.parser.parse(index["openingTime"]).time()
							mct = dateutil.parser.parse(index["closingTime"]).time()
							if mot > mct or mot == mct:
								err_message["time"] = \
									"Please provide meaningfull opening & closing time for monday!!" 
							else:
								pass
						if any(err_message.values())==True:
							mflag = 0
							return Response({
								"success": False,
								"error" : err_message,
								"message" : "Please correct listed errors!!"
								})
						else:
							mflag = 1

				if "tuesday" in data and len(data['tuesday']) > 0:
					mdata = data['tuesday']
					i = 0
					for index in mdata:
						if index["openingTime"] == '':
							err_message["opentime"] = "Please Enter opening time for tuesday!!"
						if index["closingTime"] == '':
							err_message["closetime"] = "Please Enter closing time for tuesday!!"
						if index['openingTime'] != '' and index['closingTime'] !='' and i == 0:
							i = 1
							mot = dateutil.parser.parse(index["openingTime"]).time()
							mct = dateutil.parser.parse(index["closingTime"]).time()
							if mot > mct or mot == mct:
								err_message["time"] = \
									"Please provide meaningfull opening & closing time for tuesday!!" 
							else:
								pass
						if any(err_message.values())==True:
							tuflag = 0
							return Response({
								"success": False,
								"error" : err_message,
								"message" : "Please correct listed errors!!"
								})
						else:
							tuflag = 1
				if "wednesday" in data and len(data['wednesday']) > 0:
					mdata = data['wednesday']
					i = 0
					for index in mdata:
						if index["openingTime"] == '':
							err_message["opentime"] = "Please Enter opening time for wednesday!!"
						if index["closingTime"] == '':
							err_message["closetime"] = "Please Enter closing time for wednesday!!"
						if index['openingTime'] != '' and index['closingTime'] !='' and i == 0:
							i = 1
							mot = dateutil.parser.parse(index["openingTime"]).time()
							mct = dateutil.parser.parse(index["closingTime"]).time()
							if mot > mct or mot == mct:
								err_message["time"] = \
									"Please provide meaningfull opening & closing time for wednesday!!" 
							else:
								pass
						if any(err_message.values())==True:
							wflag = 0
							return Response({
								"success": False,
								"error" : err_message,
								"message" : "Please correct listed errors!!"
								})	
						else:
							wflag = 1	


				if "thursday" in data and len(data['thursday']) > 0:
					mdata = data['thursday']
					i = 0
					for index in mdata:
						if index["openingTime"] == '':
							err_message["opentime"] = "Please Enter opening time for thursday!!"
						if index["closingTime"] == '':
							err_message["closetime"] = "Please Enter closing time for thursday!!"
						if index['openingTime'] != '' and index['closingTime'] !='' and i == 0:
							i = 1
							mot = dateutil.parser.parse(index["openingTime"]).time()
							mct = dateutil.parser.parse(index["closingTime"]).time()
							if mot > mct or mot == mct:
								err_message["time"] = \
									"Please provide meaningfull opening & closing time for thursday!!" 
							else:
								pass
						if any(err_message.values())==True:
							thflag = 0
							return Response({
								"success": False,
								"error" : err_message,
								"message" : "Please correct listed errors!!"
								})	
						else:
							thflag = 1

				if "friday" in data and len(data['friday']) > 0:
					mdata = data['friday']
					i = 0
					for index in mdata:
						if index["openingTime"] == '':
							err_message["opentime"] = "Please Enter opening time for friday!!"
						if index["closingTime"] == '':
							err_message["closetime"] = "Please Enter closing time for friday!!"
						if index['openingTime'] != '' and index['closingTime'] !='' and i == 0:
							i = 1
							mot = dateutil.parser.parse(index["openingTime"]).time()
							mct = dateutil.parser.parse(index["closingTime"]).time()
							if mot > mct or mot == mct:
								err_message["time"] = \
									"Please provide meaningfull opening & closing time for friday!!" 
							else:
								pass
						if any(err_message.values())==True:
							fflag = 0
							return Response({
								"success": False,
								"error" : err_message,
								"message" : "Please correct listed errors!!"
								})	
						else:
							fflag = 1
				if "saturday" in data and len(data['saturday']) > 0:
					mdata = data['saturday']
					i = 0
					for index in mdata:
						if index["openingTime"] == '':
							err_message["opentime"] = "Please Enter opening time for saturday!!"
						if index["closingTime"] == '':
							err_message["closetime"] = "Please Enter closing time for saturday!!"
						if index['openingTime'] != '' and index['closingTime'] !='' and i == 0:
							i = 1
							mot = dateutil.parser.parse(index["openingTime"]).time()
							mct = dateutil.parser.parse(index["closingTime"]).time()
							if mot > mct or mot == mct:
								err_message["time"] = \
									"Please provide meaningfull opening & closing time for saturday!!" 
							else:
								pass
						if any(err_message.values())==True:
							sflag = 0
							return Response({
								"success": False,
								"error" : err_message,
								"message" : "Please correct listed errors!!"
								})	
						else:
							sflag = 1

				if "sunday" in data and len(data['sunday']) > 0:
					i = 0
					mdata = data['sunday']
					for index in mdata:
						if index["openingTime"] == '':
							err_message["opentime"] = "Please Enter opening time for sunday!!"
						if index["closingTime"] == '':
							err_message["closetime"] = "Please Enter closing time for sunday!!"
						if index['openingTime'] != '' and index['closingTime'] !='' and i == 0:
							i = 1
							mot = dateutil.parser.parse(index["openingTime"]).time()
							mct = dateutil.parser.parse(index["closingTime"]).time()
							if mot > mct or mot == mct:
								err_message["time"] = \
									"Please provide meaningfull opening & closing time for sunday!!" 
							else:
								pass
						if any(err_message.values())==True:
							suflag = 0
							return Response({
								"success": False,
								"error" : err_message,
								"message" : "Please correct listed errors!!"
								})	
						else:
							suflag = 1

				o_id = OutletProfile.objects.filter(id=data['id'])[0].id
				alldata = data
				del alldata['id'] 
				del alldata['gst'] 
				del alldata['tab'] 
				del alldata['header'] 
				del alldata['footer'] 
				del alldata['min_order_value']
				del alldata['average_delivery_time']
				del alldata['company_auth_id']
				del alldata['payment_method']
				del alldata['outlet_image']
				del alldata['map_locality']
				del alldata['time_range']
				del alldata['no_of_days']
				del alldata['Outletname']
				del alldata['longitude']
				del alldata['map_city']
				del alldata['location']
				del alldata['latitude']
				del alldata['country']
				del alldata['address']
				del alldata['prefecture']
				mdatas = OutletTimingMaster.objects.create(outlet_id=o_id,\
											allday=alldata,name="timing",Company_id=Company_id)
				if "monday" in data and len(data['monday']) > 0 and mflag == 1:
					mdata = data['monday']
					for index in mdata:
						mot = dateutil.parser.parse(index["openingTime"]).time()
						mct = dateutil.parser.parse(index["closingTime"]).time()
						tdata = OutletTiming.objects.create(day='Monday',outlet_id=o_id,opening_time=mot,\
							closing_time=mct,Company_id=Company_id,allday=alldata,masterid_id=mdatas.id)
						
				if "tuesday" in data and len(data['tuesday']) > 0 and tuflag == 1:
					mdata = data['tuesday']
					for index in mdata:
						mot = dateutil.parser.parse(index["openingTime"]).time()
						mct = dateutil.parser.parse(index["closingTime"]).time()
						tdata = OutletTiming.objects.create(day='Tuesday',outlet_id=o_id,opening_time=mot,\
							closing_time=mct,Company_id=Company_id,masterid_id=mdatas.id)

				if "wednesday" in data and len(data['wednesday']) > 0 and wflag == 1:
					mdata = data['wednesday']
					for index in mdata:
						mot = dateutil.parser.parse(index["openingTime"]).time()
						mct = dateutil.parser.parse(index["closingTime"]).time()
						tdata = OutletTiming.objects.create(day='Wednesday',outlet_id=o_id,opening_time=mot,\
							closing_time=mct,Company_id=Company_id,masterid_id=mdatas.id)

				if "thursday" in data and len(data['thursday']) > 0 and thflag == 1:
					mdata = data['thursday']
					for index in mdata:
						mot = dateutil.parser.parse(index["openingTime"]).time()
						mct = dateutil.parser.parse(index["closingTime"]).time()
						tdata = OutletTiming.objects.create(day='Thursday',outlet_id=o_id,opening_time=mot,\
							closing_time=mct,Company_id=Company_id,masterid_id=mdatas.id)

				if "friday" in data and len(data['friday']) > 0 and fflag == 1:
					mdata = data['friday']
					for index in mdata:
						mot = dateutil.parser.parse(index["openingTime"]).time()
						mct = dateutil.parser.parse(index["closingTime"]).time()
						tdata = OutletTiming.objects.create(day='Friday',outlet_id=o_id,opening_time=mot,\
							closing_time=mct,Company_id=Company_id,masterid_id=mdatas.id)

				if "saturday" in data and len(data['saturday']) > 0 and sflag == 1:
					mdata = data['saturday']
					for index in mdata:
						mot = dateutil.parser.parse(index["openingTime"]).time()
						mct = dateutil.parser.parse(index["closingTime"]).time()
						tdata = OutletTiming.objects.create(day='Saturday',outlet_id=o_id,opening_time=mot,\
							closing_time=mct,Company_id=Company_id,masterid_id=mdatas.id)

				if "sunday" in data and len(data['sunday']) > 0 and suflag == 1:
					mdata = data['sunday']
					for index in mdata:
						mot = dateutil.parser.parse(index["openingTime"]).time()
						mct = dateutil.parser.parse(index["closingTime"]).time()
						tdata = OutletTiming.objects.create(day='Sunday',outlet_id=o_id,opening_time=mot,\
							closing_time=mct,Company_id=Company_id,masterid_id=mdatas.id)			
				return Response({
					"success": True, 
					"message": "Time is saved",
					"outlet_id": o_id
					})
			if data['tab'] == str(3):
				pm = data['payment_method']
				if len(pm) > 0:
					pmethod = pm.split(',')
				else:
					pmethod =[]
				record = OutletProfile.objects.filter(id=data['id'])
				p_query = record.update(
				payment_method=pmethod
				)
				if p_query:
					return Response(
							{
					"success": True,
					"message": "Outlet is registered successfully under your brand!!",
					"outlet_id": data['id']
							}
							)
			else:
				pass

			if data['tab'] == str(4):
				data = request.data
				record = OutletProfile.objects.filter(id=data['id'])
				err_message = {}
				data1 = json.loads(data["delivery_zone"])
				if len(data1) > 0:
					for index in data1:
						if index['end'] == '' or index['end'] == None:
							err_message["end"] = 'Please choose End KM.!!'
						if len(index['price_type']) == 0:
							err_message["price_type"] = 'Please choose price type!!'
						if index['isTax'] == 1:
							if len(index['taxes']) == 0:
								err_message["price_type"] = 'Please choose applicable tax(es)!!'
					if any(err_message.values())==True:
						suflag = 0
						return Response({
							"success": False,
							"error" : err_message,
							"message" : "Please correct listed errors!!"
							})	
					record.update(delivery_zone=data1)
				return Response({
					"success" : True
					})

		except Exception as e:
			print("Outlet Creation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})




class OutletUpdation(APIView):
	"""
	Outlet Creation POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create new outlets within brand.

		Data Post: {
			

			"Outletname" 			: "Adarsh Nagar, Jalandhar",
			"company_auth_id" 	    : "3",
			"latitude"              : "31.32990749999999",
			"longitude"             : "75.56381729999998",
			"address"               : "Punjab 144002, India",
			"country"               : "1",
			"city"                  : "delhi",
			"location"              : 'hari nagar ashram'
			"outlet_image"          : "a.jpg",
			"min_order_value"       : "200",
			"average_delivery_time" : "1.15",
			"outlet_instagram"      : '',
			"map_city"              : [],
			"map_locality"          : [],
			"prefecture"					: "1",
			"no_of_days"            : "5",
			"time_range"            : "15"
		}

		Response: {

			"success": True,
			"message": "Outlet is registered successfully under your brand!!"
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			auth_id = request.user.id
			cid = get_user(auth_id)
			if 'sanitized_restaurant' in data:
				pass
			else:
				data['sanitized_restaurant'] = 0
			if 'temperature_check' in data:
				pass
			else:
				data['temperature_check'] = 0
			if 'clean_kitchen' in data:
				pass
			else:
				data['clean_kitchen'] = 0

			if data['tab'] == str(0):
				validation_check = err_checks(data)
				if validation_check != None:
					return Response(validation_check)
				company_query = Company.objects.filter(id=cid)
				if company_query.count() != 0:
					data["Company"] = company_query[0].id
				else:
					return Response(
						{
							"success": False,
							"message": "Company is not valid!!"
						}
						)
				data['min_value'] = data['min_order_value']
				record = OutletProfile.objects.filter(id=data['id'])
				p_query = \
					record.update(
					Outletname=data["Outletname"],\
					country_id=data["country"],\
					prefecture=data['prefecture'],\
					min_value=data['min_value'],\
					radius = data['radius'],
					city=data["city"],
					address=data["address"],
					ip_address=data["ip_address"],
					pincode=data["pincode"],\
					landmark=data['landmark'],
					sanitized_restaurant = data['sanitized_restaurant'],
					temperature_check = data['temperature_check'],
					clean_kitchen = data['clean_kitchen'],
					acceptance = data['acceptance'],
					processing = data['processing'],
					dispatch = data['dispatch']
					)
				if data["outlet_image"] != None and data["outlet_image"] != "":
					outlet = OutletProfile.objects.get(id=data["id"])
					outlet.outlet_image = data["outlet_image"]
					outlet.save()
				return Response(
							{
					"success": True,
					"message": "Outlet is updated successfully under your brand!!",
					"outlet_id": data['id']
							}
							)
			if data['tab'] == str(1):
				err_message = {}
				if data['average_delivery_time'] == '':
					date_time_str = '0:00'
					data['average_delivery_time'] = datetime.strptime(date_time_str, '%H:%M')
				else:
					pass
				record = OutletProfile.objects.filter(id=data['id'])
				p_query = record.update(
				# map_city=data["map_city"],
				# map_locality=data["map_locality"],\
				average_delivery_time=data['average_delivery_time']
				)
				if p_query:
					return Response(
							{
					"success": True,
					"message": "Outlet is registered successfully under your brand!!",
					"outlet_id": data['id']
							}
							)
			# if data['tab'] == str(2):
			# 	record = OutletProfile.objects.filter(id=data['id'])
			# 	p_query = record.update(
			# 	no_of_days=data["no_of_days"],
			# 	time_range=data["time_range"],\
			# 	)
			# 	if p_query:
			# 		return Response(
			# 				{
			# 		"success": True,
			# 		"message": "Outlet is registered successfully under your brand!!",
			# 		"outlet_id": data['id']
			# 				}
			# 				)
			# if data['tab'] == str(2):
			# 	unique_check = HeaderFooter.objects.filter(outlet_id=data["id"])
			# 	if unique_check.count() > 0:
			# 		data["updated_at"] = datetime.now()
			# 		p_query = \
			# 		unique_check.update(header_text=data["header"],\
			# 			footer_text=data["footer"],\
			# 			gst=data["gst"],\
			# 			updated_at=datetime.now())
			# 	else:
			# 		p_query = \
			# 		HeaderFooter.objects.create(outlet_id=data['id'],
			# 		header_text=data["header"],footer_text=data["footer"],\
			# 		gst=data["gst"],company_id=cid)
			# 	if p_query:
			# 		data_info=p_query
			# 		info_msg = "Receipt Configuration is created successfully!!"
			# 		return Response({
			# 			"success": True, 
			# 			"message": info_msg,
			# 			"outlet_id": data['id']
			# 			})
			if data['tab'] == str(2):
				auth_id = request.user.id
				Company_id = get_user(auth_id)
				err_message = {}
				mflag = 0
				tuflag = 0
				wflag = 0
				thflag = 0
				fflag = 0
				sflag = 0
				suflag = 0
				if data['id'] == None:
					err_message["outlet"] = "Please Select outlet!!"
				else:
					pass
				data1 = json.loads(data["monday"])
				data['monday'] = data1
				data2 = json.loads(data["tuesday"])
				data['tuesday'] = data2
				data3 = json.loads(data["wednesday"])
				data['wednesday'] = data3
				data4 = json.loads(data["thursday"])
				data['thursday'] = data4
				data5 = json.loads(data["friday"])
				data['friday'] = data5
				data6 = json.loads(data["saturday"])
				data['saturday'] = data6
				data7 = json.loads(data["sunday"])
				data['sunday'] = data7
				if len(data['monday']) == 0 and  len(data['tuesday']) == 0 and len(data['wednesday']) == 0 and \
						len(data['thursday']) == 0 and len(data['friday']) == 0 and len(data['saturday']) == 0 and \
						len(data['sunday']) == 0:
					err_message["fill"] = "Please Fill Enter time!!"
				if any(err_message.values())==True:
					return Response({
						"success": False,
						"error" : err_message,
						"message" : "Please correct listed errors!!"
						})
				if "monday" in data and len(data['monday']) > 0:
					mdata = data['monday']
					i = 0
					for index in mdata:
						if index["openingTime"] == '':
							err_message["opentime"] = "Please Enter opening time for monday!!"
						if index["closingTime"] == '':
							err_message["closetime"] = "Please Enter closing time for monday!!"
						if index['openingTime'] != '' and index['closingTime'] !='' and i == 0:
							i = 1
							mot = dateutil.parser.parse(index["openingTime"]).time()
							mct = dateutil.parser.parse(index["closingTime"]).time()
							if mot > mct or mot == mct:
								err_message["time"] = \
									"Please provide meaningfull opening & closing time for monday!!" 
							else:
								pass
						if any(err_message.values())==True:
							mflag = 0
							return Response({
								"success": False,
								"error" : err_message,
								"message" : "Please correct listed errors!!"
								})
						else:
							mflag = 1
				if "tuesday" in data and len(data['tuesday']) > 0:
					mdata = data['tuesday']
					i = 0
					for index in mdata:
						if index["openingTime"] == '':
							err_message["opentime"] = "Please Enter opening time for tuesday!!"
						if index["closingTime"] == '':
							err_message["closetime"] = "Please Enter closing time for tuesday!!"
						if index['openingTime'] != '' and index['closingTime'] !='' and i == 0:
							i = 1
							mot = dateutil.parser.parse(index["openingTime"]).time()
							mct = dateutil.parser.parse(index["closingTime"]).time()
							if mot > mct or mot == mct:
								err_message["time"] = \
									"Please provide meaningfull opening & closing time for tuesday!!" 
							else:
								pass
						if any(err_message.values())==True:
							tuflag = 0
							return Response({
								"success": False,
								"error" : err_message,
								"message" : "Please correct listed errors!!"
								})
						else:
							tuflag = 1
				if "wednesday" in data and len(data['wednesday']) > 0:
					mdata = data['wednesday']
					i = 0
					for index in mdata:
						if index["openingTime"] == '':
							err_message["opentime"] = "Please Enter opening time for wednesday!!"
						if index["closingTime"] == '':
							err_message["closetime"] = "Please Enter closing time for wednesday!!"
						if index['openingTime'] != '' and index['closingTime'] !='' and i == 0:
							i = 1
							mot = dateutil.parser.parse(index["openingTime"]).time()
							mct = dateutil.parser.parse(index["closingTime"]).time()
							if mot > mct or mot == mct:
								err_message["time"] = \
									"Please provide meaningfull opening & closing time for wednesday!!" 
							else:
								pass
						if any(err_message.values())==True:
							wflag = 0
							return Response({
								"success": False,
								"error" : err_message,
								"message" : "Please correct listed errors!!"
								})	
						else:
							wflag = 1	


				if "thursday" in data and len(data['thursday']) > 0:
					mdata = data['thursday']
					i = 0
					for index in mdata:
						if index["openingTime"] == '':
							err_message["opentime"] = "Please Enter opening time for thursday!!"
						if index["closingTime"] == '':
							err_message["closetime"] = "Please Enter closing time for thursday!!"
						if index['openingTime'] != '' and index['closingTime'] !='' and i == 0:
							i = 1
							mot = dateutil.parser.parse(index["openingTime"]).time()
							mct = dateutil.parser.parse(index["closingTime"]).time()
							if mot > mct or mot == mct:
								err_message["time"] = \
									"Please provide meaningfull opening & closing time for thursday!!" 
							else:
								pass
						if any(err_message.values())==True:
							thflag = 0
							return Response({
								"success": False,
								"error" : err_message,
								"message" : "Please correct listed errors!!"
								})	
						else:
							thflag = 1

				if "friday" in data and len(data['friday']) > 0:
					mdata = data['friday']
					i = 0
					for index in mdata:
						if index["openingTime"] == '':
							err_message["opentime"] = "Please Enter opening time for friday!!"
						if index["closingTime"] == '':
							err_message["closetime"] = "Please Enter closing time for friday!!"
						if index['openingTime'] != '' and index['closingTime'] !='' and i == 0:
							i = 1
							mot = dateutil.parser.parse(index["openingTime"]).time()
							mct = dateutil.parser.parse(index["closingTime"]).time()
							if mot > mct or mot == mct:
								err_message["time"] = \
									"Please provide meaningfull opening & closing time for friday!!" 
							else:
								pass
						if any(err_message.values())==True:
							fflag = 0
							return Response({
								"success": False,
								"error" : err_message,
								"message" : "Please correct listed errors!!"
								})	
						else:
							fflag = 1
				if "saturday" in data and len(data['saturday']) > 0:
					mdata = data['saturday']
					i = 0
					for index in mdata:
						if index["openingTime"] == '':
							err_message["opentime"] = "Please Enter opening time for saturday!!"
						if index["closingTime"] == '':
							err_message["closetime"] = "Please Enter closing time for saturday!!"
						if index['openingTime'] != '' and index['closingTime'] !='' and i == 0:
							i = 1
							mot = dateutil.parser.parse(index["openingTime"]).time()
							mct = dateutil.parser.parse(index["closingTime"]).time()
							if mot > mct or mot == mct:
								err_message["time"] = \
									"Please provide meaningfull opening & closing time for saturday!!" 
							else:
								pass
						if any(err_message.values())==True:
							sflag = 0
							return Response({
								"success": False,
								"error" : err_message,
								"message" : "Please correct listed errors!!"
								})	
						else:
							sflag = 1

				if "sunday" in data and len(data['sunday']) > 0:
					i = 0
					mdata = data['sunday']
					for index in mdata:
						if index["openingTime"] == '':
							err_message["opentime"] = "Please Enter opening time for sunday!!"
						if index["closingTime"] == '':
							err_message["closetime"] = "Please Enter closing time for sunday!!"
						if index['openingTime'] != '' and index['closingTime'] !='' and i == 0:
							i = 1
							mot = dateutil.parser.parse(index["openingTime"]).time()
							mct = dateutil.parser.parse(index["closingTime"]).time()
							if mot > mct or mot == mct:
								err_message["time"] = \
									"Please provide meaningfull opening & closing time for sunday!!" 
							else:
								pass
						if any(err_message.values())==True:
							suflag = 0
							return Response({
								"success": False,
								"error" : err_message,
								"message" : "Please correct listed errors!!"
								})	
						else:
							suflag = 1

				o_id = OutletProfile.objects.filter(id=str(data['id']))[0].id
				alldata = data


				del alldata['id'] 
				del alldata['gst'] 
				del alldata['tab'] 
				del alldata['header'] 
				del alldata['footer'] 
				del alldata['min_order_value']
				del alldata['average_delivery_time']
				del alldata['company_auth_id']
				del alldata['payment_method']
				del alldata['outlet_image']
				del alldata['map_locality']
				del alldata['time_range']
				del alldata['no_of_days']
				del alldata['map_city']
				del alldata['country']
				del alldata['prefecture']


				chk_d = OutletTimingMaster.objects.filter(outlet_id=str(o_id))
				if chk_d.count() > 0:
					md = chk_d.update(allday=alldata,name="timingdata")
					mdatas = OutletTimingMaster.objects.filter(outlet_id=o_id)[0]
				else:
					mdatas = OutletTimingMaster.objects.create(outlet_id=str(o_id),\
											allday=alldata,name="timing",Company_id=Company_id)[0]

				if "monday" in data and len(data['monday']) > 0 and mflag == 1:
					timingdata = OutletTiming.objects.filter(outlet_id=str(o_id),day='Monday')
					if timingdata.count() > 0:
						timingdata.delete()
						mdata = data['monday']
						for index in mdata:
							mot = dateutil.parser.parse(index["openingTime"]).time()
							mct = dateutil.parser.parse(index["closingTime"]).time()
							tdata = OutletTiming.objects.create(day='Monday',outlet_id=o_id,opening_time=mot,\
								closing_time=mct,Company_id=Company_id,allday=alldata,masterid_id=mdatas.id)
					else:
						mdata = data['monday']
						for index in mdata:
							mot = dateutil.parser.parse(index["openingTime"]).time()
							mct = dateutil.parser.parse(index["closingTime"]).time()
							tdata = OutletTiming.objects.create(day='Monday',outlet_id=o_id,opening_time=mot,\
								closing_time=mct,Company_id=Company_id,allday=alldata,masterid_id=mdatas.id)
				if "tuesday" in data and len(data['tuesday']) > 0 and tuflag == 1:
					timingdata = OutletTiming.objects.filter(outlet_id=o_id,day='Tuesday')
					if timingdata.count() > 0:
						timingdata.delete()
					else:
						pass
					mdata = data['tuesday']
					for index in mdata:
						mot = dateutil.parser.parse(index["openingTime"]).time()
						mct = dateutil.parser.parse(index["closingTime"]).time()
						tdata = OutletTiming.objects.create(day='Tuesday',outlet_id=o_id,opening_time=mot,\
							closing_time=mct,Company_id=Company_id,masterid_id=mdatas.id)
					

				if "wednesday" in data and len(data['wednesday']) > 0 and wflag == 1:
					timingdata = OutletTiming.objects.filter(outlet_id=o_id,day='Wednesday')
					if timingdata.count() > 0:
						timingdata.delete()
					else:
						pass
					mdata = data['wednesday']
					for index in mdata:
						mot = dateutil.parser.parse(index["openingTime"]).time()
						mct = dateutil.parser.parse(index["closingTime"]).time()
						tdata = OutletTiming.objects.create(day='Wednesday',outlet_id=o_id,opening_time=mot,\
							closing_time=mct,Company_id=Company_id,masterid_id=mdatas.id)

				if "thursday" in data and len(data['thursday']) > 0 and thflag == 1:
					timingdata = OutletTiming.objects.filter(outlet_id=o_id,day='Thursday')
					if timingdata.count() > 0:
						timingdata.delete()
					else:
						pass
					mdata = data['thursday']
					for index in mdata:
						mot = dateutil.parser.parse(index["openingTime"]).time()
						mct = dateutil.parser.parse(index["closingTime"]).time()
						tdata = OutletTiming.objects.create(day='Thursday',outlet_id=o_id,opening_time=mot,\
							closing_time=mct,Company_id=Company_id,masterid_id=mdatas.id)

				if "friday" in data and len(data['friday']) > 0 and fflag == 1:
					timingdata = OutletTiming.objects.filter(outlet_id=o_id,day='Friday')
					if timingdata.count() > 0:
						timingdata.delete()
					else:
						pass
					mdata = data['friday']
					for index in mdata:
						mot = dateutil.parser.parse(index["openingTime"]).time()
						mct = dateutil.parser.parse(index["closingTime"]).time()
						tdata = OutletTiming.objects.create(day='Friday',outlet_id=o_id,opening_time=mot,\
							closing_time=mct,Company_id=Company_id,masterid_id=mdatas.id)

				if "saturday" in data and len(data['saturday']) > 0 and sflag == 1:
					timingdata = OutletTiming.objects.filter(outlet_id=o_id,day='Saturday')
					if timingdata.count() > 0:
						timingdata.delete()
					else:
						pass
					mdata = data['saturday']
					for index in mdata:
						mot = dateutil.parser.parse(index["openingTime"]).time()
						mct = dateutil.parser.parse(index["closingTime"]).time()
						tdata = OutletTiming.objects.create(day='Saturday',outlet_id=o_id,opening_time=mot,\
							closing_time=mct,Company_id=Company_id,masterid_id=mdatas.id)

				if "sunday" in data and len(data['sunday']) > 0 and suflag == 1:
					timingdata = OutletTiming.objects.filter(outlet_id=o_id,day='Sunday')
					if timingdata.count() > 0:
						timingdata.delete()
					else:
						pass
					mdata = data['sunday']
					for index in mdata:
						mot = dateutil.parser.parse(index["openingTime"]).time()
						mct = dateutil.parser.parse(index["closingTime"]).time()
						tdata = OutletTiming.objects.create(day='Sunday',outlet_id=o_id,opening_time=mot,\
							closing_time=mct,Company_id=Company_id,masterid_id=mdatas.id)			
				return Response({
					"success": True, 
					"message": "Time is saved",
					"outlet_id": o_id
					})
			if data['tab'] == str(3):
				pm = data['payment_method']
				if len(pm) > 0:
					pmethod = pm.split(',')
				else:
					pmethod =[]
				record = OutletProfile.objects.filter(id=data['id'])
				p_query = record.update(
				payment_method=pmethod
				)
				if p_query:
					return Response(
							{
					"success": True,
					"message": "Outlet is registered successfully under your brand!!",
					"outlet_id": data['id']
							}
							)
			else:
				pass
			if data['tab'] == str(4):
				data = request.data
				record = OutletProfile.objects.filter(id=data['id'])
				err_message = {}
				data1 = json.loads(data["delivery_zone"])
				if len(data1) > 0:
					for index in data1:
						if index['end'] == '' or index['end'] == None:
							err_message["end"] = 'Please choose End KM.!!'
						if len(index['price_type']) == 0:
							err_message["price_type"] = 'Please choose price type!!'
						if index['isTax'] == 1:
							if len(index['taxes']) == 0:
								err_message["price_type"] = 'Please choose applicable tax(es)!!'
					if any(err_message.values())==True:
						suflag = 0
						return Response({
							"success": False,
							"error" : err_message,
							"message" : "Please correct listed errors!!"
							})	
					record.update(delivery_zone=data1)
				return Response({
					"success" : True
					})
		except Exception as e:
			print("Outlet Creation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})




class OutletAction(APIView):
	"""
	Outlet Action POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to activate or deactivate Outlet.

		Data Post: {
			"id"                   		: "2",
			"active_status"             : "0"
		}

		Response: {

			"success": True, 
			"message": "Outlet is deactivated now!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			from django.db.models import Q
			data = request.data
			err_message = {}
			if data["active_status"] == "true":
				pass
			elif data["active_status"] == "false":
				pass
			else:
				err_message["active_status"] = "Active status data is not valid!!"
			err_message["id"] = \
						validation_master_anything(data["id"],
						"Outlet",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = OutletProfile.objects.filter(id=data["id"])
			if record.count() != 0:
				data["updated_at"] = datetime.now()
				if data["active_status"] == "true":
					info_msg = "Outlet is activated successfully!!"
				else:
					info_msg = "Outlet is deactivated successfully!!"
				serializer = \
				OutletProfileSerializer(record[0],data=data,partial=True)
				if serializer.is_valid():
					data_info = serializer.save()
				else:
					print("something went wrong!!")
					return Response({
						"success": False, 
						"message": str(serializer.errors),
						})
			else:
				return Response(
					{
						"success": False,
						"message": "Outlet id is not valid to update!!"
					}
					)
			final_result = []
			final_result.append(serializer.data)
			return Response({
						"success": True, 
						"message": info_msg,
						"data": final_result,
						})
		except Exception as e:
			print("Outlet action Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})




class OutletListing(APIView):
	"""
	Outlet listing Configuration POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to provide all outlet details within brand.

		Data Post: {

			"company_auth_id" 	    : "3"
		}

		Response: {

			"success": true,
			"data": [
				{
					"id": 2,
					"auth_id": 7,
					"Outletname": "GTB Nagar, Jalandhar"
				},
				{
					"id": 1,
					"auth_id": 6,
					"Outletname": "Adarsh Nagar, Jalandhar"
				}
			],
			"message": "Outlet fetching successful!!"
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			user = request.user.id
			cid = get_user(user)
			query = OutletProfile.objects.filter(Q(is_company_active=1),Q(Company=cid),Q(is_hide=0))
			if query.count() > 0:
				oulet_conf_data_serializer = []
				for q in query:
					q_dict = {}
					q_dict["id"] = q.id
					q_dict["active_status"] = q.active_status
					q_dict["Outletname"] = q.Outletname
					q_dict["address"] = q.address
					q_dict["city"] = q.city
					q_dict["prefecture"] = q.prefecture
					q_dict["pincode"] = q.pincode
					q_dict["landmark"] = q.landmark
					q_dict["ip_address"] = q.ip_address
					domain_name = addr_set()
					out_img = str(q.outlet_image)
					if out_img != "" and out_img != None and out_img != "null":
						full_path = domain_name + str(q.outlet_image)
						q_dict['outlet_image'] = full_path
					else:
						q_dict['outlet_image'] = ''
					oulet_conf_data_serializer.append(q_dict)
				return Response(
						{
							"success": True,
							"data" : oulet_conf_data_serializer,
							"message": "Outlet fetching successful!!"
						}
						)
			else:
				return Response(
						{
							"success": True,
							"data" : [],
							"message": "Outlet fetching successful!!"
						}
						)

		except Exception as e:
			print("Outlet listing configuration Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})





class OutletRetrieval(APIView):
	"""
	Outlet retrieval POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of Outlet data.

		Data Post: {
			"id"                   : "60"
		}

		Response: {

			"success"  :  True, 
			"message"  : "Outlet retrieval api worked well!!",
			"data"     : final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			err_message = {}
			err_message["id"] = \
					validation_master_anything(str(data["id"]),
					"Outlet Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = OutletProfile.objects.filter(id=data['id'])
			if record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Provided Outlet data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				q_dict = {}
				q_dict["id"] = record[0].id
				q_dict["Outletname"] = record[0].Outletname
				q_dict["address"] = record[0].address
				q_dict["radius"] = record[0].radius
				q_dict["delivery_zone"] = record[0].delivery_zone
				q_dict["city"] = record[0].city
				q_dict["pincode"] = record[0].pincode
				q_dict['landmark'] = record[0].landmark
				q_dict["acceptance"] = record[0].acceptance
				q_dict["processing"] = record[0].processing
				q_dict['dispatch'] = record[0].dispatch
				q_dict['prefecture'] = record[0].prefecture
				q_dict['address'] = record[0].address
				q_dict["country"] = []
				if record[0].country_id != None:
					cou={}
					cou['value'] = record[0].country_id
					cou['label'] = CountryMaster.objects.filter(id=record[0].country_id)[0].country
					q_dict["country"].append(cou)
				else:
					pass
				# q_dict["location"] = record[0].location
				if record[0].min_value == 0 or record[0].min_value ==None:
					q_dict["min_order_value"] = ''
				else:
					q_dict["min_order_value"] = record[0].min_value
				q_dict["average_delivery_time"] = record[0].average_delivery_time
				q_dict["days"] = record[0].no_of_days
				q_dict["time_range"] = []
				if record[0].time_range  == None:
					pass
				else:
					dic = {}
					dic['label'] = record[0].time_range
					dic['value'] = record[0].time_range
					q_dict['time_range'].append(dic)
				adt = str(record[0].average_delivery_time)
				if adt == 'None':
					q_dict["hour"] = ''
					q_dict["min"] = ''
				else:
					q_dict["hour"] = adt.split(':')[0]
					q_dict["min"] = adt.split(':')[1]
				q_dict["city_detail"] = []
				cityDetail = record[0].map_city
				if cityDetail !=None:
					for index in cityDetail:
						cat_dict = {}
						cat_dict["label"] = CityMaster.objects.filter(id=index)[0].city
						cat_dict['value'] = int(index)
						q_dict["city_detail"].append(cat_dict)
				areaDetail = record[0].map_locality
				q_dict["area_detail"] = []
				if areaDetail !=None:
					for index in areaDetail:
						cat_dict = {}
						cat_dict["label"] = AreaMaster.objects.filter(id=index)[0].area
						cat_dict['value'] = int(index)
						q_dict["area_detail"].append(cat_dict)
				q_dict["outlet_image"] = record[0].outlet_image
				full_path = addr_set()
				if q_dict["outlet_image"] != None and q_dict["outlet_image"]!="":
					q_dict["outlet_image"] = full_path+str(q_dict["outlet_image"])
				else:
					q_dict["outlet_image"] = None
				
				q_dict["payment_method"] = record[0].payment_method
				record1 = HeaderFooter.objects.filter(outlet_id=data['id'])
				if record1.count() > 0:
					q_dict["header"] = record1[0].header_text
					q_dict["footer"] = record1[0].footer_text
					q_dict["gst"] = record1[0].gst
				else:
					q_dict["header"] = ''
					q_dict["footer"] = ''
					q_dict["gst"] = ''
				timdata = OutletTimingMaster.objects.filter(outlet_id=data['id'])
				if timdata.count() > 0:
					a = timdata[0].allday
					q_dict['outlet'] = a
				else:
					pass
				final_result.append(q_dict)
			if final_result:
				return Response({
							"success": True, 
							"message": "Outlet retrieval api worked well!!",
							"data": final_result,
							})
			else:
				return Response({
							"success": True, 
							"message": "No outlet data found!!"
							})
		except Exception as e:
			print("Outlet retrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})




class OutletHide(APIView):
	"""
	Outlet Hide POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to hide or shiw outlet.

		Data Post: {
			"id"                   		: "2",
			"is_hide"                   : "0"
		}

		Response: {

			"success": True, 

		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			from django.db.models import Q
			data = request.data
			err_message = {}
			if data["is_hide"] == "true":
				pass
			elif data["is_hide"] == "false":
				pass
			else:
				err_message["is_hide"] = "Hide status data is not valid!!"
			err_message["id"] = \
						validation_master_anything(data["id"],
						"Outlet Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = OutletProfile.objects.filter(id=data["id"])
			if record.count() != 0:
				data["updated_at"] = datetime.now()
				if data["is_hide"] == "true":
					info_msg = "This outlet is hide successfully!!"
				else:
					info_msg = "This outlet is show successfully!!"
				serializer = \
				OutletProfileSerializer(record[0],data=data,partial=True)
				if serializer.is_valid():
					data_info = serializer.save()
				else:
					print("something went wrong!!")
					return Response({
						"success": False, 
						"message": str(serializer.errors),
						})
			else:
				return Response(
					{
						"success": False,
						"message": "Outlet id is not valid to update!!"
					}
					)
			return Response({
						"success": True, 
						"message": info_msg
						})
		except Exception as e:
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})

class UrbanPiperOutletDetails(APIView):
	"""
	Outlet Urban Piper Details POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to show outlet details.

		Data : {
			outlet_id : 50
		}
		Response: {

			{
   "stores":[
      {
         "city":"Delhi",
         "name":"Klugs Dummy",
         "min_pickup_time":900,
         "min_delivery_time":1800,
         "contact_phone":"7838911591",
         "notification_phones":[
            "7838911591"
         ],
         "ref_id":"2",
         "min_order_value":120,
         "hide_from_ui":false,
         "address":"Siddhartha Basti, Pocket C, Hari Nagar Ashram, New Delhi, Delhi 110014()",
         "notification_emails":[
            "customersupport@klugs.in"
         ],
         "zip_codes":[
            
         ],
         "geo_longitude":"77.202010",
         "geo_latitude":"28.650660",
         "active":true,
         "ordering_enabled":true,
         "translations":[
            
         ],
         "excluded_platforms":[
            
         ],
         "included_platforms":[
            "swiggy",
            "zomato"
         ],
         "timings":[
            {
               "day":"monday",
               "slots":[
                  {
                     "start_time":"15:00:21",
                     "end_time":"15:00:22"
                  },
                  {
                     "start_time":"15:01:22",
                     "end_time":"22:30:22"
                  }
               ]
            },
            {
               "day":"tuesday",
               "slots":[
                  {
                     "start_time":"15:00:21",
                     "end_time":"15:00:22"
                  },
                  {
                     "start_time":"15:01:22",
                     "end_time":"22:30:22"
                  }
               ]
            },
            {
               "day":"wednesday",
               "slots":[
                  {
                     "start_time":"15:00:21",
                     "end_time":"15:00:22"
                  },
                  {
                     "start_time":"15:01:22",
                     "end_time":"22:30:22"
                  }
               ]
            },
            {
               "day":"thursday",
               "slots":[
                  {
                     "start_time":"15:00:21",
                     "end_time":"15:00:22"
                  },
                  {
                     "start_time":"15:01:22",
                     "end_time":"22:30:22"
                  }
               ]
            },
            {
               "day":"friday",
               "slots":[
                  {
                     "start_time":"15:00:21",
                     "end_time":"15:00:22"
                  },
                  {
                     "start_time":"15:01:22",
                     "end_time":"22:30:22"
                  }
               ]
            },
            {
               "day":"saturday",
               "slots":[
                  {
                     "start_time":"15:00:21",
                     "end_time":"15:00:22"
                  },
                  {
                     "start_time":"15:01:22",
                     "end_time":"22:30:22"
                  }
               ]
            }
         ]
      }
   ]
}

		}
	"""

	def get(self, request):
		try:
			data = request.data
			record = OutletProfile.objects.filter(id=data['outlet_id'])
			final = {}
			stores = []
			notification_phones = []
			notification_emails = []
			slots = []
			times = {}
			day = {}
			timings = []
			st = {}
			st["city"] = record[0].city
			st["name"] = record[0].Outletname
			st["min_pickup_time"] = record[0].min_picking_time
			st["min_delivery_time"] = record[0].min_delivery_time
			st["contact_phone"] = record[0].outlet_phone
			notification_phones.append(record[0].outlet_phone)
			st["notification_phone"] = notification_phones
			st["min_order_value"] = record[0].min_value
			st["address"] = record[0].address
			st["ref_id"] = record[0].id
			st["hide_from_ui"] = False
			notification_emails.append(record[0].outlet_email)
			st["notification_emails"] = notification_emails
			st["zip_codes"]  = []
			st["geo_latitude"] = record[0].latitude
			st["geo_longitude"] = record[0].longitude
			st["active_status"] = record[0].active_status
			st["translations"] = []
			st["excluded_platforms"] = []
			st["included_platforms"] = ["swiggy","zomato"]
			timdata = OutletTimingMaster.objects.filter(outlet_id=data['outlet_id'])
			if timdata.count() > 0:
				a = timdata[0].allday
				if a["monday"]:
					day["day"] = "monday"
					times["start_time"] = a["monday"][0]["openingTime"]
					times["end_time"] = a["monday"][0]["closingTime"]
					slots.append(times)
					day["slots"] = slots
					timings.append(day)
					times = {}
					slots = []
					day = {}
				else:
					pass
				if a["tuesday"]:
					day["day"] = "tuesday"
					times["start_time"] = a["tuesday"][0]["openingTime"]
					times["end_time"] = a["tuesday"][0]["closingTime"]
					slots.append(times)
					day["slots"] = slots
					timings.append(day)
					times = {}
					slots = []
					day = {}
				else:
					pass
				if a["wednesday"]:
					day["day"] = "wednesday"
					times["start_time"] = a["wednesday"][0]["openingTime"]
					times["end_time"] = a["wednesday"][0]["closingTime"]
					slots.append(times)
					day["slots"] = slots
					timings.append(day)
					times = {}
					slots = []
					day = {}
				else:
					pass
				if a["thursday"]:
					day["day"] = "thursday"
					times["start_time"] = a["thursday"][0]["openingTime"]
					times["end_time"] = a["thursday"][0]["closingTime"]
					slots.append(times)
					day["slots"] = slots
					timings.append(day)
					times = {}
					slots = []
					day = {}
				else:
					pass
				if a["friday"]:
					day["day"] = "friday"
					times["start_time"] = a["friday"][0]["openingTime"]
					times["end_time"] = a["friday"][0]["closingTime"]
					slots.append(times)
					day["slots"] = slots
					timings.append(day)
					times = {}
					slots = []
					day = {}
				else:
					pass
				if a["saturday"]:
					day["day"] = "saturday"
					times["start_time"] = a["saturday"][0]["openingTime"]
					times["end_time"] = a["saturday"][0]["closingTime"]
					slots.append(times)
					day["slots"] = slots
					timings.append(day)
					times = {}
					slots = []
					day = {}
				else:
					pass
				if a["sunday"]:
					day["day"] = "sunday"
					times["start_time"] = a["sunday"][0]["openingTime"]
					times["end_time"] = a["sunday"][0]["closingTime"]
					slots.append(times)
					day["slots"] = slots
					timings.append(day)
					times = {}
					slots = []
					day = {}
				else:
					pass
				st["timings"] = timings
			else:
				pass
			stores.append(st)
			final["stores"] = stores
			return Response(
				final,status = HTTP_200_OK
			)
		except Exception as e:
			return Response(
				{"success": False, "message": str(e)}, status=HTTP_406_NOT_ACCEPTABLE
			)