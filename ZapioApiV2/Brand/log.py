from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.Api.BrandApi.Validation.outlet_error_check import *
from _thread import start_new_thread
from django.db.models import Avg, Max, Min, Sum
#Serializer for api
from rest_framework import serializers
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user
from Brands.models import Company
from UserRole.models import *
from django.db.models import Q
from History.models import Logs
from Event.models import PrimaryEventType

class LogSerializer(serializers.ModelSerializer):
	class Meta:
		model = Logs
		fields = '__all__'

class BrandLog(APIView):
	"""
	Brand Creation POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create new brand.

		Data Post: {
			
			"event_name"  : "kot/bill"
			"order_id"    : "32432432432432"
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
			postdata = {}
			user = request.user.id
			cid = get_user(user)
			if data['event_name'] == "kot":
				postdata['event_name'] = "Kot Printing"
				postdata['trigger']  = PrimaryEventType.objects.filter(event_type='Kot Printing')[0].id

			else:
				postdata['event_name'] = "Bill Printing"
				postdata['trigger']  = PrimaryEventType.objects.filter(event_type='Bill Printing')[0].id

			postdata['order_id'] = data['order_id']
			postdata['auth_user']  = user
			postdata['Company']  = cid
			postdata['event_by'] = ManagerProfile.objects.filter(auth_user_id=user)[0].username
			postdata['count']  = 1
			log_serializer = LogSerializer(data=postdata)
			if log_serializer.is_valid():
				data_info = log_serializer.save()
				return Response({
					"success": True, 
					"message": "Log stored",
					})

			else:
				print("something went wrong!!",log_serializer.errors)
				return Response({
					"success": False, 
					"message": str(log_serializer.errors),
					})
		except Exception as e:
			print("Brand Creation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})