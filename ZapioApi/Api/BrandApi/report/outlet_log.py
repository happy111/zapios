from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from ZapioApi.Api.BrandApi.profile.profile import CompanySerializer
from Brands.models import Company
import json
from rest_framework import serializers

from rest_framework.authtoken.models import Token
from Outlet.models import DeliveryBoy,OutletProfile
from django.db.models import Q
from datetime import datetime, timedelta
from ZapioApi.Api.paginate import pagination
import math  
from UserRole.models import ManagerProfile
import dateutil.parser
from django.db.models import Count, Sum, Max, Avg, Case, When, Value, IntegerField, BooleanField
from ZapioApi.api_packages import *
from History.models import OutletLogs


class AllLog(APIView):
	"""
	Outlet Open / Close log listing and searching  POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for Order listng and searcin of Brand.

		Data Post: {
			"start_date"            : "2019-07-24 00:00:00:00",
			"end_date"              : "2019-07-29 00:00:00:00"  
			"outlet_id"             : []                    
		}

		Response: {

			"success": True, 
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			err_message = {}

			if data['start_date'] == 'Invalid date' or data['end_date'] == 'Invalid date':
				err_message["Invalid_date"] = "Please enter valid date!!"

			if data['start_date'] == None or data['end_date'] == None:
				err_message["Invalid_date"] = "Please enter valid date!!"

			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})

			if data["start_date"] != '' and data["end_date"] != '':
				start_date = dateutil.parser.parse(data["start_date"])
				end_date = dateutil.parser.parse(data["end_date"])
				if start_date > end_date:
					err_message["from_till"] = "Validity dates are not valid!!"
			else:
				pass
			if len(data["outlet_id"]) > 0:
				outlet_unique_list = []
				for i in data["outlet_id"]:
					err_message["outlet_map"] = validation_master_anything(str(i),
												"Outlet",contact_re, 1)
					if err_message["outlet_map"] != None:
						break
					if i not in outlet_unique_list:
						outlet_unique_list.append(i)
					else:
						err_message["duplicate_outlet"] = "Outlet are duplicate!!"
						break
					record_check = OutletProfile.objects.filter(Q(id=i))
					if record_check.count() == 0:
						err_message["outlet_map"] = "Outlet is not valid!!"
						break
					else:
						pass
			else:
				err_message["outlet_map"] = "Please Enter Outlet!!"
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
				
			user = request.user.id
			is_outlet = OutletProfile.objects.filter(auth_user_id=user)
			is_brand = Company.objects.filter(auth_user_id=user)
			is_cashier = ManagerProfile.objects.filter(auth_user_id=user)
			if is_cashier.count() > 0:
				cid = ManagerProfile.objects.filter(auth_user_id=user)[0].Company_id
			else:
				pass
			if is_outlet.count() > 0:
				outlet = OutletProfile.objects.filter(auth_user_id=user)
				cid = outlet[0].Company_id
			else:
				pass
			if is_brand.count() > 0:
				outlet = Company.objects.filter(auth_user_id=user)
				cid = outlet[0].id
			else:
				pass
			outlet = data['outlet_id']
			if data["start_date"] != '' and data["end_date"] != '':
				e = end_date
				s = start_date
				query = OutletLogs.objects.filter(Q(created_at__lte=e),Q(created_at__gte=s),\
					   Q(Company=cid))
			else:
				pass
			q_count = query.count()
			if q_count > 0:
				ord_data =[] 	
				for k in outlet:
					logdata = query.filter(outlet_id=k)
					for i in logdata:
						p_list ={}
						if i.opening_time !=None:
							o_time = i.opening_time+timedelta(hours=5,minutes=30)
							ot = str(o_time.time())
							s = ot.split('.')
							p_list['opening_time'] = s[0]
						else:
							p_list['opening_time'] = ''
						if i.closing_time !=None:
							o_time = i.closing_time+timedelta(hours=5,minutes=30)
							ot = str(o_time.time())
							s = ot.split('.')
							p_list['closing_time'] = s[0]
						else:
							p_list['closing_time'] = ''
						if i.created_at !=None:
							c_time = i.created_at+timedelta(hours=5,minutes=30)
							p_list['created_at'] = c_time.strftime("%Y-%m-%d")
						else:
							p_list['created_at'] = ''
						p_list['outlet'] = i.outlet.Outletname
						cid = ManagerProfile.objects.filter(auth_user_id=i.auth_user)
						p_list['user'] = cid[0].username
						ord_data.append(p_list)
				return Response({"status":True,
							     "logdata":ord_data,
							})
			else:
				return Response({"status":True,
							    "logdata":[],
							    "page_count" : []})
		except Exception as e:
			print(e)
			return Response(
						{"error":str(e)}
						)





