from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
import re
from ZapioApi.api_packages import *


class ALLOutlets(APIView):
	"""
	Active Outlets Stream listing GET API

		Authentication Required		: No
		Service Usage & Description	: This Api is used to get listing of Active Outlets along with cam url.

	"""
	def get(self, request, format=None):
		try:
			check_company = OutletProfile.objects.filter(Company_id=1,active_status=1).order_by('priority')
			if check_company.count()==0:
				return Response(
					{
						"success": False,
	 					"message": "This Company is not active yet !!"
					}
					) 
			else:
				final_result = []
				for outlet in check_company:
					out_dict = {}
					row_id  = outlet.id
					if row_id != 35 and row_id != 34 and row_id != 33:
						out_dict["id"] = outlet.id
						out_dict["Outletname"] = outlet.Outletname
						if row_id != 26 and row_id != 32 and row_id != 36:
							out_dict["is_open"] = outlet.is_pos_open
							out_dict["cam_url"] = outlet.cam_url
						else:
							out_dict["is_open"] =  False
							out_dict["cam_url"] = None
						out_dict["priority"] = outlet.priority
						final_result.append(out_dict)
					else:
						pass
			return Response({
							"success":True,
							"message":"Active Outlets stream listing worked well!!",
							"data":final_result
							 })
		except Exception as e:
			print("Active Outlets stream listing Api Stucked into exception!!")
			print(e)
			return Response({
					"success": False, 
					"message": "Error happened!!", 
					"errors": str(e)
					})
