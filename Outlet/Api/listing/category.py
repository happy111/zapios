from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from Product.models import Product, Product_availability, ProductCategory, Category_availability
from Outlet.models import OutletProfile



class Categorylist(APIView):
	"""
	Category listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to get listing of Categories within outlet.

	"""
	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			user_id = request.user.id
			cat_q = Category_availability.objects.filter(outlet__auth_user=user_id)
			outlet_id = OutletProfile.objects.get(auth_user=user_id)
			company_id = OutletProfile.objects.filter(auth_user=user_id)[0].Company_id
			category = ProductCategory.objects.filter(active_status=1,Company=company_id)
			final_result = []
			if cat_q.count() == 0:
				create_cat_avail = \
				Category_availability.objects.create(outlet=outlet_id,available_cat=[])
				for p in category:
					cat_dict = {}
					cat_dict["id"] = p.id
					cat_dict["category_name"] = p.category_name
					cat_dict["category_code"] = p.category_code
					cat_dict["priority"] = p.priority
					cat_dict["is_available"] = False
					final_result.append(cat_dict)
			else:
				cat_ids = cat_q[0].available_cat
				if len(cat_ids) != 0:
					for p in category:
						cat_dict = {}
						cat_dict["id"] = p.id
						cat_dict["category_name"] = p.category_name
						cat_dict["category_code"] = p.category_code
						cat_dict["priority"] = p.priority
						if str(p.id) not in cat_ids:
							cat_dict["is_available"] = False
						else:
							cat_dict["is_available"] = True
						final_result.append(cat_dict)
				else:
					for p in category:
						cat_dict = {}
						cat_dict["id"] = p.id
						cat_dict["category_name"] = p.category_name
						cat_dict["category_code"] = p.category_code
						cat_dict["priority"] = p.priority
						cat_dict["is_available"] = False
						final_result.append(cat_dict)
			return Response({
							"success":True,
							"message":"Outletwise category listing worked well!!",
							"data":final_result
							 })
		except Exception as e:
			print("Outletwise category listing Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})