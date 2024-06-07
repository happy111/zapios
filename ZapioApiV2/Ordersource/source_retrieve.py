import json
import re
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
from datetime import datetime

#Serializer for api
from rest_framework import serializers
from Configuration.models import OrderSource,PaymentMethod


	
class RetrieveSource(APIView):

	"""
	Source POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used for retrieval of Source data.

		Data Post: {
			"id"                   : "1"
		}

		Response: {

			"success": True, 
			"message": "source retrieval api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			err_message = {}
			err_message["id"] = \
					validation_master_anything(data["id"],"Source Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})

			record = OrderSource.objects.filter(id=data['id'])
			if record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Provided Source data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				q_dict = {}
				q_dict["id"] 			= record[0].id
				q_dict["source_name"]   = record[0].source_name				
				q_dict["active_status"] = record[0].active_status
				q_dict["created_at"]    = record[0].created_at
				q_dict["updated_at"]    = record[0].updated_at
				q_dict["is_edit"]       = record[0].is_edit

				im = str(record[0].image)
				if im != "" and im != None and im != "null":
					domain_name = addr_set()
					full_path = domain_name + str(record[0].image)
					q_dict['image'] = full_path
				else:
					q_dict['image'] = ''
				p_method = record[0].payment_method
				q_dict['payment_method'] = []
				if p_method != None:
					for index in p_method:
						di = {}
						di['value'] = int(index)
						pdata = PaymentMethod.objects.filter(id=index)
						di['label'] = pdata[0].payment_method
						pm = str(pdata[0].payment_logo)
						if pm != None and pm != "" and pm != "null":
							domain_name = addr_set()
							full_path = domain_name + str(pdata[0].payment_logo)
							di['image'] = full_path
						else:
							di['image'] = ''
						q_dict['payment_method'].append(di)
				else:
					pass
				final_result.append(q_dict)
			return Response({
						"success": True, 
						"message": "Source retrieval api worked well!!",
						"data": final_result,
						})
		except Exception as e:
			print("Source retrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})