from datetime import datetime
import requests
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_tracking.mixins import LoggingMixin
from rest_framework import serializers
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
import dateutil.parser
from Brands.models import Company
from Outlet.models import OutletProfile
from rest_framework.authtoken.models import Token
from UserRole.models import ManagerProfile

from datetime import datetime, timedelta


class AllOutlet(APIView):
	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			err_message = {}
			user = request.user.id
			is_outlet = OutletProfile.objects.filter(auth_user_id=user)
			is_brand = Company.objects.filter(auth_user_id=user)
			is_cashier = ManagerProfile.objects.filter(auth_user_id=user)
			
			if is_cashier.count() > 0:
				cid = ManagerProfile.objects.filter(auth_user_id=user)[0].Company_id
				outlet = is_cashier[0].outlet
				orderdata = []
				for i in outlet:
					adata = {}
					a = OutletProfile.objects.filter(id=i)
					outletnames =  a[0].Outletname
					orderdata.append(outletnames)
				a = sorted(orderdata)
				finaldata = []
				for k in a:
					adata = {}
					alloutlet = OutletProfile.objects.filter(Outletname=k)
					adata['id'] = alloutlet[0].id
					adata['Outletname'] = k
					finaldata.append(adata)
				if len(finaldata) > 0:
					return Response({
								"success": True,
								"data" : finaldata
								})
				else:
					return Response({
								"success": True,
								"data" : []
								})
			else:
				pass
			if is_outlet.count() > 0 or is_brand.count() > 0:
				if is_outlet.count() > 0:
					outlet = OutletProfile.objects.filter(auth_user_id=user)
					oid = outlet[0].id
					cid = outlet[0].Company_id
					alloutlet = OutletProfile.objects.filter(id=oid,active_status=1)
				else:
					alloutlet = OutletProfile.objects.filter(Company__auth_user=user,active_status=1)
				orderdata = []
				for i in alloutlet:
					adata = {}
					a = i.Outletname
					orderdata.append(a)
				a = sorted(orderdata)
				finaldata = []
				for k in a:
					adata = {}
					alloutlet = OutletProfile.objects.filter(Outletname=k)
					adata['id'] = alloutlet[0].id
					adata['Outletname'] = k
					finaldata.append(adata)
				if len(finaldata) > 0:
					return Response({
								"success": True,
								"data" : finaldata
								})
				else:
					return Response({
								"success": True,
								"data" : []
								})
		except Exception as e:
			print(e)
			return Response(
						{"error":str(e)}
						)
			

