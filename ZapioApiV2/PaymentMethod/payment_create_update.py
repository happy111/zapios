from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime
import os
from django.db.models import Q
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user
from rest_framework import serializers
from Configuration.models import PaymentMethod,OrderSource


class PaymentSerializer(serializers.ModelSerializer):
	class Meta:
		model = PaymentMethod
		fields = '__all__'


class PaymentCreate(APIView):
	"""
	Payment Method Creation & Updation POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create & update payment method.

		Data Post: {
			"id"                   : "1"(Send this key in update record case,else it is not required!!)
			"country"		       : "1",
			"symbole"              : "INR"
			"payment_logo"	       : "paytm.jpg"(type:image),
			"payment_method"	   : "paytm",
			"keyid"				   : "sdfsdsadas",
			"keySecret"			   : "adasdas"
		}

		Response: {

			"success": True, 
			"message": "Payment Method creation/updation api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			auth_id = request.user.id
			cid = get_user(auth_id)
			data['company'] = cid
			err_message = {}
			err_message["country"] = \
					validation_master_anything(data["country"],
					"Country Id",contact_re, 1)
		
			err_message["payment_method"] = validation_master_anything(data["payment_method"],\
											"Payment Method", username_re, 3)
	
			if type(data["payment_logo"]) != str:
				im_name_path =  data["payment_logo"].file.name
				im_size = os.stat(im_name_path).st_size
				if im_size > 1000*1024:
					err_message["image_size"] = "Payment method logo can'nt excced the size more than 1000kb!!"
			else:
				data["payment_logo"] = None
			if "id" in data:
				unique_check = PaymentMethod.objects.filter(~Q(id=data["id"]),\
								Q(payment_method__iexact=data["payment_method"]),Q(company_id=cid))
			else:
				unique_check = PaymentMethod.objects.filter(Q(payment_method__iexact=data["payment_method"])\
					,Q(company_id=cid))
			if unique_check.count() != 0:
				err_message["unique_check"] = "Payment Method with this name already exists!!"
			else:
				pass
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			data["active_status"] = 1
			if "id" in data:
				payment_record = PaymentMethod.objects.filter(id=data['id'])
				if payment_record.count() == 0:
					return Response(
					{
						"success": False,
	 					"message": "Payment Method data is not valid to update!!"
					}
					)
				else:
					if data["payment_logo"] == None:
						data["payment_logo"] = payment_record[0].payment_logo
					else:
						pass
					data["updated_at"] = datetime.now()
					Payment_serializer = \
					PaymentSerializer(payment_record[0],data=data,partial=True)
					if Payment_serializer.is_valid():
						data_info = Payment_serializer.save()
					else:
						print("something went wrong!!")
						return Response({
							"success": False, 
							"message": str(Payment_serializer.errors),
							})
			else:
				Payment_serializer = PaymentSerializer(data=data)
				if Payment_serializer.is_valid():
					data_info = Payment_serializer.save()
				else:
					print("omething went wrong!!",Payment_serializer.errors)
					return Response({
						"success": False, 
						"message": str(Payment_serializer.errors),
						})
			final_result = []
			final_result.append(Payment_serializer.data)
			return Response({
						"success": True, 
						"message": "Payment method creation/updation api worked well!!",
						"data": final_result,
						})
		except Exception as e:
			print("Payment method creation/updation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})