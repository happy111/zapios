import re
import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from Brands.models import Company
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from ZapioApi.api_packages import *
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from ZapioApi.Api.BrandApi.listing.listing import addr_set
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from UserRole.models import *
from django.db.models import Q
from Location.models import CountryMaster
from Configuration.models import CurrencyMaster
import random
from rest_framework import serializers
from rest_framework.status import (
	HTTP_200_OK,
	HTTP_406_NOT_ACCEPTABLE,
	HTTP_401_UNAUTHORIZED,
)

from django.db import transaction
from ZapioApiV2.Brand.brand_create_update import *
from _thread import start_new_thread
from google.oauth2 import id_token
from google.auth.transport import requests




class CompanySerializer(serializers.ModelSerializer):
	class Meta:
		model = Company
		fields = '__all__'

class BrandOutletGooglelogin(APIView):

	"""	
	Google login POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used to provide google login services to brands.

		Data Post: {

			"email"			        : "umesh@eoraa.com",
			"token"		            : "afadadadawe32432",

		}

		Response: {

			"success"				: true,
			"credential"			: true,
			"message"				: "You are logged in now!!",
			"user_type"				: "is_outlet",
			"token"					: "1614ffa75cb577542c76ae4ad6ea146b61d688fc",
			"user_id"				: 6
		}

	"""
	
	def post(self, request, format=None):
		try:
			data = request.data
			CLIENT_ID = "435927262966-kd4rrlpflk2an87qi1qblbet4v871n16.apps.googleusercontent.com"
			try:
				idinfo = id_token.verify_oauth2_token(data['tokenId'], requests.Request(), CLIENT_ID)
				userid = idinfo['sub']
			except ValueError:
				return Response({
					"success" : False,
					"message" : "Invalid token!!"
					})
			username = data["email"]
			err_message = {}
			password = "".join(
				random.choices(string.ascii_uppercase + string.digits, k=8)
			)
			check_brand = Company.objects.filter(company_email_id=username)
			is_cashier = ManagerProfile.objects.filter(Q(username=username) |
				Q(email=username))
			if check_brand.count()==1:
				company_id = check_brand[0].id
				user_type = "is_brand"
				p_id = str(4)
			else:
				pass
			if is_cashier.count()==1:
				p_id = is_cashier[0].user_type_id
				user_type = UserType.objects.filter(id=p_id)[0].user_type
				company_id = is_cashier[0].Company_id
				usernames = str(company_id)+'m'+str(data['email'])
			else:
				pass
			allmenu = MainRoutingModule.objects.filter(active_status=1).order_by('priority')
			alldata = []
			for i in allmenu:
				alls = {}
				company_id = str(11)
				chk_p = RollPermission.objects.filter(Q(company_id=company_id),Q(main_route_id=i.id),\
					Q(label=1),Q(user_type_id=4))
				if chk_p.count() > 0:
					alls['id'] = i.module_id
					alls['icon'] = i.icon
					alls['label'] = i.label
					alls['to'] = i.to
					alls['ids'] = i.id
					alls['ids'] = i.id
					rmodule = RoutingModule.objects.filter(main_route_id=i.id,active_status=1)
					if rmodule.count() > 0:
						alls['subs'] = []
						for j in rmodule:
							al = {}
							al['icon'] = j.icon
							al['label'] = j.label
							al['to'] = j.to
							r = SubRoutingModule.objects.filter(route_id=j.id,active_status=1)
							if r.count() > 0:
								al['subs'] = []
								for k in r:
									a = {}
									a['icon'] = k.icon
									a['label'] = k.label
									a['to'] = k.to
									al['subs'].append(a)
							alls['subs'].append(al)
					else:
						pass
					alldata.append(alls)
				else:
					pass
			if len(alldata) > 0:
				alldata = alldata
			else:
				alldata = []
			if check_brand.count() > 0:
				if check_brand.first().active_status == 0:
					return Response({
					"success" : False,
					"message" : "Company account is not active..Please contact admin!!"
					})
				else:
					pass
				user_exist = User.objects.filter(username=data['email'])
				if user_exist.count() > 0:
					pass
				else:
					username = check_brand[0].username
					user_exist = User.objects.filter(username=username)
				user_exist = user_exist.first()
				if (
					user_exist.is_staff==False
					and user_exist.is_active==True
					and user_exist.is_superuser == False
				):
					full_path = addr_set()
					token, created = Token.objects.get_or_create(user=user_exist)
					user_id = token.user_id
					if check_brand[0].is_firstUser == False:
						is_firstUser = True
					else:
						is_firstUser = False
					logo = check_brand[0].company_logo
					if logo != None and logo != "":
						logo = full_path+str(check_brand[0].company_logo)
					else:
						logo = None
					check_brand.update(is_firstUser=1)
					brand = check_brand[0].company_name
					co_id = Company.objects.filter(id=check_brand[0].id)
					curdata = CountryMaster.objects.filter(id=co_id[0].country_id)
					if curdata.count() > 0:
						sym = CurrencyMaster.objects.filter(id=curdata[0].currency_id)[0].symbol
					else:
						sym = ''
					return Response(
						{
							"success": True,
							"credential" : True,
							"message" : gettext_lazy("You are logged in now!!"),
							"user_type" : 'is_brand',
							"token": token.key,
							"user_id" : user_id,
							"name" : brand,
							"logo" : logo,
							"currency"  : sym,
							"country"  :  curdata[0].country,
							"is_firstUser" : is_firstUser,
							"url" : check_brand[0].website,
							"menu" : alldata,
							"eion_id" : check_brand[0].eion_brand_id
						},
						status=HTTP_200_OK,
					)
		
			is_cashier = ManagerProfile.objects.filter(Q(username=username) |
				Q(email=username))
			if is_cashier.count() > 0:
				login_type = is_cashier[0].login_type
				if len(login_type) > 0:
					if 'web' not in login_type:
						err_message['login_type'] ="Permissions denied, Please contact admin!!"
						return Response({
							"success" : False,
							"error"   : err_message,
							"message" : "Please correct listed errors!!"
						})
				else:
					err_message['login_type'] ="Permissions denied, Please contact admin!!"
					return Response({
						"success": False,
						"error" : err_message,
						"message" : "Please correct listed errors!!"
					})
			
			if is_cashier.count()==1:
				p_id = is_cashier[0].user_type_id
				user_type = UserType.objects.filter(id=p_id)[0].user_type
				company_id = is_cashier[0].Company_id
				usernames = str(company_id)+'m'+str(username)
				if is_cashier.first().active_status == 0:
					return Response({
					"success" : False,
					"message" : "ManagerProfile account is not active..Please contact admin!!"
					})
				else:
					pass
				user_exist = User.objects.filter(username=data['email'])
				if user_exist.count() > 0:
					pass
				else:
					user_exist = User.objects.filter(email=data['email'])
				user_exist = user_exist.first()
				if (
					user_exist.is_staff==False
					and user_exist.is_active==True
					and user_exist.is_superuser == False
				):
					full_path = addr_set()
					token, created = Token.objects.get_or_create(user=user_exist)
					user_id = token.user_id
					if is_cashier[0].is_firstUser == False:
						is_firstUser = True
					else:
						is_firstUser = False
					a = Company.objects.filter(id=is_cashier[0].Company_id)[0]
					brand = a.company_name
					co_id = Company.objects.filter(id=a.id)
					curdata = CountryMaster.objects.filter(id=co_id[0].country_id)
					if curdata.count() > 0:
						sym = CurrencyMaster.objects.filter(id=curdata[0].currency_id)[0].symbol
					else:
						sym = ''
					logo = a.company_logo
					if logo != None and logo != "":
						logo = full_path+str(logo)
					else:
						logo = None
					is_cashier.update(is_firstUser=1)
					return Response(
						{
							"success": True,
							"credential" : True,
							"message" : "You are logged in now!!",
							"user_type" : user_type,
							"token": token.key,
							"user_id" : user_id,
							"name" : brand,
							"logo" : logo,
							"currency"     : sym,
							"country"      :  curdata[0].country,
							"is_firstUser" : is_firstUser,
							"url"          : a.website,
							"menu" : alldata,
							"eion_id" : a.eion_brand_id

						},
						status=HTTP_200_OK,
					)
			else:
				pass
			if is_cashier.count() == 0 or check_brand.count() == 0:
				return Response(
						{
							"success"   : False,
							"credential" : False,
							"message"    : "This Username does not exist in the system!!",
						},
					)
		except Exception as e:
			print("Outlet/Brand Login Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})




class BrandOutletGoogleSignup(APIView):

	"""	
	Google Signup POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used to provide google signup services to brands.

		Data Post: {

				"company_name"        : "QWER",
				"business_nature"     : "1",
				"company_email_id"    : "abc@gmail.com",
				"company_contact_no"  : "8750477293",
				"country"             :     "1",
				"website              : "website"
				"googletoken"         :"token",

		}

		Response: {

			"success"				: true,
			"message"				: "Register Successfully!!",

		}

	"""
	
	def post(self, request, format=None):
		try:
			data = request.data
			CLIENT_ID = "435927262966-kd4rrlpflk2an87qi1qblbet4v871n16.apps.googleusercontent.com"
			try:
			    idinfo = id_token.verify_oauth2_token(data['googletoken'], requests.Request(), CLIENT_ID)
			    userid = idinfo['sub']
			    data["company_email_id"] = idinfo['email']
			except ValueError:
				return Response({
							"success" : False,
							"message" : "Invalid token!!"
					})
			allmenu = MainRoutingModule.objects.filter(active_status=1).order_by('priority')
			alldata = []
			for i in allmenu:
				alls = {}
				company_id = str(11)
				chk_p = RollPermission.objects.filter(Q(company_id=company_id),Q(main_route_id=i.id),\
					Q(label=1),Q(user_type_id=4))
				if chk_p.count() > 0:
					alls['id'] = i.module_id
					alls['icon'] = i.icon
					alls['label'] = i.label
					alls['to'] = i.to
					alls['ids'] = i.id
					alls['ids'] = i.id
					rmodule = RoutingModule.objects.filter(main_route_id=i.id,active_status=1)
					if rmodule.count() > 0:
						alls['subs'] = []
						for j in rmodule:
							al = {}
							al['icon'] = j.icon
							al['label'] = j.label
							al['to'] = j.to
							r = SubRoutingModule.objects.filter(route_id=j.id,active_status=1)
							if r.count() > 0:
								al['subs'] = []
								for k in r:
									a = {}
									a['icon'] = k.icon
									a['label'] = k.label
									a['to'] = k.to
									al['subs'].append(a)
							alls['subs'].append(al)
					else:
						pass
					alldata.append(alls)
				else:
					pass
			if len(alldata) > 0:
				alldata = alldata
			else:
				alldata = []
			data['username'] =  data["company_email_id"]
			data['plan_name']    = 1
			data['password'] = "".join(
				random.choices(string.ascii_uppercase + string.digits, k=8)
			)
			is_user  = User.objects.filter(Q(email=data['username']) |
				Q(username=data['username']))
			if is_user.count() > 0:
				raise Exception("Oops, this mail is already registered with Aizotec. Please try again through the Sign-in page, or use Forgot Password Function to reset your password")
			with transaction.atomic():
				user_exist = User.objects.create_user(
							username=data['username'], 
							password=data['password'],
							email=data['username']
						)
				if user_exist:
					data['auth_user'] = user_exist.id
					serializer = CompanySerializer(data=data)
					if serializer.is_valid(raise_exception=True):
						is_brand = serializer.save()
						brand_id = is_brand.id
						cdata = ConfigData(brand_id)
						if (
							user_exist.is_staff==False
							and user_exist.is_active==True
							and user_exist.is_superuser == False
						):
							full_path = addr_set()
							token, created = Token.objects.get_or_create(user=user_exist)
							user_id = token.user_id
							if is_brand.is_firstUser == False:
								is_firstUser = True
							else:
								is_firstUser = False
							a = Company.objects.filter(id=brand_id)[0]
							brand = a.company_name
							co_id = Company.objects.filter(id=a.id)
							curdata = CountryMaster.objects.filter(id=co_id[0].country_id)
							if curdata.count() > 0:
								sym = CurrencyMaster.objects.filter(id=curdata[0].currency_id)[0].symbol
							else:
								sym = ''
							logo = a.company_logo
							if logo != None and logo != "":
								logo = full_path+str(logo)
							else:
								logo = None
							co_id.update(is_firstUser=1)
							return Response(
								{
									"success": True,
									"credential" : True,
									"message" : gettext_lazy("You are logged in now!!"),
									"user_type" : "is_brand",
									"token": token.key,
									"user_id" : user_id,
									"name" : brand,
									"logo" : logo,
									"currency"     : sym,
									"country"      :  curdata[0].country,
									"is_firstUser" : is_firstUser,
									"url"          : a.website,
									"menu" : alldata
								},
								status=HTTP_200_OK,
							)
		except Exception as e:
			transaction.rollback()
			return Response({"message": str(e)}, status=HTTP_406_NOT_ACCEPTABLE)

