import os
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
import json
from rest_framework.authtoken.models import Token
from django.db.models import Q

#Serializer for api
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from pyfcm import FCMNotification
from rest_framework.views import APIView

# push_api_key = "AAAAlS6ByWM:APA91bFnqJC51eYjEukPj5kUbsPTUlEh9sawI6-kmeH8cKgjlVNjPeza1vjj8BDMnaIz9mW8GdmmebnlCsUSa1YxNBfYay0tT4DCHieYCNtBx4vl3OFS7KU5eaAYutUpb55YZIvVnHcV"

push_api_key = "AAAAwymZArg:APA91bEsEQPNg1WF2Mzhdo78-QZv2aVaslzMw_B9zcvo3ryT7ekXBSGx1Hy-0l4EnRrX4WVF7XS9ydyQMtulkOttRBTDJzK4cEFMsalnpfad0ZYFctk1z6Lm7TutCU_I-v4_6iVKsaxt"


class PushHome(APIView):

	"""
	Variant listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of devices.
	"""
	# permission_classes = (IsAuthenticated,)

	# serializer_class = DeviceSerializer

	def post(self, request, format=None):
		try:
			data = request.data
			# user_key = "dkZpR-w_kUk:APA91bG4ARB55hGSkkBJT312jpM1M8DOgzrWUjwPPikCXTQy6pr85TwOnc1_UCotuFo4WCTlWg8VM0OkLiWyAtkURD1nP1Y3LP0GZHwlKmZIG6KbGf_V-3oArWBQq30VvHMqD6Poc_JD"
			user_key = data["token"]
			push_service = FCMNotification(api_key=push_api_key)
			# user_key = \
			# "dJjTSTzf7AA:APA91bHyL_6keukzHMGADdLLCmDKAtX5JNb2_R64PAJrHgY4GwhbKFp1hINlV4TquyttlaUz94KRANN71hq-SZ6wdQ8INxF-4QHIxYFReaGJ99kCR_jLEiix-bzJx7GGy1I-F383KU0J"
			# # Your api-key can be gotten from:  https://console.firebase.google.com/project/<project-name>/settings/cloudmessaging

			# user_key = userkey
			registration_id = user_key
			message_title = "Browser Push Notification Test"
			message_body = "Hi there.....This is test notification.You can have a look over it!!"
			result = \
			push_service.notify_single_device(registration_id=user_key, \
				message_title=message_title, message_body=message_body)

			print (result)
			return Response({"status":True,
				"result" : result
							})
		except Exception as e:
			print(e)
			return Response({"success": False,
							"message":"Device api stucked into exception!!"})



