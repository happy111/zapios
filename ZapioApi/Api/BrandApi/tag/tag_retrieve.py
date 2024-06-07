from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime

#Serializer for api
from rest_framework import serializers
from Product.models import Tag,Product


def addr_set():
	domain_name = "https://zapio-admin.com/media/"
	return domain_name
	
class TagRetrieve(APIView):

	"""
	Tag POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used for retrieval of tag data.

		Data Post: {
			"id"                   : "1"
		}

		Response: {

			"success": True, 
			"message": "Tag retrieval api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			err_message = {}

			err_message["id"] = \
					validation_master_anything(data["id"],
					"Tag Id",contact_re, 1)

			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})

			record = Tag.objects.filter(id=data['id'])
			if record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Provided Tag data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				q_dict = {}
				q_dict["id"] = record[0].id
				q_dict["tag_name"] = record[0].tag_name
				# q_dict["food_detail"] = []
				# pro_dict = {}
				# pro_dict["label"] = record[0].food_type.food_type
				# pro_dict["key"] = record[0].food_type_id
				# pro_dict["value"] = record[0].food_type_id
				# q_dict["food_detail"].append(pro_dict)

				img = record[0].tag_image
				domain_name = addr_set()
				if img != "" and img != None and img != "null":
					full_path = domain_name + str(img)
					q_dict['tag_image'] = full_path
				else:
					q_dict['tag_image'] = ''

				q_dict["active_status"] = record[0].active_status
				q_dict["created_at"] = record[0].created_at
				q_dict["updated_at"] = record[0].updated_at



				final_result.append(q_dict)
			return Response({
						"success": True, 
						"message": "Tag retrieval api worked well!!",
						"data": final_result,
						})
		except Exception as e:
			print("Tag retrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})