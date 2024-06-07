import re
import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from Brands.models import Company,MergeBrand
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from ZapioApi.api_packages import *
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import logout
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from UserRole.models import *
from Location.models import CountryMaster
from Configuration.models import CurrencyMaster
from History.models import Logs
from rest_framework import serializers
from Event.models import PrimaryEventType



class LogSerializer(serializers.ModelSerializer):
	class Meta:
		model = Logs
		fields = '__all__'




class Poslogin(APIView):

	"""	
	Pos login POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used to provide login services to pos.

		Data Post: {

			"username"			    : "umesh",
			"password"		        : "123456"
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
	

	def post(self, request, format=None):
		try:
			data = request.data
			err_message = {}
			postdata = {}
			err_message["username"] =  only_required(data["username"],"Username")
			err_message["password"] =  only_required(data["password"],"Password")
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			is_pos = ManagerProfile.objects.filter(username=data['username'])
			if is_pos.count() > 0:
				login_type = is_pos[0].login_type
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
			else:
				return Response({
						"success": False,
						"credential" : False,
						"message": "Please enter valid login credentials!!"
						})


			Company_id = is_pos[0].Company_id
			co_id = Company.objects.filter(id=Company_id)
			curdata = CountryMaster.objects.filter(id=co_id[0].country_id)
			if curdata.count() > 0:
				sym = CurrencyMaster.objects.filter(id=curdata[0].currency_id)[0].symbol
			else:
				sym = ''
			if is_pos.count()==1:
				user_type = is_pos[0].user_type.user_type
				type_id = is_pos[0].user_type_id
				allmenu = BillingMainRoutingModule.objects.filter(active_status=1).order_by('priority')
				alldata = []
				for i in allmenu:
					alls = {}
					ids = i.id
					alls['module'] = i.module_name
					rp = BillRollPermission.objects.filter(user_type_id=type_id,company_id=Company_id,main_route_id=i.id)
					if rp.count() > 0:
						lp = rp[0].label
						if lp == False:
							alls['permissions'] = lp
						else:
							alls['permissions'] = lp
					else:
						alls['permissions'] = False
					alldata.append(alls)
				al = {}
				for j in alldata:
					al[j['module']] = j['permissions']
			else:
				return Response({
						"success": False,
						"message": "Username not found!"
						})
			if is_pos.count()==1:
				if is_pos[0].active_status == 0 or is_pos[0].is_hide == 1:
					return Response({
					"success" : False,
					"message" : "Pos account is not active..Please contact admin!!"
					})
				else:
					pass
				is_company = Company.objects.filter(id=is_pos[0].Company_id)[0]	
				if is_company.active_status == 0:
					return Response({
					"success" : False,
					"message" : "Your company account is deactivated due to some reason!!"
					})
				else:
					pass
				credential_check = \
					is_pos.filter(password=data['password'])
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
				username = str(is_company.id)+'m'+data['username']
				user_authenticate = authenticate(username=username,
											password=data['password'])
				if user_authenticate == None:
					return Response({
						"success": False,
						"credential" : False,
						"message": "Your account is not activated, please open your registered email!!"
						})
				else:
					pass
				if user_authenticate and user_authenticate.is_active == True \
										and user_authenticate.is_staff==False\
										and user_authenticate.is_superuser == False:
					login(request,user_authenticate)
					token, created = Token.objects.get_or_create(user=user_authenticate)
					user_id = token.user_id
					pro_pic = is_pos[0].manager_pic
					full_path = addr_set()
					if pro_pic != None and pro_pic != "":
						pic = full_path+str(pro_pic)
					else:
						pic = None
					clogo = is_company.company_logo
					if clogo !=None and clogo !="":
						clog = full_path+str(clogo)
					else:
						clog = None
					postdata['auth_user']  = user_id
					postdata['Company']  = Company_id
					postdata['event_by'] = data['username']
					postdata['count']  = 1
					postdata['relevance']  = '50'
					postdata['event_name']  = 'Login in Billing'
					ch_p = PrimaryEventType.objects.filter(event_type__icontains='Login in Billing')
					if ch_p.count() > 0:
						postdata['trigger']  = ch_p[0].id
					log_serializer = LogSerializer(data=postdata)
					if log_serializer.is_valid():
						data_info = log_serializer.save()
					else:
						print("something went wrong",log_serializer.errors)

					brands =Company.objects.filter(active_status=True,owner_phone=is_company.owner_phone)
					if brands.count() > 0:
						brand_list = []
						for bd in brands:
							brand_list.append(bd.id)
						if 	is_company.id in brand_list:
							brand = brand_list
						else:
							brand = []
					else:
						brand = []	
					return Response({
						"success": True,
						"credential" : True,
						"message" : "You are logged in now!!",
						"user_type" : user_type,
						"token": token.key,
						"user_id" : user_id,
						"username" : is_pos[0].username,
						"profile_pic" : pic,
						"company_logo" : clog,
						"company_name" : is_company.company_name,
						"company_id" : is_company.id,
						"permissions" : al,
						"currency"  : sym,
						"attendance_type":is_company.attendance_type,
						"brand" : brand
						})
				else:
					return Response({
						"success": False,
						"credential" : False,
						"message": "Please enter valid login credentials!!"
						})

			else:
				pass

		except Exception as e:
			print("POS Login Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})



class Poslogout(APIView):
	"""
	POS logout POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to provide logout service to pos.

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
							"message": "You have been successfully logged out!!",
							})
			else:
				return Response({
							"success": False,
							"message": "User not Found!!",
							})
		except Exception as e:
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})
