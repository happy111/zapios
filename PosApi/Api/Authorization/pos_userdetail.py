from datetime import datetime
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_tracking.mixins import LoggingMixin
from UserRole.models import ManagerProfile,UserType
from Brands.models import Company


def addr_set():
	domain_name = "https://zapio-admin.com/media/"
	return domain_name



class PosUserDetail(APIView):

	"""
	Methods Allowed: get

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to list detail pos user.

	"""

	permission_classes = (IsAuthenticated,)
	def get(self, request):
		try:
			data = request.data
			user = request.user
			alldata = ManagerProfile.objects.filter(auth_user_id=user.id)
			if alldata.count() > 0:
				res = {}
				res['username'] = alldata[0].username
				res['manager_name'] = alldata[0].manager_name
				res['email'] = alldata[0].email
				res['active_status'] = alldata[0].active_status
				res['password'] = alldata[0].password
				res['mobile'] = alldata[0].mobile
				full_path = addr_set()
				imgp = alldata[0].manager_pic
				if imgp != None and imgp != "":
					res['profile_pic'] = full_path+str(alldata[0].manager_pic)
				else:
					res['profile_pic'] = None
			else:
				pass
			return Response({"status":True,
							 "data" : res
							})
		except Exception as e:
			print("ConfigurationDataApiException")
			print(e)
			return Response({"success": False, 
							"message": "Bad Request", 
							"error": str(e)})
