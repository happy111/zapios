from functools import partial
import json
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_406_NOT_ACCEPTABLE,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
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
from django.contrib.auth import logout
from ZapioApi.Api.BrandApi.listing.listing import addr_set
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from UserRole.models import *
from django.db.models import Q
from Location.models import CountryMaster
from Configuration.models import CurrencyMaster

from django.db import transaction
from django.utils.translation import gettext_lazy



class BrandOutletlogin(APIView):

	"""	
	Outlet/Brand login POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used to provide login services to outlets & brands.

		Data Post: {

			"username"			    : "insta_adarshnagar",
			"password"		        : "123456",
			"login_type"            : ""
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
	
	# permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			err_message = {}
			err_message["username"] =  only_required(data["username"],"Username")
			err_message["password"] =  only_required(data["password"],"Password")
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			is_brand = Company.objects.filter(Q(username=data['username']) | \
				Q(company_email_id=data['username']))
			is_cashier = ManagerProfile.objects.filter(Q(username=data['username']) |
				Q(email=data['username']),Q(password=data['password']))
			if is_cashier.count() > 0:
				login_type = is_cashier[0].login_type
				if len(login_type) > 0:
					if 'web' not in login_type:
						err_message['login_type'] ="Permissions denied, Please contact admin!!"
						return Response({
							"success": False,
							"error" : err_message,
							"message" : "Please correct listed errors!!"
						})
				else:
					err_message['login_type'] ="Permissions denied, Please contact admin!!"
					return Response({
						"success": False,
						"error" : err_message,
						"message" : "Please correct listed errors!!"
					})
			company_id = ''
			if is_brand.count()==1:
				company_id = is_brand[0].id
				user_type = "is_brand"
				p_id = str(12)
			else:
				pass
			if is_cashier.count()==1:
				p_id = is_cashier[0].user_type_id
				user_type = UserType.objects.filter(id=p_id)[0].user_type
				company_id = is_cashier[0].Company_id
				usernames = str(company_id)+'m'+str(data['username'])
			else:
				pass
			if is_brand.count() == 0 and is_cashier.count() == 0:
				return Response \
						({
						"success": False,
						"credential" : False,
						"message": \
						"Please enter valid login credentials!!"
						},status=HTTP_400_BAD_REQUEST)
			else:
				pass
			co_id = Company.objects.filter(id=company_id)
			curdata = CountryMaster.objects.filter(id=co_id[0].country_id)
			if curdata.count() > 0:
				sym = CurrencyMaster.objects.filter(id=curdata[0].currency_id)[0].symbol
			else:
				sym = ''
			allmenu = MainRoutingModule.objects.filter(active_status=1).order_by('priority')
			alldata = []
			for i in allmenu:
				alls = {}
				print(i.id)
				chk_p = RollPermission.objects.filter(Q(main_route_id=i.id),Q(label=1),Q(user_type_id=p_id))
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
			full_path = addr_set()
			if is_brand.count()==1:
				if is_brand.first().active_status == 0:
					return Response({
					"success" : False,
					"message" : "Company account is not active..Please contact admin!!"
					},status=HTTP_400_BAD_REQUEST)
				else:
					pass
				credential_check = \
					is_brand.filter(password=data['password'])
				if credential_check.count() == 1:
					pass
				else:
					return Response \
						({
						"success": False,
						"credential" : False,
						"message": \
						"Please enter valid login credentials!!"
						},status=HTTP_400_BAD_REQUEST)
				user_authenticate = authenticate(username=data['username'],
											password=data['password'])
				if user_authenticate == None:
					brand_data = Company.objects.filter(company_email_id=data['username'])
					data['username'] = brand_data[0].username
					user_authenticate = authenticate(username=data['username'],
											password=data['password'])

				brand = is_brand[0].company_name
				if user_authenticate == None:
					return Response({
						"success": False,
						"credential" : False,
						"message": "Your account is not activated, please open your registered email!!"
						},status=HTTP_400_BAD_REQUEST)
				else:
					pass
				if user_authenticate and user_authenticate.is_active == True \
										and user_authenticate.is_staff==False\
										and user_authenticate.is_superuser == False:
					login(request,user_authenticate)
					token, created = Token.objects.get_or_create(user=user_authenticate)
					user_id = token.user_id
					if is_brand[0].is_firstUser == False:
						is_firstUser = True
					else:
						is_firstUser = False

					logo = is_brand[0].company_logo
					if logo != None and logo != "":
						logo = full_path+str(is_brand[0].company_logo)
					else:
						logo = None
					is_brand.update(is_firstUser=1)
					return Response({
						"success": True,
						"credential" : True,
						"message" : gettext_lazy("You are logged in now sss!!"),
						"user_type" : user_type,
						"token": token.key,
						"user_id" : user_id,
						"name" : brand,
						"logo" : logo,
						"menu" : alldata,
						"currency"  : sym,
						"country"  :  curdata[0].country,
						"is_firstUser" : is_firstUser,
						"url" : is_brand[0].website,
						"eion_id" : is_brand[0].eion_brand_id
						})

				else:
					return Response({
						"success": False,
						"credential" : False,
						"message": gettext_lazy("Please enter valid login credentials!!")
						},status=HTTP_400_BAD_REQUEST)

			elif is_cashier.count()==1:
				if is_cashier.first().active_status == 0:
					return Response({
					"success" : False,
					"message" : gettext_lazy("ManagerProfile account is not active..Please contact admin!!")
					},status=HTTP_400_BAD_REQUEST)
				else:
					pass
				credential_check = \
					is_cashier.filter(password=data['password'])

				if credential_check.count() == 1:
					pass
				else:
					return Response \
						({
						"success": False,
						"credential" : False,
						"message": \
						gettext_lazy("Please enter valid login credentials!!")
						},status=HTTP_400_BAD_REQUEST)
				user_authenticate = authenticate(username=usernames,
											password=data['password'])
				if user_authenticate == None:
					profile_data = ManagerProfile.objects.filter(email=data['username'])
					data['username'] = profile_data[0].username
					user_authenticate = authenticate(username=data['username'],
											password=data['password'])
				a = Company.objects.filter(id=is_cashier[0].Company_id)[0]
				brand = a.company_name
				if user_authenticate == None:
					return Response({
						"success": False,
						"credential" : False,
						"message": gettext_lazy("Your account is not activated, please open your registered email!!")
						},status=HTTP_400_BAD_REQUEST)
				else:
					pass
				if user_authenticate and user_authenticate.is_active == True \
										and user_authenticate.is_staff==False\
										and user_authenticate.is_superuser == False:
					login(request,user_authenticate)
					token, created = Token.objects.get_or_create(user=user_authenticate)
					if is_cashier[0].is_firstUser == False:
						is_firstUser = True
					else:
						is_firstUser = False
					user_id = token.user_id
					logo = a.company_logo
					if logo != None and logo != "":
						logo = full_path+str(logo)
					else:
						logo = None
					is_cashier.update(is_firstUser=1)
					return Response({
						"success": True,
						"credential" : True,
						"message" : gettext_lazy("You are logged in now!!"),
						"user_type" : user_type,
						"token": token.key,
						"user_id" : a.auth_user_id,
						"name" : brand,
						"logo" : logo,
						"menu" : alldata,
						"currency"  : sym,
						"country"  :  curdata[0].country,
						"is_firstUser" : is_firstUser,
						"url" : a.website,
						"eion_id" : a.eion_brand_id
						})

				else:
					return Response({
						"success": False,
						"credential" : False,
						"message": gettext_lazy("Please enter valid login credentials!!")
						},status=HTTP_400_BAD_REQUEST)

			else:
				return Response({
						"success": False,
						"credential" : False,
						"message": gettext_lazy("This Username does not exist in the system!!")
						},status=HTTP_400_BAD_REQUEST)
		except Exception as e:
			print("Outlet/Brand Login Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})



class BrandOutletlogout(APIView):
	"""
	Outlet/Brand logout POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to provide logout service to outlets & brands.

		Data Post: {

			"token": "95dabfce1f8ebe9331851a1a1c5aa22bcb9b8120"
		}

		Response: {

			"success": True,
			"message" : "You have been successfully logged out!!"
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

