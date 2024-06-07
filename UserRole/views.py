from rest_framework.views import APIView
from rest_framework.response import Response
from UserRole.models import UserType
from rest_framework.permissions import IsAuthenticated
from UserRole.models import *
from Brands.models import Company
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user
from UserRole.Validation.usertype_error_check import *
from .serializers import *
from ZapioApi.api_packages import *
from UserRole.Validation.route_error_check import *
from UserRole.Validation.sub_route_error_check import *
from UserRole.Validation.manager_error_check import *


class UserTypeListing(APIView):
	"""
	User listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of user type data within brand.
	"""
	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			record = UserType.objects.filter(Company_id=1).order_by('-created_at')
			final_result = []
			if record.count() > 0:
				for i in record:
					record_dict = {}
					record_dict['user_type'] = i.user_type
					record_dict['id'] = i.id
					record_dict['active_status'] = i.active_status
					final_result.append(record_dict)
				return Response({
						"success": True, 
						"data": final_result})
			else:
				return Response({
						"success": True, 
						"data": []})
		except Exception as e:
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})



class UserTypeActiveListing(APIView):
	"""
	User listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of user type data within brand.
	"""
	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			record = UserType.objects.filter(active_status=1)
			final_result = []
			if record.count() > 0:
				for i in record:
					record_dict = {}
					record_dict['user_type'] = i.user_type
					record_dict['id'] = i.id
					final_result.append(record_dict)
				return Response({
						"success": True, 
						"data": final_result})
			else:
				return Response({
						"success": True, 
						"data": []})
		except Exception as e:
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})



class UserTypeRetrieval(APIView):
	"""
	UserType retrieval POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of UserType data.

		Data Post: {
			"id"                   : "1"
		}

		Response: {

			"success": True, 
			"message": "UserType retrieval api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			err_message = {}
			err_message["id"] = \
					validation_master_anything(data["id"],
					"UserType Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = UserType.objects.filter(id=data['id'])
			if record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Provided UserType data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				q_dict = {}
				q_dict["id"] = record[0].id
				q_dict["user_type"] = record[0].user_type
				q_dict["active_status"] = record[0].active_status
				final_result.append(q_dict)
			return Response({
						"success": True, 
						"message": "UserType retrieval api worked well!!",
						"data": final_result,
						})
		except Exception as e:
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})



class UserTypeCreationUpdation(APIView):
	"""
	UserType Creation & Updation POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create & update User Types.

		Data Post: {
			"id"                   : "1",(Send this key in update record case,else it is not required!!)
			"user_type"		   	   : "Outlet manager"
		}

		Response: {

			"success": True, 
			"message": "UserType creation/updation api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			from Brands.models import Company
			data = request.data
			auth_id = request.user.id
			Company_id = get_user(auth_id)
			validation_check = err_check(data)
			if validation_check != None:
				return Response(validation_check) 
			integrity_check = record_integrity_check(data,auth_id)
			if integrity_check != None:
				return Response(integrity_check)
			data["Company"] = Company_id
			if "id" in data:
				record = UserType.objects.filter(id=data['id'])
				if record.count() == 0:
					return Response(
					{
						"success": False,
	 					"message": "User Type data is not valid to update!!"
					}
					)
				else:
					data["updated_at"] = datetime.now()
					serializer = \
					UserTypeSerializer(record[0],data=data,partial=True)
					if serializer.is_valid():
						data_info = serializer.save()
						info_msg = "User Type is updated successfully!!"
					else:
						print("something went wrong!!")
						return Response({
							"success": False, 
							"message": str(addon_serializer.errors),
							})
			else:
				serializer = UserTypeSerializer(data=data)
				if serializer.is_valid():
					data_info = serializer.save()
					info_msg = "User Type is created successfully!!"
				else:
					print("something went wrong!!")
					return Response({
						"success": False, 
						"message": str(serializer.errors),
						})
			return Response({
						"success": True, 
						"message": info_msg
						})
		except Exception as e:
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})



