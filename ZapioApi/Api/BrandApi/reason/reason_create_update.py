from rest_framework.views import APIView
from rest_framework.response import Response
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime
import os
from django.db.models import Q
from discount.models import DiscountReason
from ZapioApi.Api.BrandApi.reason.serializer import ReasonSerializer
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user



class ReasonCreationUpdation(APIView):

	"""
	Reason Creation & Updation POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create & update Discount Reason.

		Data Post: {
			"id"                       : "1"(Send this key in update record case,else it is not required!!)
			"reason"		           : "dddddd",
		}

		Response: {

			"success": True, 
			"message": "Discount Reason creation/updation api worked well!!",
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
			user = request.user.id
			cid = get_user(user)
			err_message = {}
			err_message["reason"] = \
					validation_master_anything(data["reason"],
					"Discount Reason",description_re, 2)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			if "id" in data:
				unique_check = DiscountReason.objects.filter(~Q(id=data["id"]),\
								Q(reason=data["reason"]),Q(Company_id=cid))
			else:
				unique_check = DiscountReason.objects.filter(Q(reason=data["reason"]),\
										Q(Company_id=cid))
			if unique_check.count() != 0:
				err_message["unique_check"] = "Discount Reason with this name already exists!!"
			else:
				pass
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			data["active_status"] = 1
			data['Company'] = cid
			if "id" in data:
				reason_record = DiscountReason.objects.filter(id=data['id'])
				if reason_record.count() == 0:
					return Response(
					{
						"success": False,
	 					"message": "Discount Reason is not valid to update!!"
					}
					)
				else:
					data["updated_at"] = datetime.now()
					reason_serializer = \
					ReasonSerializer(reason_record[0],data=data,partial=True)
					if reason_serializer.is_valid():
						data_info = reason_serializer.save()
						info_msg = "Discount Reason is updated successfully!!"
					else:
						print("something went wrong!!")
						return Response({
							"success": False, 
							"message": str(reason_serializer.errors),
							})
			else:
				reason_serializer = ReasonSerializer(data=data)
				if reason_serializer.is_valid():
					data_info = reason_serializer.save()
					info_msg = "Discount Reason  is created successfully!!"
				else:
					print("something went wrong!!")
					return Response({
						"success": False, 
						"message": str(reason_serializer.errors),
						})
			return Response({
						"success": True, 
						"message": info_msg
						})
		except Exception as e:
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})