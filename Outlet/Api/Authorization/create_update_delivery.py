from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile, DeliveryBoy
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime
import os
from django.db.models import Q
from Outlet.Api.serializers.deliveryboy_serializers import DeliverySerializer
from rest_framework import serializers
from rest_framework.generics import ListAPIView

class DeliveryBoyRegistration(APIView):
	"""
	Delivery Boy Creation POST API
		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create new DeliveryBoy.
		Data Post: {
			"name"			               : "umesh",
			"email"		                   : "umeshsamal3@gmail.com",
			"address" 					   : "sunlight colony ashram",
			"mobile" 	    			   : "8750477098",
			"profile_pic"                  : "a/jpg", (type:image)
		}
		Response: {
			"success": True,
			"message": "Delivery boy is registered successfully under your brand!!"
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			err_message = {}
			data = request.data
			print("SSSSSSSSSSSSSSSSSSSSSSSSSSs",data)
			auth_id = request.user.id
			data['Outlet'] = OutletProfile.objects.filter(auth_user=auth_id).first().id
			if "profile_pic" in data:
				pass
			else:
				data["profile_pic"] = None
			err_message["name"] = \
					validation_master_anything(data["name"],
					"Name",username_re, 3)
			err_message["email"] = \
					validation_master_anything(data["email"],
					"Email",email_re, 3)
			err_message["address"] = \
					validation_master_anything(data["address"],
					"Address", address_re, 3)
			err_message["mobile"] = \
					validation_master_exact(data["mobile"], 
						"Mobile No.",contact_re, 10)
			if "id" in data:
				unique_check = DeliveryBoy.objects.filter(~Q(id=data["id"]),\
								Q(mobile__iexact=data["mobile"]))
			else:
				unique_check = DeliveryBoy.objects.filter(Q(mobile__iexact=data["mobile"]))
			if unique_check.count() != 0:
				err_message["unique_check"] = "Mobile number already exists!!"
			else:
				pass
			if "id" in data:
				unique_check = DeliveryBoy.objects.filter(~Q(id=data["id"]),\
								Q(email__iexact=data["email"]))
			else:
				unique_check = DeliveryBoy.objects.filter(Q(email__iexact=data["email"]))
			if unique_check.count() != 0:
				err_message["unique_check"] = "Email ID already exists!!"
			else:
				pass
			if type(data["profile_pic"]) != str:
				im_name_path =  data["profile_pic"].file.name
				im_size = os.stat(im_name_path).st_size
				if im_size > 170*1024:
					err_message["image_size"] = "Profile Picture can'nt excced the size more than 170kb!!"
			else:
				data["profile_pic"] = None

			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})

			data["active_status"] = 1
			print("NNNNNNNNNNNNNNNNNNN",data)
			if "id" in data:
				Delivery_record = DeliveryBoy.objects.filter(id=data['id'])
				if Delivery_record.count() == 0:
					return Response(
					{
						"success": False,
						"message": "Delivery Boy data is not valid to update!!"
					}
					)
				else:
					if data["profile_pic"] != None:
						pass
					else:
						data["profile_pic"] = Delivery_record[0].profile_pic
					data["updated_at"] = datetime.now()
					Delivery_serializer = \
					DeliverySerializer(Delivery_record[0],data=data,partial=True)
					if Delivery_serializer.is_valid():
						s=Delivery_serializer.save()
						return Response({
								"success": True, 
								"message": "Delivery Boy updation api worked well!!",
								"data": Delivery_serializer.data,
								})
					else:
						print("something went wrong!!")
						return Response({
							"success": False, 
							"message": str(Delivery_serializer.errors),
							})
			else:
				Delivery_Serializer = DeliverySerializer(data=data)
				if Delivery_Serializer.is_valid():
					data_info = Delivery_Serializer.save()
					return Response({
								"success": True, 
								"message": "Delivery Boy creation api worked well!!",
								"data": Delivery_Serializer.data,
								})
				else:
					print("something went wrong!!")
					return Response({
						"success": False, 
						"message": str(Delivery_Serializer.errors),
						})
		except Exception as e:
				print(str(e))
				return Response({"success": False, 
								"message": "Error happened!!", 
								"errors": str(e)})


def addr_set():
	domain_name = "http://zapio-admin.com:8080/media/"
	return domain_name

class DeliveryBoyListing(APIView):
	"""
	Delivery Boy Listing GET API
		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of Delivery Boy data within brand.
	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		user = self.request.user.id
		delivery_boy_data = OutletProfile.objects.filter(auth_user=user).first().id
		if delivery_boy_data:
			delivery_data = DeliveryBoy.objects.filter(Outlet=delivery_boy_data)
			pro_data =[]
			for i in delivery_data:
				p_list ={}
				p_list['id'] = i.id
				p_list['name'] = i.name
				p_list['email'] = i.email
				p_list['mobile'] = i.mobile
				p_list['address'] = i.address
				p_list['profile_pic'] = str(i.profile_pic)
				p_list['active_status'] = i.active_status
				domain_name = addr_set()
				if i.profile_pic != "" and i.profile_pic != None:
					full_path = domain_name + str(i.profile_pic)
					p_list['profile_pic'] = full_path
				pro_data.append(p_list)
			return Response({"status":True,
							"data":pro_data})




class DeliveryTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = DeliveryBoy
		fields = '__all__'

class DeliveryAction(APIView):
	"""
	Delivery Action POST API
		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to activate or deactivate Delivery Boy.
		Data Post: {
			"id"                   		: "2",
			"active_status"             : "0"
		}

		Response: {

			"success": True, 
			"message": "Food Type is deactivated now!!",
			"data": final_result
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
						"Delivery Boy Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = DeliveryBoy.objects.filter(id=data["id"])
			if record.count() != 0:
				data["updated_at"] = datetime.now()
				if data["active_status"] == "true":
					info_msg = "Delivery Boy is activated successfully!!"
				else:
					info_msg = "Delivery Boy is deactivated successfully!!"
				serializer = \
				DeliveryTypeSerializer(record[0],data=data,partial=True)
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
						"message": "Delivery Boy id is not valid to update!!"
					}
					)
			final_result = []
			final_result.append(serializer.data)
			return Response({
						"success": True, 
						"message": info_msg,
						"data": final_result,
						})
		except Exception as e:
			print("Delivery Boy action Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})


class DeliveryActiveListing(ListAPIView):
	"""
	Active Delivery BOy listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of active Delivery boy.
	"""
	permission_classes = (IsAuthenticated,)

	def get_queryset(self):
		user = self.request.user

		queryset = DeliveryBoy.objects.filter(active_status=1).order_by('-created_at')
		return queryset.filter(Outlet__auth_user=user.id)

	def list(self, request):
		queryset = self.get_queryset()
		serializer = DeliveryTypeSerializer(queryset, many=True)
		response_list = serializer.data 
		return Response({
					"success": True,
					"data" : response_list,
					"message" : "Delivery Boy API worked well!!"})







class DeliveryBoyRetrieval(APIView):
	"""
	Delivery Boy retrieval POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of Retrievw data within outlet.

		Data Post: {
			"id"                   : "3"
		}

		Response: {

			"success": True, 
			"message": "Delivery BOy retrieval api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			data["id"] = str(data["id"])
			err_message = {}
			err_message["id"] = \
					validation_master_anything(data["id"],
					"Delivery Boy Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			delivery_record = DeliveryBoy.objects.filter(id=data['id'])
			if delivery_record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Required Delivery Boy data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				q_dict = {}
				q_dict["id"] = delivery_record[0].id
				q_dict["name"] = delivery_record[0].name
				q_dict["email"] = delivery_record[0].email
				q_dict["address"] = delivery_record[0].address
				q_dict["mobile"] = delivery_record[0].mobile
				q_dict["active_status"] = delivery_record[0].active_status
				q_dict['profile_pic'] = str(delivery_record[0].profile_pic)
				domain_name = addr_set()
				if delivery_record[0].profile_pic != "" and delivery_record[0].profile_pic != None:
					full_path = domain_name + str(delivery_record[0].profile_pic)
					q_dict['profile_pic'] = full_path
				final_result.append(q_dict)
			return Response({
						"success": True, 
						"message": "Delivery Boy retrieval api worked well!!",
						"data": final_result,
						})
		except Exception as e:
			print("Delivery Boy Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})



