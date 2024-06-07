# import re
# import json
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from Outlet.models import OutletProfile
# from django.contrib.auth.models import User
# from rest_framework.permissions import IsAuthenticated
# from ZapioApi.api_packages import *
# from datetime import datetime

# from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user
# from rest_framework import serializers
# from Product.models import ProductCategory,ProductsubCategory,Product
# from django.db.models import Q

# class ProductCategorySerializer(serializers.ModelSerializer):
# 	class Meta:
# 		model = ProductCategory
# 		fields = '__all__'



# class CategoryView(APIView):
# 	"""
# 	Category view POST API

# 		Authentication Required		: Yes
# 		Service Usage & Description	: This Api is used for view of category data within brand.

# 		Data Post: {
# 			"id"                   : "3"
# 		}

# 		Response: {

# 			"success": True, 
# 			"message": "Category retrieval api worked well!!",
# 			"data": final_result
# 		}

# 	"""
# 	permission_classes = (IsAuthenticated,)
# 	def post(self, request, format=None):
# 		try:
# 			from Brands.models import Company
# 			data = request.data
# 			data["id"] = str(data["id"])
# 			auth_id = request.user.id
# 			cid = get_user(auth_id)
# 			err_message = {}
# 			err_message["id"] = \
# 					validation_master_anything(data["id"],
# 					"Category Id",contact_re, 1)
# 			if any(err_message.values())==True:
# 				return Response({
# 					"success": False,
# 					"error" : err_message,
# 					"message" : "Please correct listed errors!!"
# 					})
# 			category_record = ProductCategory.objects.filter(id=data['id'])
# 			if category_record.count() == 0:
# 				return Response(
# 				{
# 					"success": False,
#  					"message": "Required Category data is not valid to retrieve!!"
# 				}
# 				)
# 			else:
# 				final_result = []
# 				q_dict = {}
# 				q_dict["id"] = category_record[0].id
# 				q_dict["category_name"] = category_record[0].category_name
# 				q_dict["category_code"] = category_record[0].category_code
# 				q_dict["description"] = category_record[0].description
# 				q_dict["priority"] = category_record[0].priority
# 				q_dict["active_status"] = category_record[0].active_status
# 				domain_name = addr_set()
# 				cat_img = str(category_record[0].category_image)
# 				if cat_img != "" and cat_img != None and cat_img != "null":
# 					full_path = domain_name + str(cat_img)
# 					q_dict['category_image'] = full_path
# 				else:
# 					q_dict['category_image'] = ''
# 				q_dict["subcategory"] = []
# 				scount = ProductsubCategory.objects.filter(category_id=data['id'])
# 				if scount.count() > 0:
# 					for index in scount:
# 						sub = {}
# 						sub['name'] = index.subcategory_name
# 						q_dict["subcategory"].append(sub)
# 				else:
# 					pass
# 				a = str(data['id'])
# 				q_dict["product"] = []
# 				pcount = Product.objects.filter(Q(product_categorys__icontains=a),Q(Company=cid))
# 				if pcount.count() > 0:
# 					for index in pcount:
# 						pro = {}
# 						pro['name'] = index.product_name
# 						q_dict["product"].append(pro)
# 				else:
# 					pass
# 				final_result.append(q_dict)
# 			return Response({
# 						"success": True, 
# 						"message": "Category retrieval api worked well!!",
# 						"data": final_result,
# 						})
# 		except Exception as e:
# 			print("Category retrieval Api Stucked into exception!!")
# 			print(e)
# 			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})
