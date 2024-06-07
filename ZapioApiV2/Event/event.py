# import os
# import re
# import json
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from ZapioApi.api_packages import *
# from datetime import datetime
# from django.db.models import Q
# from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user
# from rest_framework import serializers
# from Event.models import Event

# class EventSerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = Event
# 		fields = '__all__'

# class EventCreate(APIView):

# 	"""
# 	Event Creation & Updation POST API

# 		Authentication Required		: Yes
# 		Service Usage & Description	: This Api is used to create & update Event
# 		Data Post: {
# 			"id"                       : "1"(Send this key in update record case,else it is not required!!)
# 			"event_type"		       :  "1",
# 			"secondary_event_type"     :  "1",
# 			"event_time"			   :  "",



# 		}
# 		Response: {

# 			"success": True, 
# 			"message": "Event type creation/updation api worked well!!",
# 			"data": final_result
# 		}

# 	"""
# 	permission_classes = (IsAuthenticated,)
# 	def post(self, request, format=None):
# 		try:
# 			from Brands.models import Company
# 			mutable = request.POST._mutable
# 			request.POST._mutable = True
# 			data = request.data
# 			user = request.user.id
# 			cid = get_user(user)
# 			data['company'] = cid
			
# 			err_message = {}
# 			# err_message["event_type"] = only_required(data["event_type"],"Event Type")
# 			# if any(err_message.values())==True:
# 			# 	return Response({
# 			# 		"success" : False,
# 			# 		"error"   : err_message,
# 			# 		"message" : "Please correct listed errors!!"
# 			# 		})
# 			# if "id" in data:
# 			# 	unique_check = PrimaryEventType.objects.filter(~Q(id=data["id"]),\
# 			# 					Q(event_type=data["event_type"]),Q(company_id=cid))
# 			# else:
# 			# 	unique_check = PrimaryEventType.objects.filter(Q(event_type=data["event_type"]),Q(company_id=cid))
# 			# if unique_check.count() != 0:
# 			# 	err_message["unique_check"] = "Event type with this name already exists!!"
# 			# else:
# 			# 	pass
# 			# if any(err_message.values())==True:
# 			# 	return Response({
# 			# 		"success": False,
# 			# 		"error" : err_message,
# 			# 		"message" : "Please correct listed errors!!"
# 			# 		})
# 			data["active_status"] = 1
# 			if "id" in data:
# 				event_record = Event.objects.filter(id=data['id'])
# 				if event_record.count() == 0:
# 					return Response(
# 					{
# 						"success": False,
# 	 					"message": "Event type data is not valid to update!!"
# 					}
# 					)
# 				else:
# 					data["updated_at"] = datetime.now()
# 					event_serializer = EventSerializer(event_record[0],data=data,partial=True)
# 					if event_serializer.is_valid():
# 						data_info = event_serializer.save()
# 						info_msg = "Event type is updated successfully!!"
# 						return Response({
# 							"success": True, 
# 							"message": info_msg
# 						})
# 					else:
# 						print("something went wrong!!",event_serializer.errors)
# 						return Response({
# 							"success": False, 
# 							"message": str(event_serializer.errors),
# 							})
# 			else:
# 				event_serializer = EventSerializer(data=data)
# 				if event_serializer.is_valid():
# 					data_info = event_serializer.save()
# 					info_msg = "Event type is created successfully!!"
# 				else:
# 					print("something went wrong!!",event_serializer.errors)
# 					return Response({
# 						"success": False, 
# 						"message": str(event_serializer.errors),
# 						})
# 			return Response({
# 						"success": True, 
# 						"message": info_msg
# 						})
# 		except Exception as e:
# 			print("Event type creation/updation Api Stucked into exception!!")
# 			print(e)
# 			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})