import re
import datetime
import os
import xlrd 
from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from Brands.models import Company
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from ZapioApi.api_packages import *
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from Configuration.models import Excelimport
from rest_framework import serializers
from Product.models import ProductCategory
from django.db.models import Q

class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = ProductCategory
		fields = '__all__'



class CategoryImport(APIView):
	"""
	Category Upload POST API

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
						"success":  False, 
						"message" : "Only xls is allowed" 
						})
			else:
				pass
			registration_data = {}
			cid = Company.objects.filter(auth_user=user.id)[0].id
			alldata = Excelimport.objects.create(image=data['image'],types='category')
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
				data['category_name'] = sheet.cell_value(i, 0)
				data['category_code'] = sheet.cell_value(i, 1)
				data['description']   = sheet.cell_value(i, 2)
				data['Company'] =  cid
				category_already_exist = ProductCategory.objects.filter(Q(category_name=data['category_name']),Q(Company_id=cid))
				if category_already_exist.count() > 0:
					e = category_already_exist[0].id
					cat = ProductCategory.objects.filter(id=e)
					if cat.count() > 0:
						category_serializer = CategorySerializer(cat[0],data=data,partial=True)
						if category_serializer.is_valid():
							category_serializer.save()
						else:
							print(category_serializer.errors)
					else:
						pass
				else:
					max_priority = \
							ProductCategory.objects.filter(Company_id=cid).aggregate(Max('priority'))
					mpid = max_priority["priority__max"] + 1
					data['priority'] = mpid
					category_serializer = CategorySerializer(data=data)
					if category_serializer.is_valid():
						category_serializer.save()
					else:
						print(category_serializer.errors)
			return Response({
						"success": True, 
						"message" : "Category Successfully" 
						})
		except Exception as e:
			print("Category creation/updation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})

