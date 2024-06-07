# from risingapi.serializers.customer_serializers import CustomerSignUpSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_201_CREATED, \
	HTTP_406_NOT_ACCEPTABLE, HTTP_200_OK, HTTP_503_SERVICE_UNAVAILABLE
from Customers.models import CustomerProfile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
import re
from ZapioApi.api_packages import *
import secrets
import datetime
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.http import Http404
from django.utils.translation import gettext_lazy

class CustomerSignin(APIView):
	"""
	Customer Login POST API
		
		Authentication Required		: No
		Service Usage & Description	: This Api is used to custome login.

		Data Post: {

			"username": "1114114718",
			"password": "123456",
			"company" : "3",
		}

		Response: {

			"success": True,
			"credential" : True,
			"message" : "You are logged in now!!",
			"token": token.key
		}

	"""
	def post(self, request, format=None):
		try:
			signin_data = request.data
			err_message = {}
			err_message["username"] =  validation_master_anything(
									signin_data["username"],
									"Username", contact_re, 10)

			err_message["password"] =  only_required(signin_data["password"],"Password")
			if any(err_message.values())==True:
				return Response({
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			username = signin_data['company'] + signin_data['username']
			is_user = CustomerProfile.objects.filter(username=signin_data['username'])
			if is_user.count()==1:
				if is_user.first().active_status == 0:
					return Response({
					"success" : False,
					"message" : "Account is not active..Please contact admin!!"
					})
				else:
					pass
				credential_check = \
					is_user.filter(pass_pin=signin_data['password'])
				if credential_check.count() == 1:
					pass
				else:
					return Response \
						({
						"success": False,
						"credential" : False,
						"message": \
						"Please enter valid login credentials!!"
						})
				user_authenticate = authenticate(username=username,
											password=signin_data['password'])
				if user_authenticate == None:
					return Response({
						"success": False,
						"credential" : False,
						"message": "Your account is not activated, please open your registered mobile!!"
						})
				else:
					pass
				if user_authenticate and user_authenticate.is_active == True \
										and user_authenticate.is_staff==False\
										and user_authenticate.is_superuser == False:
					login(request,user_authenticate)
					token, created = Token.objects.get_or_create(user=user_authenticate)
					return Response({
						"success": True,
						"credential" : True,
						"message" : gettext_lazy("You are logged in now!!"),
						"token": token.key
						})
				else:
					return Response({
						"success": False,
						"credential" : False,
						"message": gettext_lazy("Please enter valid login credentials!!")
						})
			else:
				return Response({
						"success": False,
						"credential" : False,
						"message": gettext_lazy("This mobile number does not exist in the system!!")
						})
		except Exception as e:
			print("Login Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})


class CustomerSignout(APIView):
	"""
	Post Data: {
		"token": "fcb12c357477382748004d68f815b1fb89e0c390",
	}
	Response: {
		"success": True,
		"message" : "You have been successfully logged out!!",

	}
	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			self.authuserId = request.user.id
			userData = User.objects.filter(id=self.authuserId).first()
			if userData:
				request.user.auth_token.delete()
				logout(request)
				return Response({
							"success": True,
							"message": gettext_lazy("You have been successfully logged out!!"),
							})
			else:
				return Response({
							"success": False,
							"message": "User not Found!!",
							})
		except Exception as e:
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})
