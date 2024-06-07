from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from Product.models import Product, Product_availability
from Outlet.models import OutletProfile



class Productlist(APIView):
	"""
	Product listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to get listing of products within outlet.

	"""
	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			user_id = request.user.id
			product_q = Product_availability.objects.filter(outlet__auth_user=user_id)
			company_id = OutletProfile.objects.filter(auth_user=user_id)[0].Company_id
			outlet_id = OutletProfile.objects.get(auth_user=user_id)
			product = Product.objects.filter(active_status=1,Company=company_id)
			final_result = []
			if product_q.count() == 0:
				for i in product:
					product_dict = {}
					product_dict["id"] = i.id
					product_dict["product_name"] = i.product_name
					product_dict["is_available"] = False
					product_dict["food_type"] = i.food_type.food_type
					final_result.append(product_dict)	
			else:
				product_ids = product_q[0].available_product
				if len(product_ids) != 0:
					for p in product:
						product_dict = {}
						product_dict["id"] = p.id
						product_dict["product_name"] = p.product_name
						product_dict["food_type"] = p.food_type.food_type
						if str(p.id) not in product_ids:
							product_dict["is_available"] = False
						else:
							product_dict["is_available"] = True
						final_result.append(product_dict)
				else:
					for i in product:
						product_dict = {}
						product_dict["id"] = i.id
						product_dict["product_name"] = i.product_name
						product_dict["is_available"] = False
						product_dict["food_type"] = i.food_type.food_type
						final_result.append(product_dict)
			return Response({
							"success":True,
							"message":"Outletwise product listing worked well!!",
							"data":final_result
							 })
		except Exception as e:
			print("Outletwise product listing Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})