class UserTypeAction(APIView):
	"""
	UserType Action POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to activate or deactivate UserType.

		Data Post: {
			"id"                   		: "2",
			"active_status"             : "0"
		}

		Response: {

			"success": True, 
			"message": "User Type is deactivated now!!"
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			from django.db.models import Q
			data = request.data
			err_message = {}
			if data["active_status"] == "true":
				pass
			elif data["active_status"] == "false":
				pass
			else:
				err_message["active_status"] = "Active status data is not valid!!"
			err_message["id"] = \
						validation_master_anything(data["id"],
						"UserType Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = UserType.objects.filter(id=data["id"])
			if record.count() != 0:
				data["updated_at"] = datetime.now()
				if data["active_status"] == "true":
					info_msg = "User Type is activated successfully!!"
				else:
					info_msg = "User Type is deactivated successfully!!"
				serializer = \
				UserTypeSerializer(record[0],data=data,partial=True)
				if serializer.is_valid():
					data_info = serializer.save()
				else:
					print("something went wrong!!")
					return Response({
						"success": False, 
						"message": str(serializer.errors),
						})
			else:
				return Response(
					{
						"success": False,
						"message": "UserType id is not valid to update!!"
					}
					)
			return Response({
						"success": True, 
						"message": info_msg
						})
		except Exception as e:
			print("UserType action Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})




class ManagersListing(APIView):
	"""
	Managers Profile listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of manager profile data within brand.
	"""
	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			user = request.user.id
			ch_brand = Company.objects.filter(auth_user_id=user)
			if ch_brand.count() > 0:
				nuser=user
			else:
				pass
			ch_cashier = ManagerProfile.objects.filter(auth_user_id=user)
			if ch_cashier.count() > 0:
				company_id = ch_cashier[0].Company_id
				auth_user_id = Company.objects.filter(id=company_id)[0].auth_user_id
				nuser=auth_user_id
			else:
				pass
			record = ManagerProfile.objects.filter(Company__auth_user=nuser,is_hide=0).order_by('-created_at')
			final_result = []
			if record.count() > 0:
				for i in record:
					record_dict = {}
					record_dict['user_type'] = i.user_type.user_type
					record_dict['is_attandance'] = i.is_attandance
					record_dict['id'] = i.id
					record_dict['active_status'] = i.active_status
					record_dict['first_name'] = i.manager_name
					record_dict['last_name'] = i.last_name
					record_dict['is_rider'] = i.is_rider
					record_dict["km"] = i.km
					record_dict["compensation"] = i.compensation
					record_dict["mobile"] = i.mobile
					email = i.email
					record_dict['is_hide'] = i.is_hide
					if email == None:
						record_dict['email'] = "N/A"
					else:
						record_dict['email'] = email
					record_dict['username'] = i.username
					final_result.append(record_dict)
				return Response({
						"success": True, 
						"data": final_result})
			else:
				return Response({
						"success": True, 
						"data": []})
		except Exception as e:
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})



class ManagerRetrieval(APIView):
	"""
	Manager retrieval POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of Manager data.

		Data Post: {
			"id"                   : "1"
		}

		Response: {

			"success": True, 
			"message": "Manager retrieval api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			err_message = {}
			err_message["id"] = \
					validation_master_anything(data["id"],
					"Manager Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = ManagerProfile.objects.filter(id=data['id'])
			if record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Provided manager data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				q_dict = {}
				q_dict["id"] = record[0].id
				q_dict["user_type_details"] = []
				user_type_dict = {}
				user_type_dict["label"] = record[0].user_type.user_type
				user_type_dict["key"] = record[0].user_type_id
				user_type_dict["value"] = record[0].user_type_id
				q_dict["user_type_details"].append(user_type_dict)
				q_dict["active_status"] = record[0].active_status
				q_dict["username"] = record[0].username
				q_dict["first_name"] = record[0].manager_name
				q_dict["last_name"] = record[0].last_name
				q_dict["is_attandance"] = record[0].is_attandance
				q_dict["is_rider"] = record[0].is_rider
				q_dict["password"] = record[0].password
				q_dict["km"] = record[0].km
				q_dict["compensation"] = record[0].compensation
				q_dict["mobile"] = record[0].mobile
				if record[0].login_type != None:
					q_dict["login_detail"] = []
					for index in record[0].login_type:
						login_dict = {}
						login_dict["label"] = index
						login_dict["key"] = index
						login_dict["value"] = index
						q_dict["login_detail"].append(login_dict)
				else:
					q_dict["login_detail"] = None 
				q_dict['outlet'] = []
				if len(record[0].outlet) > 0:
					a = record[0].outlet
					for i in a:
						out = {}
						
						out['label'] = OutletProfile.objects.filter(id=str(i))[0].Outletname
						out['value'] = int(i)
						q_dict['outlet'].append(out)
				else:
					pass
				final_result.append(q_dict)
			return Response({
						"success": True, 
						"message": "Manager retrieval api worked well!!",
						"data": final_result,
						})
		except Exception as e:
			print("Manager retrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})



def genrate_invoice_number(cname,cid):
	chk_data = ManagerProfile.objects.filter(Company_id=cid)
	if chk_data.count() > 0:
		eid = chk_data.last().employee_id
		if eid != None:
			ids = int(eid.replace(cname.upper(),'0'))
			fid = ids + 1
			length = len(str(fid))
			fl = 3 - length
			number = ('0' * fl)+str(fid)
			return str(cname.upper())+str(number)
		else:
			return str(cname.upper())+str('001')


class ManagerCreationUpdation(APIView):
	"""
	Manager Creation/Updation POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create new outlets within brand.

		Data Post: {
			
			"id"                    : "1"(In case of updation, optional key)
			"outlet"                : [1,2],
			"username"			    : "insta_assist_mgr",
			"password"		        : "123456",
			"user_type" 			: "1",
			"first_name"            : "umesh",
			"last_name"             : "samal"
			"login_type"            : "[]"   For example android/web/ios
			"is_attandance"         : 'true',
			"is_rider"              : 'true',
			"compensation"          : '0',
			"km"					: "4"

		}

		Response: {

			"success": True,
			"message": "Manager is registered successfully under your brand!!"
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			auth_id = request.user.id
			Company_id = get_user(auth_id)
			data["Company"] = Company_id
			data["auth_username"] = str(data["Company"])+"m"+str(data["username"])
			validation_check = err_check(data)
			if validation_check != None:
				return Response(validation_check)
			integrity_check = record_integrity_check(data,auth_id,data['Company'])
			if integrity_check != None:
				return Response(integrity_check)
			if "id" not in data:
				create_user = User.objects.create_user(
							username=data["auth_username"],
							password=data['password'],
							is_staff=False,
							is_active=True
							)
				if create_user:
					data["active_status"] = 1
					data["auth_user"] = create_user.id
					company_name = Company.objects.filter(id=Company_id)[0].company_name
					data['employee_id'] = genrate_invoice_number(company_name,Company_id)	
					data['manager_name'] = data['first_name']
					serializer = ManagerSerializer(data=data)
					if serializer.is_valid():
						data_info = serializer.save()
						info_msg = "Staff is registered successfully under your brand!!"
					else:
						create_user.delete()
						print(str(serializer.errors))
						return Response({
							"success": False, 
							"message": str(serializer.errors)
							})
				else:
					return Response(
					{
					"success": False,
					"message": "Some error occured in the process of manager profile creation!!"
					}
					)
			else:
				del data["username"]
				record = ManagerProfile.objects.filter(id=data["id"])
				manager_auth_id = record[0].auth_user_id
				check_the_user = User.objects.filter(id=manager_auth_id).first()
				check_the_user.set_password(data["password"])
				check_the_user.save()
				data["updated_at"] = datetime.now()
				data['manager_name'] = data['first_name']
				company_name = Company.objects.filter(id=Company_id)[0].company_name
				if record[0].employee_id !=None:
					pass
				else:
					data['employee_id'] = genrate_invoice_number(company_name,Company_id)	
				serializer = ManagerSerializer(record[0],data=data,partial=True)
				if serializer.is_valid():
					data_info = serializer.save()
					info_msg = "Staff record is updated successfully!!"
				else:
					print("something went wrong!!")
					return Response({
						"success": False, 
						"message": str(serializer.errors),
						})
			return Response({
						"success": True,
						"message": info_msg
						})
		except Exception as e:
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})



class ManagerAction(APIView):
	"""
	Manager Profile Action POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to activate or deactivate manager profile.

		Data Post: {
			"id"                   		: "2",
			"active_status"             : "0"
		}

		Response: {

			"success": True, 
			"message": "This profile is deactivated now!!"
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			from django.db.models import Q
			data = request.data
			err_message = {}
			if data["active_status"] == "true":
				pass
			elif data["active_status"] == "false":
				pass
			else:
				err_message["active_status"] = "Active status data is not valid!!"
			err_message["id"] = \
						validation_master_anything(data["id"],
						"Manager Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = ManagerProfile.objects.filter(id=data["id"])
			if record.count() != 0:
				data["updated_at"] = datetime.now()
				if data["active_status"] == "true":
					info_msg = "This profile is activated successfully!!"
				else:
					info_msg = "This profile is deactivated successfully!!"
				serializer = \
				ManagerProfileSerializer(record[0],data=data,partial=True)
				if serializer.is_valid():
					data_info = serializer.save()
				else:
					print("something went wrong!!")
					return Response({
						"success": False, 
						"message": str(serializer.errors),
						})
			else:
				return Response(
					{
						"success": False,
						"message": "Manager id is not valid to update!!"
					}
					)
			return Response({
						"success": True, 
						"message": info_msg
						})
		except Exception as e:
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})



class ModuleListing(APIView):
	"""
	Module listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of module data within brand.
	"""
	# permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			record = MainRoutingModule.objects.filter(active_status=1)
			final_result = []
			if record.count() > 0:
				for i in record:
					record_dict = {}
					record_dict['module_id'] = i.module_id
					record_dict['icon'] = i.icon
					record_dict['label'] = i.label
					record_dict['to'] = i.to
					record_dict['component'] = i.component
					route_record = RoutingModule.objects.filter(active_status=1,main_route=i.id)
					if route_record.count() != 0:
						record_dict['subs'] = []
						for j in route_record:
							route_dict = {}
							route_dict['icon'] = j.icon
							route_dict['label'] = j.label
							route_dict['to'] = j.to
							route_dict['component'] = j.component
							sub_route_record = \
							SubRoutingModule.objects.filter(active_status=1,route=j.id)
							if sub_route_record.count() != 0:
								route_dict['subs'] = []
								for k in sub_route_record:
									sub_route_dict = {}
									sub_route_dict['icon'] = k.icon
									sub_route_dict['label'] = k.label
									sub_route_dict['to'] = k.to
									sub_route_dict['component'] = k.component
									route_dict['subs'].append(sub_route_dict)
							else:
								pass
							record_dict['subs'].append(route_dict)
					else:
						pass
					final_result.append(record_dict)
				return Response({
						"success": True, 
						"data": final_result})
			else:
				return Response({
						"success": True, 
						"data": []})
		except Exception as e:
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})


class MainRouteListing(APIView):
	"""
	Main Route listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of Main Routes.
	"""
	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			record = MainRoutingModule.objects.filter(active_status=1)
			final_result = []
			if record.count() > 0:
				for i in record:
					record_dict = {}
					record_dict['module_id'] = i.id
					record_dict['module_name'] = i.module_name
					final_result.append(record_dict)
				return Response({
						"success": True, 
						"data": final_result})
			else:
				return Response({
						"success": True, 
						"data": []})
		except Exception as e:
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})



