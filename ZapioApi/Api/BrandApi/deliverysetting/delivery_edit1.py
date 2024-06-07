from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime
from rest_framework import serializers
from Configuration.models import DeliverySetting
from ZapioApi.Api.BrandApi.deliverysetting.serializer import DeliverySerializer
from django.db.models import Q
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user

class DeliveryEdit(APIView):

	"""
	Delivery & Packaging Configuration Edit POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to edit the delivery & packaging Configuration details.

		Data Post: {
		    "delivery_charge"                : "#ffd600",
    		"package_charge"                   : "#000",
    		"tax_percent"                : "#ffd600",
    		"CGST"                   : "#000",
  			"id"                          : "1"
		}

		Response: {

			"success"  : True, 
			"message"  : "Theme api worked well!!",
			"data"     : final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			from Brands.models import Company
			data = request.data
			user = request.user
			auth_id = user.id
			Company_id = get_user(auth_id)
			if data['tab'] == str(0):
				err_message = {}
				if data['price_type'] == 'undefined':
					err_message["price_type"] = 'Please choose price type!!'
				if data['is_tax'] == 'true':
					if len(data['tax']) == 2:
						err_message["tax"] = 'Please choose tax!!'
				if any(err_message.values())==True:
					return Response({
						"success": False,
						"error" : err_message,
						"message" : "Please correct listed errors!!"
						})
				data['tax'] = data['tax']
				data['price_type'] = data['price_type']
				data["delivery_charge"] = float(data["delivery_charge"])
				data["package_charge"] = float(data["package_charge"])
				data["is_tax"] = data["is_tax"]
				record = DeliverySetting.objects.filter(Q(id=data['id']),Q(company=Company_id))
				if record.count() == 0:
					return Response(
						{
							"status": False,
		 					"message": "Delivery Charge Configuration data is not valid to update!!"
						})
				else:
					data["updated_at"] = datetime.now()
					theme_serializer = \
						DeliverySerializer(record[0],data=data,partial=True)
					if theme_serializer.is_valid():
						data_info = theme_serializer.save()
						return Response({
							"status": True, 
							"message": "Delivery & Taxes Configuration is updated successfully!!",
							"data": theme_serializer.data
							})
					else:
						print("something went wrong!!",theme_serializer.errors)
						return Response({
							"status": False, 
							"message": str(theme_serializer.errors),
							})
			if data['tab'] == str(1):
				record = PaymentDetails.objects.filter(id=data['id'])
				if record.count() == 0:
					return Response(
						{
							"status": False,
		 					"message": "Payment Configuration data is not valid to update!!"
						})
				else:
					data["updated_at"] = datetime.now()
					payment_serializer = \
						PaymentSerializer(record[0],data=data,partial=True)
					if payment_serializer.is_valid():
						data_info = payment_serializer.save()
						return Response({
							"status": True, 
							"message": "Payment credentials are updated successfully!!",
							"data": payment_serializer.data
							})
					else:
						print("something went wrong!!")
						return Response({
							"status": False, 
							"message": str(payment_serializer.errors),
							})
			if data['tab'] == str(2):
				err_message = {}
				err_message["u_id"] =  only_required(data["u_id"],"User Id")
				err_message["analytics_snippets"] =  \
				only_required(data["analytics_snippets"],"Analytics Snippet")
				err_message["id"] = validation_master_anything(str(data["id"]),
									"Id",contact_re, 1)
				if any(err_message.values())==True:
					return Response({
						"success": False,
						"error" : err_message,
						"message" : "Please correct listed errors!!"
						})
				record = AnalyticsSetting.objects.filter(Q(id=data['id']),Q(company=Company_id))
				if record.count() == 0:
					return Response(
						{
							"status": False,
		 					"message": "Analytics Configuration data is not valid to update!!"
						})
				else:
					data["updated_at"] = datetime.now()
					serializer = \
						AnalyticsSerializer(record[0],data=data,partial=True)
					if serializer.is_valid():
						data_info = serializer.save()
						return Response({
							"status": True, 
							"message": "Google Analytics Configuration is updated successfully!!",
							"data": serializer.data
							})
					else:
						print("something went wrong!!")
						return Response({
							"status": False, 
							"message": str(serializer.errors),
							})

		except Exception as e:
			print("Delivery Configuration retrieval Api Stucked into exception!!")
			print(e)
			return Response({
							"status": False, 
							"message": "Error happened!!", 
							"errors": str(e)})