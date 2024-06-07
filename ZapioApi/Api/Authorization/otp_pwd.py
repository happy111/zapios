import json
import re
import os
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
from datetime import datetime
from django.db.models import Max
from ZapioApi.Api.BrandApi.listing.listing import addr_set, ProductlistingSerializer

#Serializer for api
from rest_framework import serializers
from Brands.models import Company
from UserRole.models import *
from email_validator import validate_email, EmailNotValidError
from Notification.models import EmailVerify
from _thread import start_new_thread
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


def otp_generator():
	import random
	otp = random.randint(1000, 9999)
	return otp

class EmailOTPSerializer(serializers.ModelSerializer):
	class Meta:
		model = EmailVerify
		fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
	class Meta:
		model = Company
		fields = '__all__'

class ManagerSerializer(serializers.ModelSerializer):
	class Meta:
		model = ManagerProfile
		fields = '__all__'

def email_send_module(post_data):
	try:
		to = post_data['email']
		cname = Company.objects.filter(id=post_data['Company'])[0]
		if cname.company_logo != None:
			domain_name = addr_set()
			full_path = domain_name + str(cname.company_logo)
		else:
			full_path = ''


		cc_email_id = []
		to_email = [
			to,
		]
		url = "https://api.sendgrid.com/v3/mail/send"
		headers = {'Content-type': 'application/json',
			"Authorization": "Bearer ",
		   'Accept': 'application/json'}
		
		data = {
			  "personalizations": [
				{
				  "to": [
					{
					  "email": to,
					},

				  ],
				  "dynamic_template_data": {
				   "company_name":cname.company_name,
				  "name":post_data['name'],
				  "otp" : post_data['otp'],
				  "logo" :full_path.strip()
 
				},
				}
			  ],
			  "from": {
				"email": "umeshsamal070@gmail.com",
				 "name" : cname.company_name
			  },
				"subject": "mail_subject",
				"template_id":"d-7fe20c18c4924925b8df961f9494bbc5",
				"content": [{"type": "text/html", "value": "Heya!"}]
			}
		response= requests.post(url,data=json.dumps(data),headers=headers)
		print(response)
		return response
	except Exception as e:
		print(e)

