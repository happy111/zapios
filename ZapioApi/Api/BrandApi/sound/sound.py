from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from ZapioApi.Api.BrandApi.profile.profile import CompanySerializer
from Brands.models import Company
from datetime import datetime
#Serializer for api
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user


class SoundStatus(APIView):
	"""
	Sound Effect listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of sound effect status within brand.
	"""
	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			user = self.request.user.id
			Company_id = get_user(user)
			company_data = Company.objects.filter(id=Company_id)
			if company_data.count()!=0:
				final_result = []
				i = company_data[0]
				d_dict = {}
				d_dict["is_sound"] = i.is_sound
				final_result.append(d_dict)
				return Response({"status":True,
								"data":final_result})
			else:
				return Response({"status":True,
								"data":[]
								})
		except Exception as e:
			print(e)
			return Response({"status":False,
				             "message":str(e),
				             })


class ChangeSound(APIView):
	"""
	Sound Status Change POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to change status of sound effect.

		Data Post: {
			"is_sound"             		:  True
		}

		Response: {

			"success": True, 
			"message": "Sound Effect is enabled now!!"
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			err_message = {}
			if data["is_sound"] == True:
				pass
			elif data["is_sound"] == False:
				pass
			else:
				err_message["is_sound"] = "Is Sound status data is not valid!!"
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			auth_id = request.user.id
			Company_id = get_user(auth_id)
			record = Company.objects.filter(id=Company_id)
			if record.count() != 0:
				data["updated_at"] = datetime.now()
				if data["is_sound"] == True:
					info_msg = "Sound Effect is enabled now!!"
				else:
					info_msg = "Sound Effect is disabled now!!"
				serializer = \
				CompanySerializer(record[0],data=data,partial=True)
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
						"message": "Is Sound data is not valid to update!!"
					}
					)
			return Response({
						"success": True, 
						"message": info_msg
						})
		except Exception as e:
			print("Is Sound status change Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})