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
from Product.models import Product
from django.db.models import Q

class ProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = '__all__'



class ProductImport(APIView):
	"""
	Product Upload POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to product upload.

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
			alldata = Excelimport.objects.create(image=data['image'],types='product')
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
				data['product_name'] = sheet.cell_value(i, 0)
				data['product_code'] = sheet.cell_value(i, 1)
				data['product_desc']   = sheet.cell_value(i, 2)
				data['kot_desc'] = sheet.cell_value(i, 3)
				data['price'] = sheet.cell_value(i, 4)
				data['discount_price']   = sheet.cell_value(i, 5)
				data['Company'] =  cid
				product_already_exist = Product.objects.filter(Q(product_name=data['product_name']),Q(Company_id=cid))
				if product_already_exist.count() > 0:
					e = product_already_exist[0].id
					pro = Product.objects.filter(id=e)
					if pro.count() > 0:
						product_serializer = ProductSerializer(cat[0],data=data,partial=True)
						if product_serializer.is_valid():
							product_serializer.save()
						else:
							print(product_serializer.errors)
					else:
						pass
				else:
					max_priority = \
							Product.objects.filter(Company_id=cid).aggregate(Max('priority'))
					mpid = max_priority["priority__max"] + 1
					data['priority'] = mpid
					product_serializer = ProductSerializer(data=data)
					if product_serializer.is_valid():
						product_serializer.save()
					else:
						print(product_serializer.errors)
			return Response({
						"success": True, 
						"message" : "Product Successfully" 
						})
		except Exception as e:
			print("Product creation/updation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})

