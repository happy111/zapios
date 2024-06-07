import re
from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
from rest_framework import serializers
from Configuration.models import PaymentMethod
from Location.models import CountryMaster
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user
from django.db.models import Q





class PaymentAllList(APIView):
	"""
	Payment Method listing Configuration POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to provide all payment method.

		Data Post: {

		}

		Response: {

			"success": True,
			"data" :  serializer,
			"message": "Payment Method listing api worked well!!"
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			err_message = {}
			auth_id = request.user.id
			cid = get_user(auth_id)
			data['company'] = cid
			query = PaymentMethod.objects.filter(company_id=cid)
			if query.count()==0:
				return Response(
					{
						"success": False,
	 					"message": "No Payment Method Found"
					}
					) 
			else:
				serializer = []
				for index in query:
					q_dict = {}
					q_dict["id"] = index.id
					q_dict["country"] = index.country.country
					q_dict["symbol"] = index.symbol
					q_dict["payment_method"] = index.payment_method
					q_dict["keyid"] = index.keyid
					q_dict["keySecret"] = index.keySecret
					q_dict["active_status"] = index.active_status
					q_dict["created_at"] = index.created_at
					q_dict["updated_at"] = index.updated_at
					q_dict["wordLimit"] = index.word_limit
					domain_name = addr_set()
					if index.payment_logo != "" and index.payment_logo != None:
						full_path = domain_name + str(index.payment_logo)
						q_dict['payment_logo'] = full_path
					else:
						q_dict['payment_logo'] = ''
					serializer.append(q_dict)
			return Response(
					{
						"success": True,
						"data" : serializer,
	 					"message": "Payment Method listing api worked well!!"
					}
					)
		except Exception as e:
			print("Payment Method listing api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})