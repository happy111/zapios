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
import time
import dateutil.parser
import requests 
import json
import os
import re

class POSSerializer(serializers.ModelSerializer):

	class Meta:
		model = SushiyaCustomer
		fields = '__all__'


class BoatData(APIView):
	def post(self, request, format=None):
		try:
			datas = request.data
			for i in range(1,100):
				datas['page'] = str(i)
				url = "http://192.168.0.112:1234/api/front/pos/alldata/"
				headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
				response= requests.post(url,data=json.dumps(datas),headers=headers)
			return Response({"success": True, 
						"message": "Save Successfully", 
						"data" : response
						})
		except Exception as e:
			print("POS data creation/updation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, 
							"message": "Error happened!!", 
							"errors": str(e)})
