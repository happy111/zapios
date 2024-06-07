import time
import dateutil.parser
import requests
import os
import json
import re
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
from datetime import datetime
from django.db.models import Q
from django.db.models import Max
from rest_framework import serializers
from pos.models import POSOrder,SushiyaCustomer
from datetime import datetime, timedelta


class POSSerializer(serializers.ModelSerializer):
	class Meta:
		model = SushiyaCustomer
		fields = '__all__'


class PosData(APIView):
	"""
	POS data POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used to extract data for pos.

		Data Post: {
				"start_date"  : "2017-09-30"
				"end_date"     : "2017-09-23"
				"page"			: "1"
		}

		Response: {
		}

	2017-09-01
	"""

	def post(self, request, format=None):
		try:
			data = request.data
			stdate = data['start_date']
			ltdate = data['end_date']
			pag = data['page']
			url = 'https://api.posify.in/api/v1/order_report?__page='+pag+'&__limit=100&__start_date__equal='+stdate+'T00:00:00.619Z&__end_date__equal='+ltdate+'T00:00:00.619Z&__order_by=-invoice_number%27'
			response=requests.get(url, \
				headers=\
				{"Authorization":\
				".eJwFwckNwDAIALBdeBcJEo4wS9VHxLH_CLVfuCGRRo01HChtF0-zYBsfyloZofCAHpet3ia5ioaY3KV8mIjN98D3A9dwEsQ.XmjEgg.-OPalbo77njweZWhSDEpQ344XAk"})
			geodata = response.json()
			resdata = geodata['data']
			for i in resdata:
				alldata = {}
				co = i['created_on']
				s = str(i['created_on'])
				x = dateutil.parser.parse(i["created_on"])
				alldata['created_on'] = x
				alldata['customer_name'] = i['customer_name']
				alldata['customer_number'] = i['customer_number']
				t = i['date']
				o = dateutil.parser.parse(i["date"])
				alldata['date'] = o
				alldata['discount_value'] = i['discount_value']
				alldata['external_id'] = i['external_id']
				alldata['ids'] = i['id']
				alldata['invoice_number'] = i['invoice_number']
				alldata['order_type'] = i['order_type']
				alldata['outlet'] = i['outlet']
				alldata['payment_mode'] = i['payment_mode'][0]
				alldata['rider_name'] = i['rider_name']
				alldata['rider_number'] = i['rider_number']
				alldata['source'] = i['source']
				alldata['status_name'] = i['status_name']
				alldata['sub_total'] = i['sub_total']
				alldata['time'] = i['time']
				alldata['total'] = i['total']
				alldata['sub_total'] = i['sub_total']
				alldata['total_tax'] = i['total_tax']
				alldata['user_name'] = i['user_name']
				alldata['company'] = 4
				alldata1 = SushiyaCustomer.objects.filter(invoice_number=i['invoice_number'])
				if alldata1.count() == 1:
					pos_serializer = POSSerializer(alldata1[0],data=alldata,partial=True)
					if pos_serializer.is_valid():
						pos_serializer.save()
					else:
						return Response({
							"status" : False,
							"message" : aa.errors
							})
				else:
					try:
						pos_serializer = POSSerializer(data=alldata)
						if pos_serializer.is_valid():
							pos_serializer.save()
						else:
							return Response({
							"status" : False,
							"message" : pos_serializer.errors
							})
					except Exception as e:
						print(e)
			return Response({"success": True, 
							"message": "Save Successfully", 
							"data" : pos_serializer.data
							})
		except Exception as e:
			print("POS data creation/updation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, 
							"message": "Error happened!!", 
							"errors": str(e)})
