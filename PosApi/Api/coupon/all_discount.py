from rest_framework.views import APIView
from rest_framework.response import Response
from Product.models import ProductCategory, Product_availability, Category_availability, Product,\
Variant,AddonDetails
from ZapioApi.api_packages import *
from django.db.models import Q
from rest_framework_tracking.mixins import LoggingMixin
import datetime
from discount.models import Discount,DiscountReason
from frontApi.coupon.coupon_check import *
from rest_framework.permissions import IsAuthenticated
from Outlet.models import OutletProfile
from UserRole.models import * 

class AllDiscount(LoggingMixin,APIView):
	"""
	All discount list POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used all discount outletwise

		Data Post: {
				"outlet" : 1
			 }

		Response: {
				{
					"status": true,
					"subtotalprice": 1396
				}
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			user = request.user
			c = ManagerProfile.objects.filter(auth_user_id=user.id)
			co_id = c[0].Company_id
			ut = c[0].user_type_id
			result = []
			final_result = []
			final_result1 = []
			today = datetime.datetime.now()
			query = Discount.objects.filter(
							Q(valid_till__gte=today),
							Q(active_status=1))
			if query.count() > 0:
				for i in query:
					q_dict = {}
					if len(i.outlet_id) == 0 or str(data['outlet']) in i.outlet_id:
						if len(i.user_roll) == 0 or str(ut) in i.user_roll:
							q_dict["id"] = i.id
							q_dict["discount_type"] = []
							coupon_dict = {}
							coupon_dict["label"] = i.discount_type
							coupon_dict["key"] = i.discount_type
							coupon_dict["value"] = i.discount_type
							q_dict["discount_type"].append(coupon_dict)
							q_dict["valid_frm"] = i.valid_frm
							q_dict["valid_till"] = i.valid_till
							q_dict["discount_name"] = i.discount_name
							q_dict["is_all_category"] = i.is_all_category
							q_dict["is_all_product"] = i.is_all_product
							q_dict["category_detail"] = []
							pa = i.category_map
							for p in pa:
								query1 = ProductCategory.objects.filter(id=p)
								p_dict = {}
								p_dict["value"] = query1[0].category_name
								p_dict["id"] = query1[0].id
								q_dict["category_detail"].append(p_dict)

							q_dict["product_detail"] = []
							pa = i.product_map
							for p in pa:
								query1 = Product.objects.filter(id=p)
								p_dict = {}
								p_dict["value"] = query1[0].product_name
								p_dict["id"] = query1[0].id
								q_dict["product_detail"].append(p_dict)

							q_dict["outlet_detail"] = []
							pa = i.outlet_id
							for p in pa:
								query1 = OutletProfile.objects.filter(id=p)
								p_dict = {}
								p_dict["value"] = query1[0].Outletname
								p_dict["id"] = query1[0].id
								q_dict["outlet_detail"].append(p_dict)

							q_dict["flat_discount"] = i.flat_discount
							q_dict["flat_percentage"] = i.flat_percentage
							q_dict["is_min_shop"] = i.is_min_shop
							q_dict["is_reason_required"] = i.is_reason_required
							q_dict['reason']=[]

							if i.is_reason_required == True:
								allreason = DiscountReason.objects.filter(active_status=1,Company_id=co_id)
								for k in allreason:
									re = {}
									re['id'] = k.id
									re['reason'] = k.reason
									q_dict['reason'].append(re)
							else:
								pass
							q_dict["min_shoping"] = i.min_shoping
							q_dict["max_shoping"] = i.max_shoping
							q_dict["active_status"] = i.active_status
							final_result1.append(q_dict)
			if len(final_result1) > 0:
				return Response({
							"success": True, 
							"data": final_result1,
							})
			else:
				return Response({
							"success": True, 
							"message": "No Discount data found!!"
							})
		except Exception as e:
			print("CoupondataApiException")
			print(e)
			return Response({"status": False, 
							"message": "Bad Request", 
							 "error": str(e)})