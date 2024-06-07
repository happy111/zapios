import re
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from Brands.models import Company
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from ZapioApi.api_packages import *
from datetime import datetime

from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from UserRole.models import ManagerProfile,UserType
from rest_framework import serializers




def addr_set():
	domain_name = "https://zapio-admin.com/media/"
	return domain_name


class ProfileSerializer(serializers.ModelSerializer):
	class Meta:
		model = ManagerProfile
		fields = '__all__'



class ProfileUpdate(APIView):

	"""	
	Profile Update POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to provide profile update to pos.

		Data Post: {

			"mobile"			    : "umesh",
			"email"		            : "123456"
			"profile_pic"           : "a.jpg"
		}

		Response: {

			    "success": true,
			    "credential": true,
			    "message": "You are logged in now!!",
			    "user_type": "Pos Manager",
			    "token": "5f7b5a511109b961e534604db0899910e354ee95",
			    "user_id": 150
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
			err_message["email"] = \
					validation_master_anything(data["email"],
					"Email",email_re, 3)
			err_message["mobile"] = \
					validation_master_exact(data["mobile"], "Mobile No.",contact_re, 10)
			if type(data["profile_pic"]) != str:
				im_name_path =  data["profile_pic"].file.name
				im_size = os.stat(im_name_path).st_size
				if im_size > 500*1024:
					err_message["image_size"] = "Profile can'nt excced the size more than 500kb!!"
			else:
				data["profile_pic"] = None
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			data["updated_at"] = datetime.now()
			pdata = ManagerProfile.objects.filter(auth_user_id=user.id)
			p_serializer = ProfileSerializer(pdata[0],data=data,partial=True)
			if p_serializer.is_valid():
				data_info = p_serializer.save()
			else:
				print("something went wrong!!")
				return Response({
					"success": False, 
					"message": str(p_serializer.errors),
					})

			alldata = ManagerProfile.objects.filter(auth_user_id=user.id)
			if alldata.count() > 0:
				res = {}
				res['username'] = alldata[0].username
				res['manager_name'] = alldata[0].manager_name
				res['email'] = alldata[0].email
				res['active_status'] = alldata[0].active_status
				res['password'] = alldata[0].password
				res['mobile'] = alldata[0].mobile
				full_path = addr_set()
				imgp = alldata[0].manager_pic
				if imgp != None and imgp != "":
					res['profile_pic'] = full_path+str(alldata[0].manager_pic)
				else:
					res['profile_pic'] = None
			return Response({
						"success": True, 
						"message": "Profile Update  api worked well!!",
						"data": res,
						})
		except Exception as e:
			print("Profile update updation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})