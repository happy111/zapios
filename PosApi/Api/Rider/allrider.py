from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from Outlet.models import DeliveryBoy,OutletProfile
from ZapioApi.api_packages import *
from UserRole.models import *
from django.db.models import Q

class RiderList(APIView):
	"""
	listing Of rider POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to listing of rider outletwise.

		Data Post: {
			
			"outlet"     : "1"
		}

		Response: {

			"success" : True,
			"message" : "Rider listing worked well!!",
			"data"    : final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			data["outlet"] = str(data["outlet"])
			err_message = {}
			err_message["outlet"] = \
					validation_master_anything(data["outlet"],
					"Outlet Id",contact_re, 1)
			outlet_record = OutletProfile.objects.filter(id=data['outlet'])
			if outlet_record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Required outlet data is not valid to retrieve!!"
				}
				)
			else:
				alld = ManagerProfile.objects.filter(Q(outlet__contains=[data['outlet']]),
					Q(active_status=1),Q(is_rider=1))
				if alld.count() > 0:
					alldata = []
					for i in alld:
						al = {}
						al['id'] = i.id
						al['name'] = str(i.manager_name) + str(i.last_name)
						al['email'] = i.email
						al['is_assign'] = i.is_assign
						al['mobile'] = i.mobile
						al['outlet'] = OutletProfile.objects.filter(id=data['outlet'])[0].Outletname
						alldata.append(al)
					return Response({
           					 "success":True,
							 "data" : alldata
						})
				else:
					return Response({
           					 "success":True,
							 "message":"No Rider Allow!!",
							 "data" : []
						})
		except Exception as e:
			print("Outletwise category listing Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})