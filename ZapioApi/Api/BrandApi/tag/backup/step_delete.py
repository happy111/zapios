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
from kitchen.models import StepToprocess, ProcessTrack
from Product.models import Product,Variant
from django.db.models import Max,Min


class StepProcessDelete(APIView):

	"""
	Step process Delete POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to delete step process and sync remaining ones accordingly.

		Data Post: {
			"id"                   : "21"
		}

		Response: {

			"success": True, 
			"message": "Step deleted successfully!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			data["id"] = str(data["id"])
			err_message = {}
			err_message["id"] = \
					validation_master_anything(data["id"],
					"Step Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			process_data = StepToprocess.objects.filter(id=data['id'])
			if process_data.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Required Process data is not valid to retrieve!!"
				}
				)	
			else:
				p_id = process_data[0].product_id
				v_id = process_data[0].varient_id
				track_delete = ProcessTrack.objects.filter(Step=data['id']).delete()
				data_delete = process_data.delete()
				q = StepToprocess.objects.filter(product=p_id)
				if v_id == None:
					pass
				else:
					q = q.filter(varient=v_id)
				q_count = q.count()
				q = q.order_by('step')
				counter = 1
				for r in q:
					step_query = StepToprocess.objects.filter(id=r.id).update(step=counter)
					counter = counter+1
			return Response({
						"success": True, 
						"message": "Step deleted successfully!!",
						})
		except Exception as e:
				print("Step process Delete Api Stucked into exception!!")
				print(e)
				return Response({"success": False, 
								"message": "Error happened!!", 
								"errors": str(e)})
