from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .available import POSProductAvailableList



class OutletProductlist(APIView):
	"""
	Outletwise Product listing POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to retrieve listing of Products associated with outlet.

		Data Post: {
			
			"outlet"     : "1"
		}

		Response: {

			"success" : True,
			"message" : "Outletwise product listing worked well!!",
			"data"    : final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			user = request.user
			pro_check = POSProductAvailableList(data,user)
			if pro_check !=None:
				return Response(pro_check) 
			else:
				return Response ({
           					 "success":True,
							 "message":"No Data Found!!",
							 "data":[]
						})
		except Exception as e:
			print("Outletwise product listing Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})