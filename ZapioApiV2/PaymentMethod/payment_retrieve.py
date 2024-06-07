import re
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
from datetime import datetime
from Configuration.models import PaymentMethod
from Location.models import CountryMaster





class PaymentRetrieve(APIView):
	"""
	Payment Method retrieval POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of payment method data.

		Data Post: {
			"id"                   : "1"
		}

		Response: {

			"success": True, 
			"message": "Payment Method retrieval api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			err_message = {}
			err_message["id"] = \
					validation_master_anything(data["id"],
					"Payment Method Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = PaymentMethod.objects.filter(id=data['id'])
			if record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Provided Payment Method data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				q_dict = {}
				q_dict["id"] = record[0].id
				q_dict["country"] = record[0].country.country
				q_dict["cid"] = record[0].country_id
				q_dict["limit"] = record[0].word_limit
				q_dict["symbol"] = record[0].symbol
				q_dict["payment_method"] = record[0].payment_method
				q_dict["keyid"] = record[0].keyid
				q_dict["keySecret"] = record[0].keySecret
				q_dict["active_status"] = record[0].active_status
				q_dict["created_at"] = record[0].created_at
				q_dict["updated_at"] = record[0].updated_at
				domain_name = addr_set()
				if record[0].payment_logo != "" and record[0].payment_logo != None:
					full_path = domain_name + str(record[0].payment_logo)
					q_dict['payment_logo'] = full_path
				else:
					q_dict['payment_logo'] = ''
				final_result.append(q_dict)
			return Response({
						"success": True, 
						"message": "Payment Method retrieval api worked well!!",
						"data": final_result,
						})
		except Exception as e:
			print("Payment Method retrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})