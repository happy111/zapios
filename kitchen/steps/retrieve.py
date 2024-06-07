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
from Product.models import ProductCategory
from kitchen.models import StepToprocess
from zapio.settings import Media_Path


class PreparationStepRetrieval(APIView):
	"""
	Product Preparation steps retrieval POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of steps data associated with product.
		Instruction                 : Send v_id as null if there is no v_id associated with product.

		Data Post: {
			"p_id"                   : "3",
			"v_id"                 	 : "43"
		}

		Response: {

			"success": True, 
			"message": "Preparation Steps retrieval api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			data["p_id"] = str(data["p_id"])
			err_message = {}
			err_message["p_id"] = \
					validation_master_anything(data["p_id"],
					"Product Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			auth_id = request.user.id
			outlet_id = OutletProfile.objects.filter(auth_user=auth_id)
			c_id = outlet_id[0].Company_id
			if data["v_id"] !=None:
				record = StepToprocess.objects.filter(company_id=c_id,product=data["p_id"],\
										varient=data["v_id"],active_status=1).order_by('step')
			else:
				record = StepToprocess.objects.filter(company_id=c_id,product=data["p_id"],\
													active_status=1).order_by('step')
			if record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Required Preparation Steps data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				for q in record:
					q_dict = {}
					q_dict["id"] = q.id
					q_dict["p_id"] = q.product_id
					q_dict["step_no"] = q.step
					q_dict["process"] = q.process
					if data["v_id"] !="N/A":
						q_dict["v_id"] = q.varient_id
					else:
						q_dict["v_id"] = None
					q_dict["description"] = q.description
					q_dict["time_of_process"] = q.time_of_process
					q_dict["image"] = q.image
					if q.image != None and q.image != "":
						q_dict["image"] = Media_Path+str(q.image)
					else:
						q_dict["image"] = None
					q_dict["ingredient_description"] = q.ingredient
					final_result.append(q_dict)
			return Response({
						"success": True, 
						"message": "Preparation Steps retrieval api worked well!!",
						"data": final_result,
						})
		except Exception as e:
			print("Preparation Steps retrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})
