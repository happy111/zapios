from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime
import os
from django.db.models import Max,Q

#Serializer for api
from rest_framework import serializers
from Brands.models import Company
from UserRole.models import ManagerProfile,UserType


class ProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = ManagerProfile
		fields = '__all__'


class Changepassword(APIView):

	"""
	Change Password POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to change password of pos users.

		Data Post: {
			"password"		   : "12345678",
			"new_pwd"		   : "123456",
			"c_pwd" 	       : "123456",
 		}

		Response: {

			"success": True, 
			"message": "Your password has been changed successfully!!",
		}

	"""

	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			user = request.user
			err_message = {}
			err_message["password"] = only_required(data["password"],"Old Password")
			err_message["new_pwd"] = validation_master_anything(data["new_pwd"],"New Password",
										pass_re, 6)
			err_message["c_pwd"] = validation_master_anything(data["c_pwd"],"Confirm Password",
									pass_re, 6)

			if data["new_pwd"]!=data["c_pwd"]\
					and err_message["c_pwd"]==None:
				err_message["c_pwd"] = "Your password don't match!!"

			if any(err_message.values())==True:
				return Response({
					"success": False, 
					"error" : err_message,
					"message" : "Please correct listed errors!!" 
					})



			is_user = ManagerProfile.objects.filter(Q(password=data["password"]),\
				Q(auth_user_id=user.id),Q(active_status=1))

			if is_user.count()!=1:
				return Response({
						"success": True,
						"message": "Your credentials are not authenticated!!"
						})
			else:
				data["username"] = is_user[0].username
			check_the_user = User.objects.filter(id=user.id).first()
			if is_user.count()==1 and check_the_user:
				try:
					data["password"] = request.data["new_pwd"]
					check_the_user.set_password(data["new_pwd"])
					check_the_user.save()
					serializer = ProfileSerializer(is_user[0],data=data, partial=True)

					if serializer.is_valid():
						serializer.save()
						user_authenticate = authenticate(username=data['username'], 
											password=data['password'])
						login(request,user_authenticate)
					else:
						print("something went wrong!!")
						return Response({
							"success": False, 
							"message": str(serializer.errors),
							})
					return Response({
						"success": True,
						"message": "Your password has been changed successfully!!"
						})
				except Exception as e:
					return Response({
					"success": False,
					"message": str(e)
					})
			else:
				return Response({
					"success": False,
					"message": str(check_the_user)
					})
		except Exception as e:
			print("Change Password Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})