class RouteListing(APIView):
	"""
	Route listing POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of Routes.

		Data Post: {

			"main_routes" 	    : [1,2]
		}

		Response: {

			"success": true,
		    "data": final_result,
		    "message": "Route fetching successful!!"
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			validation_check = err_check(data)
			if validation_check != None:
				return Response(validation_check) 
			integrity_check = record_integrity_check(data)
			
			if integrity_check != None:
				return Response(integrity_check)
			record = RoutingModule.objects.filter(active_status=1)
			main_routes = data["main_routes"]
			final_result = []
			for i in main_routes:
				q = RoutingModule.objects.filter(active_status=1,main_route=i)
				if q.count() != 0:
					for j in q:
						record_dict = {}
						record_dict['module_id'] = j.id
						record_dict['module_name'] = j.module_name
						final_result.append(record_dict)
				else:
					pass
			return Response({
					"success": True, 
					"data": final_result})
		except Exception as e:
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})



class SubRouteListing(APIView):
	"""
	Sub Route listing POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of Sub Routes.

		Data Post: {

			"routes" 	    : [1,2]
		}

		Response: {

			"success": true,
		    "data": final_result,
		    "message": "Sub Route fetching successful!!"
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			validation_check = err_check(data)
			if validation_check != None:
				return Response(validation_check) 
			integrity_check = record_integrity_check(data)
			if integrity_check != None:
				return Response(integrity_check)
			routes = data["routes"]
			final_result = []
			for i in routes:
				q = SubRoutingModule.objects.filter(active_status=1,route=i)
				if q.count() != 0:
					for j in q:
						record_dict = {}
						record_dict['module_id'] = j.id
						record_dict['module_name'] = j.sub_module_name
						final_result.append(record_dict)
				else:
					pass
			return Response({
					"success": True, 
					"data": final_result})
		except Exception as e:
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})




