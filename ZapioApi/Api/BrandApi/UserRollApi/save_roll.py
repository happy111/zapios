from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime
from django.db.models import Q
import os
from django.db.models import Max
from ZapioApi.Api.BrandApi.Validation.category_error_check import *
from rest_framework import serializers
from Product.models import ProductCategory
from UserRole.models import *
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user

# class PermissionSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = BillRollPermission
# 		fields = '__all__'

class PermissionSerializer(serializers.ModelSerializer):
	class Meta:
		model = RollPermission
		fields = '__all__'




class SaveRoll(APIView):
	"""
	User Permission Creation & Updation POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create & update user permission within brand.

		Data Post: {
			Hints : 0 = edit 1 = view 2 = None

			"user_type"		       : "1",
			"main_route"		   : "1",
			"label"	               : 0,

		}
		Response: {

			"success": True, 
			"message": "Category creation/updation api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = {}
			auth_id = request.user.id
			Company_id = get_user(auth_id)
			userdata = UserType.objects.filter(Q(active_status=1)).order_by('id')
			for i in userdata:
				user_type = i.id
				#allmenu = BillingMainRoutingModule.objects.filter(active_status=1)
				allmenu = MainRoutingModule.objects.filter(active_status=1)
				print("eeeeeeeeeeeeeeee444",allmenu)
				for j in allmenu:
					main_module = j.id
					data['user_type']  = user_type
					data['main_route'] = main_module
					data['company'] = Company_id
					data['label'] = 1
					#roll_count = BillRollPermission.objects.filter(Q(company=Company_id),Q(user_type_id=user_type),Q(main_route_id=main_module))
					roll_count = RollPermission.objects.filter(Q(company=Company_id),Q(user_type_id=user_type),Q(main_route_id=main_module))
					print("rrrrrrrrrrrrrrrr",roll_count.count())
					if roll_count.count() > 0:
						per_serializer = PermissionSerializer(roll_count[0],data=data,partial=True)
						if per_serializer.is_valid():
							data_info = per_serializer.save()
						else:
							print("tttttttttttttttttttt",per_serializer.errors)
					else:
						per_serializer = PermissionSerializer(data=data)
						if per_serializer.is_valid():
							data_info = per_serializer.save()
						else:
							print("aaaaaaaa",per_serializer.errors)
			return Response({
						"success": True, 
						"message": "User Role api worked well!!"
						})
		except Exception as e:
			print("User Roll Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})

