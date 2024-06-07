import re
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
from datetime import datetime
from ZapioApi.Api.BrandApi.listing.listing import addr_set
from rest_framework import serializers
from urbanpiper.models import *
from django.db.models import Q
from Configuration.models import TaxSetting,Tax
from Configuration.models import *
from Location.models import *
from Outlet.models import OutletTiming,OutletProfile,OutletTimingMaster

class OutletSerializer(serializers.ModelSerializer):
	class Meta:
		model = OutletProfile
		fields = '__all__'


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
				q_dict["latitude"] = record[0].latitude
				q_dict["radius"] = record[0].radius
				q_dict["longitude"] = record[0].longitude
				q_dict["delivery_zone"] = record[0].delivery_zone
				q_dict["city"] = record[0].city
				q_dict["pincode"] = record[0].pincode
				q_dict['landmark'] = record[0].landmark
				q_dict["country"] = []
				if record[0].country_id != None:
					cou={}
					cou['value'] = record[0].country_id
					cou['label'] = CountryMaster.objects.filter(id=record[0].country_id)[0].country
					q_dict["country"].append(cou)
				else:
					pass
				q_dict["state"] = []
				if record[0].state_id != None:
					st={}
					st['value'] = record[0].state_id
					st['label'] = StateMaster.objects.filter(id=record[0].state_id)[0].state
					q_dict["state"].append(st)
				else:
					pass
				q_dict["location"] = record[0].location
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


