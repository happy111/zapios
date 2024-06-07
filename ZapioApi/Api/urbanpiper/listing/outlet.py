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



class UrbanOutletListing(APIView):
	"""
	Outlet listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for providing attached outlets with urbanpiper within brand.
	"""
	permission_classes = (IsAuthenticated,)
	def get(self, request):
		try:
			user = request.user.id
			Company_id = get_user(user)
			record = OutletSync.objects.filter(company=Company_id).order_by('-created_at')
			result =[]
			if record.count() != 0:
				for i in record:
					record_dict ={}
					record_dict['id'] = i.id
					record_dict['is_synced'] = i.is_synced
					record_dict['action_at'] = i.action_at
					if record_dict['action_at'] != None:
						a_time = i.action_at+timedelta(hours=5,minutes=30)
						record_dict['action_at'] = a_time.strftime("%d %b %y %I:%M %p")
					else:
						record_dict['action_at'] = None
					record_dict['attached_at'] = \
					(i.created_at + timedelta(hours=5,minutes=30)).strftime("%d %b %y %I:%M %p")
					record_dict["outlet_name"] = i.outlet.Outletname
					record_dict["sync_status"] = i.get_sync_status_display()
					record_dict["urbanpiper_store_id"] = i.urbanpiper_store_id
					ActionSync_record = ActionSync.objects.filter(sync_outlet=i.id)
					if ActionSync_record.count() == 0:
						record_dict["store_status"] = False
					else:
						record_dict["store_status"] = ActionSync_record[0].is_enabled
					if i.sync_status == "not_intiated":
						color = "danger"
					elif i.sync_status == "in_progress":
						color = "warning"
					else:
						color = "success"
					record_dict["color_code"] = color
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



class UnInitiatedOutletListing(APIView):
	"""
	Not Initiated Outlet listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for providing active and attached outlets with urbanpiper within brand.
	"""
	permission_classes = (IsAuthenticated,)
	def get(self, request):
		try:
			user = request.user.id
			record = \
			OutletSync.objects.filter(company__auth_user=user,sync_status='not_intiated',
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


