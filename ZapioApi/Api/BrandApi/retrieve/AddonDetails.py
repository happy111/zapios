from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
import re
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
import json
from datetime import datetime

#Serializer for api
from rest_framework import serializers
from Product.models import AddonDetails

class AddonDetailsSerializer(serializers.ModelSerializer):
	class Meta:
		model = AddonDetails
		fields = '__all__'


class AddonDetailsRetrieval(APIView):
	"""
	AddonDetails retrieval POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of AddonDetails data.

		Data Post: {
			"id"                   : "1"
		}

		Response: {

			"success": True, 
			"message": "AddonDetails retrieval api worked well!!",
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
					"AddonDetails Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = AddonDetails.objects.filter(id=data['id'])
			if record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Provided AddonDetails data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				q_dict = {}
				q_dict["id"] = record[0].id
				q_dict["priority"] = record[0].priority

				q_dict["addon_gr_name"] = record[0].addon_gr_name
				q_dict["addon_gr_name_details"] = []
				addon_gr_name_dict = {}
				if record[0].product_variant != None:
					addon_gr_name_dict["label"] = \
					record[0].addon_gr_name+' | '+record[0].product_variant.variant
				else:
					addon_gr_name_dict["label"] = \
					record[0].addon_gr_name
				addon_gr_name_dict["key"] = record[0].id
				addon_gr_name_dict["value"] = record[0].id
				q_dict["addon_gr_name_details"].append(addon_gr_name_dict)
				q_dict["min_addons"] = record[0].min_addons
				q_dict["max_addons"] = record[0].max_addons
				q_dict["description"] = record[0].description
				q_dict["product_variant_id"] = record[0].product_variant_id
				if q_dict["product_variant_id"] != None:
					q_dict["product_variant"] = record[0].product_variant.variant
				else:
					q_dict["product_variant"] = None
				q_dict["associated_addons"] = record[0].associated_addons
				q_dict["associated_addons_details"] = []
				if q_dict["associated_addons"] != None:
					if len(q_dict["associated_addons"]) != 0:
						for i in q_dict["associated_addons"]:
							if 'addon_name' in i and 'price' in i:
								associated_addons_dict = {}
								associated_addons_dict["name"] = i["addon_name"]
								associated_addons_dict["price"] = i["price"]
								q_dict["associated_addons_details"].append(associated_addons_dict)
							else:
								pass
					else:
						pass
				else:
					pass
				q_dict["active_status"] = record[0].active_status
				q_dict["created_at"] = record[0].created_at
				q_dict["updated_at"] = record[0].updated_at
				final_result.append(q_dict)
			return Response({
						"success": True, 
						"message": "AddonDetails retrieval api worked well!!",
						"data": final_result,
						})
		except Exception as e:
			print("AddonDetails retrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})