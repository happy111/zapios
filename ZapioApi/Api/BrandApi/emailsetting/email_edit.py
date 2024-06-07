from rest_framework.views import APIView
from rest_framework.response import Response
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime
import os
from django.db.models import Q
from Configuration.models import EmailSetting
from rest_framework import serializers

def null_converter(d):
	if d == None or d == "null" or d == "undefined":
		d = ""
	else:
		pass
	return d


class EmailSerializer(serializers.ModelSerializer):

	class Meta:
		model = EmailSetting
		fields = '__all__'
class EmailEdit(APIView):

	"""
	Configuration Edit POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to edit the Email Configuration details.

		Data Post: {
		    "title"                               : "#ffd600",
    		"content"                             : "#000",
    		"dis_content"                         : "#000",
  			"thank"                               : "1",
  			"image"								  : a.jpg,
  			"id"								  : 1,
  			"coupon"                              : ""
		}

		Response: {

			"success"  : True, 
			"message"  : "Theme api worked well!!",
			"data"     : final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			user = request.user
			err_message = {}
			data["title"] =  null_converter(data["title"])
			data["content"] = null_converter(data["content"])
			data["thank"] =  null_converter(data["thank"])
			data["dis_content"] = null_converter(data["dis_content"])
			data["coupon"] = null_converter(data["coupon"])
			err_message["title"] = \
							validation_master_anything(data["title"],"Title",
								username_re,1)	
			err_message["content"] = \
							validation_master_anything(data["content"],"Content",
								description_re,1)	
			err_message["subcontent"] = \
							validation_master_anything(data["thank"],"subcontent",
								description_re,1)	
	
			err_message["dis_content"] =  \
							only_required(str(data["dis_content"]), "Discount Content")

			err_message["coupon"] = \
							validate_anything(data["coupon"],contact_re,
								zero__re,1,"Coupon")	

			if type(data["image"]) != str:
				im_name_path =  data["image"].file.name
				im_size = os.stat(im_name_path).st_size
				if im_size > 500*1024:
					err_message["image_size"] = "Email image can'nt excced the size more than 500kb!!"
				else:
					pass
			else:
				data["image"] = None

			print(err_message)	

			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = EmailSetting.objects.filter(id=data['id'])
			if record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Email data is not valid to update!!"
				}
				)
			else:
				if data["image"] == None:
					data["image"] = record[0].image
				else:
					pass
				data["updated_at"] = datetime.now()
				email_serializer = \
					EmailSerializer(record[0],data=data,partial=True)
				if email_serializer.is_valid():
					data_info = email_serializer.save()
					return Response({
						"status": True, 
						"message": "Email Configuration is updated successfully!!",
						"data": email_serializer.data
						})
				else:
					print("something went wrong!!")
					return Response({
						"status": False, 
						"message": str(email_serializer.errors),
						})
		except Exception as e:
			print("Email Configuration retrieval Api Stucked into exception!!")
			print(e)
			return Response({
							"status": False, 
							"message": "Error happened!!", 
							"errors": str(e)})
		except Exception as e:
			print("Email Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})