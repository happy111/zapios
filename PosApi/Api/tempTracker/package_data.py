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
from Configuration.models import *

class PackageCharge(APIView):
	"""
	Packing_charge Information data get API

		Authentication Required		 	: 		Yes
		Service Usage & Description	 	: 		This Api is used to provide Packing Charge.

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
			cid = ManagerProfile.objects.filter(auth_user_id=request.user.id)[0].Company_id
			pdata = DeliverySetting.objects.filter(company_id=cid)
			if pdata.count() > 0:
				dic = {}
				dic['price_type'] = pdata[0].price_type
				dic['is_tax'] = pdata[0].is_tax
				if dic['is_tax'] == 1:
					t = pdata[0].tax
					if t != None:
						if len(t) > 0:
							dic['tax'] = []
							for i in t:
								d = {}
								ta = Tax.objects.filter(id=str(i))
								if ta.count() > 0:
									d['tax_name'] = ta[0].tax_name
									d['percentage'] = ta[0].tax_percent
									dic['tax'].append(d)
						else:
							pass
					else:
						pass
				else:
					pass
				dic['delivery_charge'] = pdata[0].delivery_charge
				dic['packing_charge'] = pdata[0].package_charge
				final_result.append(dic)
			else:
				pass
			return Response({
				"success"	: 	True, 
				"data"	: 	final_result
				})
						 
		except Exception as e:
			return Response({
				"success"	: 	False, 
				"message"	: 	"Error happened!!", 
				"errors"	: 	str(e)
				})



			



