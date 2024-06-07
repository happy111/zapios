from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
import json
from datetime import datetime
import os
from django.db.models import Max
from Brands.models import Company
from ZapioApi.api_packages import *
#Serializer for api
from rest_framework import serializers
from UserRole.models import ManagerProfile,UserType
from Customers.serializers.customer_serializer import CustomerSignUpSerializer
from Customers.models import CustomerProfile
from django.db.models import Q

class CustomerRegister(APIView):
	"""
	Customer Creation & Updation POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create & update customer.

		Data Post: {
			"id"                           : "1"(Send this key in update record case,else it is not required!!)
			"pass_pin"		               : "123456",
			"mobile"                       : "8750477098",
			"name"	       		           : "umesh",
			"email"                        : "umeshsamal3@gmail.com",
 			"address"              : [
								{
									"latitude"             : "432423234",
									"longitude"            : "324324324",
									"type"                 : "home",
									"secondary_address"    : "hari nagar ashram"
								}],
			
		}

		Response: {

			"success": True, 
			"message": "Customer creation/updation api worked well!!",
		
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			user = request.user
			registration_data = {}
			co_id = ManagerProfile.objects.filter(auth_user_id=user.id)[0].Company_id
			err_message = {}

			err_message["pass_pin"] =\
			 validation_master_anything(data["pass_pin"],"Password",pass_re, 6)

			err_message["mobile"] = \
					validation_master_exact(data["mobile"], "Mobile No.",contact_re, 10)

			err_message["name"] = \
					validation_master_anything(data["name"], "Name",alpha_re, 3)

			err_message["email"] = \
					validation_master_anything(data["email"],
					"Email",email_re, 3)

			if len(data["address"]) != 0:
				for i in data["address"]:
					if "latitude" in i and  "longitude" in i and "type" in i and "secondary_address" in i:
						pass
					else:
						err_message["address_detail"] = \
					"Customer latitude,longitude,type,secondary_address is not set!!"
						break	

					err_message["latitude"] = \
								validation_master_anything(i["latitude"],"latitude",
								lat_long_re,3)

					err_message["longitude"] = \
								validation_master_anything(i["longitude"],"longitude",
								lat_long_re,3)

					err_message["type"] = \
								validation_master_anything(i["type"],"Type",
								alpha_re,3)
				
					err_message["address"] = \
								validation_master_anything(i["secondary_address"],"Address",
								address_re,3)
					add = i["secondary_address"]
			else:
				err_message["address"] = \
					"Customer latitude,longitude,type,secondary_address is not set!!"

			username = str(co_id)+ data['mobile']

			if "id" in data:
				data['id'] = str(data["id"])
				unique_check = CustomerProfile.objects.filter(~Q(id=data["id"]),\
								Q(mobile=data['mobile']),\
								Q(company_id=co_id))
			else:
				unique_check = CustomerProfile.objects.filter(\
								Q(mobile=data['mobile']),\
								Q(company_id=co_id))

			if unique_check.count() > 0:
				err_message["mobile"] = "Mobile number already exists!!"
			else:
				pass

			if "id" in data:
				data['id'] = str(data["id"])
				unique_check = CustomerProfile.objects.filter(~Q(id=data["id"]),\
								Q(email=data['email']),\
								Q(company_id=co_id))
			else:
				unique_check = CustomerProfile.objects.filter(\
								Q(email=data['email']),\
								Q(company_id=co_id))
				
			if unique_check.count() > 0:
				err_message["email"] = "Email id already exists!!"
			else:
				pass

			if any(err_message.values())==True:
				return Response({
								"success": False,
								"error" : err_message,
								"message" : "Please correct listed errors!!"
							})
			if "id" in data:
				data['id'] = str(data["id"])
				record = CustomerProfile.objects.filter(id=data['id'])
				if record.count() == 0:
					return Response(
					{
						"success": False,
						"message": "Customer data is not valid to update!!"
					})
				else:
					userid = CustomerProfile.objects.filter(id=data['id'])[0].auth_user_id
					check_the_user = User.objects.filter(id=userid).first()
					User.objects.filter(id=userid).update(username=username)
					check_the_user.set_password(data["pass_pin"])
					registration_data["updated_at"] = datetime.now()
					registration_data["is_pos"] = 0
					registration_data["pass_pin"] = data['pass_pin']
					registration_data["name"] = data['name']
					registration_data["company"] = co_id
					registration_data["active_status"] = 1
					registration_data["address1"] = data['address']
					registration_data["address"] = add
					registration_data["mobile"] = data['mobile']
					registration_data["email"] = data['email']
					registration_data["username"] = username

					customer_registration_serializer = \
					CustomerSignUpSerializer(record[0],data=registration_data,partial=True)
					if customer_registration_serializer.is_valid():
						customer_data_save = customer_registration_serializer.save()
					else:
						print("something went wrong!!")
						return Response({
							"success": False, 
							"message": str(customer_registration_serializer.errors),
							})
					return Response({"success" : True,
									"message": "Customer updation api worked well!!"})
					
			else:
				user_already_exist = User.objects.filter(username=username)
				if user_already_exist.count() > 0:
					return Response({"success" : False,
								     "message" : "Username already exist!!"})
				else:
					create_user = User.objects.create_user(
							username=username,
							email=data['email'],
							password=data['pass_pin'],
							is_staff=False,
							is_active=True
							)
					if create_user:
						registration_data["auth_user"] = create_user.id
						registration_data["is_pos"] = 0
						registration_data["username"] = username
						registration_data["pass_pin"] = data['pass_pin']
						registration_data["name"] = data['name']
						registration_data["company"] = co_id
						registration_data["active_status"] = 1
						registration_data["address1"] = data['address']
						registration_data["address"] = add
						registration_data["mobile"] = data['mobile']
						registration_data["email"] = data['email']
						customer_registration_serializer = CustomerSignUpSerializer(data=registration_data)
						if customer_registration_serializer.is_valid():
							customer_data_save = customer_registration_serializer.save()
						else:
							print(customer_registration_serializer.errors)

						return Response({"success" : True,
										 "message" : "Customer creation api worked well!!",
							             })

		except Exception as e:
			print("Product creation/updation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})