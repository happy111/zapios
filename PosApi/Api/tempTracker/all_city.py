import re
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
from Outlet.models import TempTracking, OutletProfile
from UserRole.models import ManagerProfile
from datetime import datetime, timedelta
from .latest_temp import secret_token 
from Brands.models import Company
from Product.models import FoodType
from Location.models import CityMaster,AreaMaster
from Outlet.models import OutletProfile

class AllCity(APIView):
	"""
	All City data get API

		Authentication Required		 	: 		Yes
		Service Usage & Description	 	: 		This Api is used to provide All city.

		Data Get: {
		}

		Response: {

			"success"	: 	True,
			"data"		:	result, 

		}

	"""
	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			final_result = []
			p_list={}
			cid = ManagerProfile.objects.filter(auth_user_id=request.user.id)[0].Company_id
			allcity = CityMaster.objects.filter(active_status=1,company_id=cid)
			p_list['all_city'] = []
			outlet_data = ManagerProfile.objects.filter(auth_user_id=request.user.id)[0].outlet
			if allcity.count() > 0:
				for j in allcity:
					city_dict = {}
					city_dict['id'] = j.id
					city_dict['city'] = j.city
					p_list['all_city'].append(city_dict)
			else:
				pass
			p_list['all_locality'] = []
			allcity = CityMaster.objects.filter(active_status=1,company_id=cid)
			if allcity.count() > 0:
				for j in allcity:
					allarea = AreaMaster.objects.filter(active_status=1,city_id=j.id)
					if allarea.count() > 0:
						for k in allarea:
							area_dict = {}
							area_dict['id'] = k.id
							area_dict['city'] = j.id
							area_dict['area'] = k.area
							area_dict['outlets'] = []
							outlet = OutletProfile.objects.filter(map_locality__icontains=k.id)
							if outlet.count() > 0:
								for index in outlet:
									if str(index.id) in outlet_data:
										di = {}
										di['id'] = index.id
										di['name'] = index.Outletname
										area_dict['outlets'].append(di)
									else:
										pass
							else:
								pass
							p_list['all_locality'].append(area_dict)

					else:
						pass
			else:
				pass
			final_result.append(p_list)
			return Response({
				"success"	: 	True, 
				"data"  	: 	final_result
				})
		except Exception as e:
			return Response({
				"success"	: 	False, 
				"message"	: 	"Error happened!!", 
				"errors"	: 	str(e)
				})



			