class ManagerHide(APIView):
	"""
	Manager Profile Hide POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to hide or shiw manager profile.

		Data Post: {
			"id"                   		: "2",
			"is_hide"                   : "0"
		}

		Response: {

			"success": True, 

		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			from django.db.models import Q
			data = request.data
			err_message = {}
			if data["is_hide"] == "true":
				pass
			elif data["is_hide"] == "false":
				pass
			else:
				err_message["is_hide"] = "Hide status data is not valid!!"
			err_message["id"] = \
						validation_master_anything(data["id"],
						"Manager Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = ManagerProfile.objects.filter(id=data["id"])
			if record.count() != 0:
				data["updated_at"] = datetime.now()
				if data["is_hide"] == "true":
					info_msg = "This profile is hide successfully!!"
				else:
					info_msg = "This profile is show successfully!!"
				serializer = \
				ManagerProfileSerializer(record[0],data=data,partial=True)
				if serializer.is_valid():
					data_info = serializer.save()
				else:
					print("something went wrong!!")
					return Response({
						"success": False, 
						"message": str(serializer.errors),
						})
			else:
				return Response(
					{
						"success": False,
						"message": "Manager id is not valid to update!!"
					}
					)
			return Response({
						"success": True, 
						"message": info_msg
						})
		except Exception as e:
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})
