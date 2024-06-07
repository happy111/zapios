from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_201_CREATED, \
	HTTP_406_NOT_ACCEPTABLE, HTTP_200_OK, HTTP_503_SERVICE_UNAVAILABLE
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.sites.shortcuts import get_current_site
from ZapioApi.Api.BrandApi.profile.profile import CompanySerializer
import json
#Serializer for api
from rest_framework import serializers

from Orders.models import Order
from rest_framework.authtoken.models import Token
from Outlet.models import DeliveryBoy,OutletProfile
from django.db.models import Q
from datetime import datetime, timedelta


class OutletSerializer(serializers.ModelSerializer):
	class Meta:
		model = OutletProfile
		fields = '__all__'

class outletOnOff(APIView):
	"""
	Outlet On / Off  POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to open / close outlet

		Data Post: {
			"is_open"  : True
		}

		Response: {

			"success": True, 
			"message": "Outlet is open for now!!",

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
			if data["is_open"] == True:
				pass
			elif data["is_open"] == False:
				pass
			else:
				err_message["active_status"] = "Active status data is not valid!!"
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			user = request.user.id
			outlet_record = OutletProfile.objects.filter(auth_user=user)
			if outlet_record.count() != 0:
				data["updated_at"] = datetime.now()
				if data["is_open"] == True:
					info_msg = "Outlet is open for now!!"
				else:
					info_msg = "Outlet is closed for now!!"
				serializer = \
				OutletSerializer(outlet_record[0],data=data,partial=True)
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


class Outlet_Is_open(APIView):
	"""
	Outlet Open status GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to get outlet open status!!

	"""
	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			user = request.user.id
			outlet_record = OutletProfile.objects.filter(auth_user=user)
			is_open = outlet_record[0].is_open
			return Response({
							"success": True, 
							"is_open": is_open,
							})
		except Exception as e:
			print("Outlet Open status Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})


