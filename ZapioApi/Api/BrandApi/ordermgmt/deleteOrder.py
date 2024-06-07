from datetime import datetime
import requests
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_tracking.mixins import LoggingMixin
from rest_framework import serializers
from django.http import HttpResponse
from Orders.models import Order,OrderStatusType,OrderTracking
from rest_framework.permissions import IsAuthenticated
import dateutil.parser
from Brands.models import Company
from Outlet.models import OutletProfile
from rest_framework.authtoken.models import Token
from UserRole.models import ManagerProfile

from datetime import datetime, timedelta
from django.db.models import Count, Sum, Max, Avg, Case, When, Value, IntegerField, BooleanField
from ZapioApi.api_packages import *


class DeleteOrder(APIView):
	"""
	Order data GET API

		Authentication Required		: Yes
		Service Usage & Description	: .Download Order csv file

		Data Post: {
			"start_date" :""
			"end_date" : ""
			"outlet_id" : []
		}

		Response: {

			"success": True, 
			"message": "Dashboard card analysis api worked well!!",
			"data": final_result
		}

	"""
	def post(self, request, format=None):
		try:
			record = \
			Order.objects.filter(Q(outlet_id=33)|Q(outlet_id=None)|Q(id=131)|Q(id=305)|Q(id=345)|Q(id=589)|Q(id=281))
			
			for i in record:
				track_delete = OrderTracking.objects.filter(order=i.id).delete()
			record_delete = record.delete()
			return Response({
							"success": True,
							"data" : []
							})

		except Exception as e:
			print(e)
			return Response(
						{"error":str(e)}
						)
			

