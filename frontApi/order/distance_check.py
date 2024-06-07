from rest_framework.views import APIView
from rest_framework.response import Response
from .error_radious_check import *


class DistanceCheck(APIView):
	"""
	Distance Check POST API

		Authentication Required		: No
		Service Usage & Description	: This Api is used to check the delivery radious.

		Data Post: {
			"lat"	:	"41.90278349999999",
			"long"	:	"12.4963655",
			"shop_id" : "20"
		}

		Response: {

			"success": true,
			"message": "We deliver at your place!!"
		}

	"""
	def post(self, request, format=None):
		try:
			data = request.data
			if 'type' in data:
				return Response({
								"success":True,
								"message":"We deliver at your place!!"
								})

			
			check_address_circle = check_circle(data)
			if check_address_circle != None:
				return Response(check_address_circle)
			else:
				return Response({
								"success":True,
								"message":"We deliver at your place!!"
								})
		except Exception as e:
			print(e)
			return Response({"success": False,
							"message":"Distance Check api stucked into exception!!"})