class EmailOtp(APIView):
	"""
	otp send POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to send otp.

		Data Post: {

			"email"		     : "12345678",
		}

		Response: {

			"success": True, 

		}

	"""
	def post(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			err_message = {}
			try:
				valid = validate_email(data["email"])  
			except EmailNotValidError as e:
				return Response(
						{
							"success": False, 
							"message": "Please enter a valid email!!"
						})
			is_brand = Company.objects.filter(company_email_id=data['email'])
			
			if is_brand.count() > 0:
				is_user = 0
			else:
				is_user  = ManagerProfile.objects.filter(email = data['email'])
				is_user = is_user.count()

			if is_user == 0 and is_brand.count() == 0:
				return Response({
						"success": False,
						"message": "Your credentials are not authenticated!!"
						})
			else:
				if is_brand.count() > 0:
					company = is_brand[0].id
				if is_user > 0:
					is_user  = ManagerProfile.objects.filter(email = data['email'])
					p_id = is_user[0].user_type_id
					user_type = UserType.objects.filter(id=p_id)[0].user_type
					company = is_user[0].Company_id
				else:
					pass
				email_data = EmailVerify.objects.filter(email=data['email'],types='cms')
				if email_data.count() > 0:
					post_data = {}
					post_data["otp"] = otp_generator()
					post_data["name"] = 'test'
					post_data['otp_creation_time'] =  datetime.now()
					post_data['active_status'] = 0
					post_data['types'] = 'cms'
					post_data["email"] = data['email']
					post_data["Company"] = company
					otp_serializer = EmailOTPSerializer(email_data[0],data=post_data,partial=True)
					if otp_serializer.is_valid():
						otp_serializer.save()
						res = start_new_thread(email_send_module, (post_data,))
						return Response(
							{
								"success": True, 
								"message": "OTP is send successfully",
							})
					else:
						return Response(
							{
								"success": False, 
								"message": "Error Occured !!",
							})
				else:
					post_data = {}
					post_data["otp"] = otp_generator()
					post_data["name"] = 'test'
					post_data['otp_creation_time'] =  datetime.now()
					post_data['active_status'] = 0
					post_data['types'] = 'cms'
					post_data["email"] = data['email']
					post_data["Company"] = company
					otp_serializer = EmailOTPSerializer(data=post_data)
					if otp_serializer.is_valid():
						otp_serializer.save()
						res = start_new_thread(email_send_module, (post_data,))
						return Response(
							{
								"success": True, 
								"message": "OTP is send successfully",

							})
					else:
						return Response(
							{
								"success": False, 
								"message": "Error Occured !!",
							})
		except Exception as e:
			print("OTP Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})




class VerifyOtp(APIView):

	"""
	Email verify POST API

		Authentication Required     : No
		Service Usage & Description : This Api is used to email verify.

		Data Post:  {
				
				"email" : "umesh@eoraa.com"
				"otp"   : ""
				
			  }

		Response: {

			"success": true,
			"message": "Email Verify successfully"
		}

	"""

	def post(self, request, format=None):
		try:
			post_data = request.data
			err_message = {}
			try:
				valid = validate_email(post_data["email"])  
			except EmailNotValidError as e:
				return Response(
						{
							"success": False, 
							"message": "Please enter a valid email!!"
						})
			email_data = EmailVerify.objects.filter(email=post_data['email'],\
				otp=post_data['otp'],active_status=0,types='cms')
			if email_data.count() > 0:
				post_data['otp_use_time'] =  datetime.now()
				otp_serializer = EmailOTPSerializer(email_data[0],data=post_data,partial=True)
				if otp_serializer.is_valid():
					otp_serializer.save()
					email_dt = EmailVerify.objects.filter(email=post_data['email'],\
						otp=post_data['otp'],types='cms')
					link_create_time = email_dt.first().otp_creation_time
					link_used_time = email_dt.first().otp_use_time
					time_diff = link_used_time-link_create_time
					get_minutes = time_diff.total_seconds() / 60
					expire_msg = "Your otp has been expired..please generate again!!"
					if get_minutes > 100:
						email_data.delete()
						return Response({
									"status": False,
									"message": expire_msg
									})
					else:
						email_data.update(active_status=1)
						email_data = EmailVerify.objects.filter(email=post_data['email'],types='cms',
							active_status=1)
						if email_data.count() > 0:
							return Response({
										"status": True,
										"message": "Verify Successfully!!",
										"company" : urlsafe_base64_encode(force_bytes(email_dt[0].Company_id)),
										"email"   : urlsafe_base64_encode(force_bytes(post_data['email']))
										})
			else:
				return Response({
									"status": False,
									"message": "Wrong otp!!"
									})


		except Exception as e:
			print(e)
			return Response(
				{
					"success": False,
					"message": "Email Verify api stucked into exception!!",
				}
			)

class ResetPassword(APIView):
	"""
	Change Password POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to change password of users.

		Data Post: {
			
			"new_pwd"		   : "123456",
			"c_pwd" 	       : "123456",
			"company"          : 1,
			"email"            : 
 		}

		Response: {

			"success": True, 
			"message": "Your password has been changed successfully!!",
		}

	"""

	def post(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			dt = {}
			err_message = {}
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
			
			is_brand = Company.objects.filter(id=data['company'],company_email_id=data['email'])
			is_user = ManagerProfile.objects.filter(Company=data['company'],email=data['email'])
			if is_user.count() == 0 and is_brand.count == 0:
				return Response({
						"oldpass": False,
						"message": "Your credentials are not authenticated!!"
						})
			
			if is_brand.count() > 0:
				data["username"] = is_brand[0].username
			else:
				data['username'] = is_user[0].username
			

			check_the_user = User.objects.filter(username=data['username']).first()
			if check_the_user == None:
				user_data = ManagerProfile.objects.filter(email=data['email'])
				if user_data.count() > 0:
					company_id = user_data[0].Company_id
					data['username'] =str(company_id)+'m'+str(user_data[0].username)
					check_the_user = User.objects.filter(username=data['username']).first()


			if check_the_user:
				try:
					data["password"] = request.data["new_pwd"]
					check_the_user.set_password(data["new_pwd"])
					check_the_user.save()
					if is_brand.count() > 0:
						serializer = CompanySerializer(is_brand[0],data=data, partial=True)
					else:
						data['password'] = data['password']
						serializer = ManagerSerializer(is_user[0],data=data, partial=True)
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
