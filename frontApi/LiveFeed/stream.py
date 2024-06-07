from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
import re
from ZapioApi.api_packages import *


class OutletCam(APIView):
	"""
	Outletwise Cam Feed POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used to get all information reagrding cam feed
		outletwise.

		Data Post: {

			"outlet_id" : 18
		}

		Response: {

			"success": True,
			"message" : "API worked well!!",
			"data"   : result
		}

	"""
	def post(self, request, format=None):
		try:
			data = request.data
			err_message = {}
			err_message["outlet_id"] = \
						validation_master_anything(str(data["outlet_id"]),
						"Outlet Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = OutletProfile.objects.filter(id=data["outlet_id"],active_status=1)
			if record.count() == 0:
				err_message["outlet"] = "Outlet is not active!!"
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			else:
				if record[0].is_open == 1:
					pass
				else:
					err_message["outlet"] = "Outlet closed!!"
					return Response({
							"success": False,
							"error" : err_message,
							"message" : "Please correct listed errors!!"
						})
				result = []
				data_dict = {}
				data_dict["id"] = record[0].id
				data_dict["Outlet"] = record[0].Outletname
				data_dict["cam_url"] = record[0].cam_url
				result.append(data_dict)
				return Response({
					"success": True,
					"message" : "API worked well!!",
					"data"   : result
					})			
		except Exception as e:
			print("Cam Feed Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})
