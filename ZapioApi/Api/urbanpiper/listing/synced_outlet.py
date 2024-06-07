from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Brands.models import Company
#Serializer for api
from rest_framework import serializers
from django.db.models import Q
from datetime import datetime, timedelta
from urbanpiper.models import OutletSync, ActionSync
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user


class SyncedOutletListing(APIView):
	"""
	Synce Outlet listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for providing Synced outlets with urbanpiper within brand.
	"""
	permission_classes = (IsAuthenticated,)
	def get(self, request):
		try:
			user = request.user.id
			Company_id = get_user(user)
			record = \
			OutletSync.objects.filter(company=Company_id,sync_status='synced',
								outlet__active_status=1).order_by('-created_at')
			result =[]
			if record.count() != 0:
				for i in record:
					record_dict ={}
					record_dict['id'] = i.outlet_id
					record_dict["outlet_name"] = i.outlet.Outletname
					result.append(record_dict)
			else:
				pass
			return Response({"status":True,
							"data":result})
		except Exception as e:
			print(e)
			return Response(
						{"error":str(e)}
						)
