from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from Brands.models import Company
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import re
from ZapioApi.api_packages import *
import datetime
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from Customers.serializers.customer_serializer import CustomerSignUpSerializer,CustomerOTPSerializer
from Customers.models import CustomerProfile

import os
import xlrd 
from Configuration.models import Excelimport


class CustomerImport(APIView):
	"""
	Customer Upload POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to customer upload.

		Data Post: {
				"image" : 'a.jpg'
		}
		Response: {

		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			user = request.user
			chk_ext =  str(data["image"])
			a = chk_ext.split('.')
			ext = a[1]
			if ext != 'xls':
				return Response({
						"success": False, 
						"message" : "Only xls is allowed" 
						})
			else:
				pass
			registration_data = {}
			cid = Company.objects.filter(auth_user=user.id)[0].id
			alldata = Excelimport.objects.create(image=data['image'],types='customer')
			dt = Excelimport.objects.filter(id=alldata.id)[0].image
			a = os.path.join(os.path.dirname(os.path.dirname(__file__)))
			b = a.replace("ZapioApi/Api/BrandApi","")
			ad =b+'media/'+str(dt)
			wb = xlrd.open_workbook(ad) 
			sheet = wb.sheet_by_index(0) 
			sheet.cell_value(0, 0) 
			a =[]
			for i in range(1,sheet.nrows):
				data = {}
				data['name'] = sheet.cell_value(i, 0)
				c = sheet.cell_value(i, 1)
				data['username'] = str(cid)+str(c)
				data['pas_pin'] =  sheet.cell_value(i, 2)
				data['email'] = sheet.cell_value(i, 3)
				data['address'] =  sheet.cell_value(i, 4)
				data['company'] =  cid
				user_already_exist = User.objects.filter(username=data['username'])
				if user_already_exist.count() > 0:
					e = user_already_exist[0].id
					registration_data["name"] = data['name']
					registration_data["username"] = data['username']
					registration_data["email"] = data['email']
					registration_data["pass_pin"] = str(data['pas_pin'])
					registration_data["address"] = data['address']
					registration_data["company"] = data['company']
					registration_data["mobile"] = str(int(c))
					cus = CustomerProfile.objects.filter(auth_user_id=e)
					if cus.count() > 0:
						customer_registration_serializer = CustomerSignUpSerializer(cus[0],data=registration_data,partial=True)
						if customer_registration_serializer.is_valid():
							customer_registration_serializer.save()
						else:
							print(customer_registration_serializer.errors)
					else:
						pass
				else:
					create_user = User.objects.create_user(
									username=data['username'],
									email=data['username'],
									password=data['pas_pin'],
									is_staff=False,
									is_active=True
									)
					if create_user:
						registration_data["auth_user"] = create_user.id
						registration_data["name"] = data['name']
						registration_data["username"] = data['username']
						registration_data["email"] = data['email']
						registration_data["pass_pin"] = str(data['pas_pin'])
						registration_data["address"] = data['address']
						registration_data["company"] = data['company']
						registration_data["active_status"] = 1
						registration_data["mobile"] = str(int(c))
						customer_registration_serializer = CustomerSignUpSerializer(data=registration_data)
						if customer_registration_serializer.is_valid():
							customer_registration_serializer.save()
						else:
							print(customer_registration_serializer.errors)
					else:
						pass
			return Response({
						"success": True, 
						"message" : "Registration Successfully" 
						})
		except Exception as e:
			print("Step process creation/updation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})

