from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
#Serializer for api
from rest_framework import serializers
from django.db.models import Q
from datetime import datetime, timedelta
from urbanpiper.models import OutletSync
from Outlet.models import OutletProfile
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user



class UrbanOutletAttach(APIView):
	"""
	Outlet attach with urbanpiper GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for attaching outlets with urbanpiper within brand.
	"""
	permission_classes = (IsAuthenticated,)
	def get(self, request):
		try:
			auth_id = request.user.id
			Company_id = get_user(auth_id)
			record = OutletProfile.objects.filter(Company=Company_id,active_status=1)
			result =[]
			sync_count = 0
			if record.count() != 0:
				for i in record:
					q = OutletSync.objects.filter(outlet=i.id)
					if q.count() == 0:
						sync = OutletSync.objects.create(outlet_id=i.id,company=i.Company)
						sync_count = sync_count+1
					else:
						pass
			else:
				pass
			if sync_count == 0:
				msg = "Outlets are already attached!!"
			else:
				msg = "Total "+str(sync_count)+" outlets are attached successfully!!"
			return Response({"status": True,
							"message" : msg})
		except Exception as e:
			print(e)
			return Response(
						{"error":str(e)}
						)


