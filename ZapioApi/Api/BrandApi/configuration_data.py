import re
from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
from Product.models import ProductCategory, ProductsubCategory,Product
#Serializer for api
from rest_framework import serializers
from Outlet.models import OutletProfile
from Location.models import CityMaster, AreaMaster
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user
from django.db.models import Q







class OutletListing(APIView):
	"""
	Outlet listing Configuration POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to provide all outlet details within brand.

		Data Post: {

			"company_auth_id" 	    : "3"
		}

		Response: {

			"success": true,
			"data": [
				{
					"id": 2,
					"auth_id": 7,
					"Outletname": "GTB Nagar, Jalandhar"
				},
				{
					"id": 1,
					"auth_id": 6,
					"Outletname": "Adarsh Nagar, Jalandhar"
				}
			],
			"message": "Outlet fetching successful!!"
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			user = request.user.id
			cid = get_user(user)
			query = OutletProfile.objects.filter(Q(is_company_active=1),Q(Company=cid))
			if query.count() > 0:
				oulet_conf_data_serializer = []
				for q in query:
					q_dict = {}
					q_dict["id"] = q.id
					q_dict["active_status"] = q.active_status
					q_dict["Outletname"] = q.Outletname
					q_dict["address"] = q.address
					q_dict["location"] = q.location
					domain_name = addr_set()
					out_img = str(q.outlet_image)
					if out_img != "" and out_img != None and out_img != "null":
						full_path = domain_name + str(q.outlet_image)
						q_dict['outlet_image'] = full_path
					else:
						q_dict['outlet_image'] = ''
					oulet_conf_data_serializer.append(q_dict)
				return Response(
						{
							"success": True,
							"data" : oulet_conf_data_serializer,
							"message": "Outlet fetching successful!!"
						}
						)
			else:
				return Response(
						{
							"success": True,
							"data" : [],
							"message": "Outlet fetching successful!!"
						}
						)

		except Exception as e:
			print("Outlet listing configuration Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})



# class CatagoryListing(APIView):
# 	"""
# 	Catagory listing Configuration POST API

# 		Authentication Required		: Yes
# 		Service Usage & Description	: This Api is used to provide all Catagory within brand.

# 		Data Post: {

# 			"company_auth_id" 	    : "3",
# 			"status"   ; "true"
# 		}

# 		Response: {

# 			"success": True,
# 			"data" : catagory_conf_data_serializer,
# 			"message": "Catagory fetching successful!!"
# 		}

# 	"""
# 	permission_classes = (IsAuthenticated,)
# 	def post(self, request, format=None):
# 		try:
# 			from Brands.models import Company
# 			data = request.data
# 			user = request.user.id
# 			cid = get_user(user)

# 			err_message = {}
# 			err_message["company_auth_id"] = \
# 					validation_master_anything(data["company_auth_id"],
# 					"Company auth ID",contact_re, 1)
# 			if any(err_message.values())==True:
# 				return Response({
# 					"success": False,
# 					"error" : err_message,
# 					"message" : "Please correct listed errors!!"
# 					})
# 			if data['status'] == True:
# 				query = ProductCategory.objects.\
# 						filter(Company=cid,active_status=1).order_by('-created_at')
# 			else:
# 				query = ProductCategory.objects.\
# 						filter(Company=cid,active_status=0).order_by('-created_at')

# 			catagory_conf_data_serializer = []
# 			for q in query:
# 				q_dict = {}
# 				q_dict["id"] = q.id
# 				q_dict["category_name"] = q.category_name 
# 				q_dict["outlet_map"] = q.outlet_map
# 				q_dict["priority"] = q.priority
# 				q_dict["category_code"] = q.category_code
# 				scount = ProductsubCategory.objects.filter(category_id=q.id).count()
# 				if scount > 0:
# 					q_dict['sub_category_count'] = scount
# 				else:
# 					q_dict['sub_category_count'] = 0
# 				a = str(q.id)
				

# 				pcount = Product.objects.filter(product_categorys__exact=[str(a)],\
# 					active_status=1,Company_id=cid)
# 				if pcount.count() > 0:
# 					q_dict['product_count'] = pcount.count()
# 				else:
# 					q_dict['product_count'] = 0
# 				domain_name = addr_set()
# 				cat_img = str(q.category_image)
# 				if cat_img != "" and cat_img != None and cat_img != "null":
# 					full_path = domain_name + str(q.category_image)
# 					q_dict['category_image'] = full_path
# 				else:
# 					q_dict['category_image'] = ''
# 				q_dict["active_status"] = q.active_status
# 				catagory_conf_data_serializer.append(q_dict)
# 			return Response(
# 					{
# 						"success": True,
# 						"data" : catagory_conf_data_serializer,
# 						"message": "Catagory fetching successful!!"
# 					}
# 					)
# 		except Exception as e:
# 			print("Catagory listing configuration Api Stucked into exception!!")
# 			print(e)
# 			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})


# class SubCatagoryListing(APIView):
# 	"""
# 	Sub-Catagory listing Configuration POST API

# 		Authentication Required		: Yes
# 		Service Usage & Description	: This Api is used to provide all Sub-Catagory within catagory.

# 		Data Post: {

# 			"cat_id" 	    : "3"
# 		}

# 		Response: {

# 			"success": True,
# 			"data" : subcatagory_conf_data_serializer,
# 			"message": "Sub-Catagory fetching successful!!"
# 		}

# 	"""
# 	permission_classes = (IsAuthenticated,)
# 	def post(self, request, format=None):
# 		try:
# 			from Brands.models import Company
# 			data = request.data
# 			err_message = {}
# 			err_message["cat_id"] = \
# 					validation_master_anything(data["cat_id"],
# 					"Catagory ID",contact_re, 1)
# 			if any(err_message.values())==True:
# 				return Response({
# 					"success": False,
# 					"error" : err_message,
# 					"message" : "Please correct listed errors!!"
# 					})
# 			query = ProductsubCategory.objects.filter(category=data["cat_id"]).order_by('-created_at')
# 			subcatagory_conf_data_serializer = []
# 			for q in query:
# 				q_dict = {}
# 				q_dict["id"] = q.id
# 				q_dict["category_id"] = q.category_id 
# 				q_dict["subcategory_name"] = q.subcategory_name
# 				q_dict["active_status"] = q.active_status
# 				domain_name = addr_set()
# 				sub_img = str(q.subcategory_image)
# 				if sub_img != "" and sub_img != None and sub_img != "null":
# 					full_path = domain_name + str(q.subcategory_image)
# 					q_dict['subcategory_image'] = full_path
# 				else:
# 					q_dict['subcategory_image'] = ''
# 				subcatagory_conf_data_serializer.append(q_dict)
# 			return Response(
# 					{
# 						"success": True,
# 						"data" : subcatagory_conf_data_serializer,
# 						"message": "Sub-Catagory fetching successful!!"
# 					}
# 					)
# 		except Exception as e:
# 			print("Sub-Catagory listing configuration Api Stucked into exception!!")
# 			print(e)
# 			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})



# class CatagoryWiseOutletListing(APIView):
# 	"""
# 	Catagory listing Configuration POST API

# 		Authentication Required		: Yes
# 		Service Usage & Description	: This Api is used to provide all outlets mapped with catagory.

# 		Data Post: {

# 			"cat_id" 	    : "3"
# 		}

# 		Response: {

# 			"success": True,
# 			"data" : catwise_serializer,
# 			"message": "Catagorywise outlet fetching successful!!"
# 		}

# 	"""
# 	permission_classes = (IsAuthenticated,)
# 	def post(self, request, format=None):
# 		try:
# 			from Brands.models import Company
# 			data = request.data
# 			err_message = {}
# 			err_message["cat_id"] = \
# 					validation_master_anything(data["cat_id"],
# 					"Catagory ID",contact_re, 1)
# 			if any(err_message.values())==True:
# 				return Response({
# 					"success": False,
# 					"error" : err_message,
# 					"message" : "Please correct listed errors!!"
# 					})
# 			query = ProductCategory.objects.filter(id=data["cat_id"]).order_by('-created_at')
# 			if query.count()==0:
# 				return Response(
# 					{
# 						"success": False,
# 						"message": "Category id is not valid to list out associated outlets!!"
# 					}
# 					) 
# 			else:
# 				data_info = query[0].outlet_map
# 				catwise_serializer = []
# 				for i in data_info:
# 					q_dict = {}
# 					outlet_info = OutletProfile.objects.filter(id=i,active_status=1)
# 					q_dict["id"] = outlet_info[0].id
# 					q_dict["outlet_name"] = outlet_info[0].Outletname
# 					catwise_serializer.append(q_dict)
# 			return Response(
# 					{
# 						"success": True,
# 						"data" : catwise_serializer,
# 						"message": "Catagorywise outlet fetching successful!!"
# 					}
# 					)
# 		except Exception as e:
# 			print("Catagorywise outlet fetching Api Stucked into exception!!")
# 			print(e)
# 			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})


# class CatagoryWiseSubCategoryListing(APIView):
# 	"""
# 	CatagoryWise Sub-Catagory listing Configuration POST API

# 		Authentication Required		: Yes
# 		Service Usage & Description	: This Api is used to provide all sub-category mapped with catagory.

# 		Data Post: {

# 			"cat_id" 	    : "3"
# 		}

# 		Response: {

# 			"success": True,
# 			"data" : catwise_serializer,
# 			"message": "CatagoryWise Sub-Catagory listing api worked well!!"
# 		}

# 	"""
# 	permission_classes = (IsAuthenticated,)
# 	def post(self, request, format=None):
# 		try:
# 			data = request.data
# 			err_message = {}
# 			err_message["cat_id"] = \
# 					validation_master_anything(data["cat_id"],
# 					"Catagory ID",contact_re, 1)
# 			if any(err_message.values())==True:
# 				return Response({
# 					"success": False,
# 					"error" : err_message,
# 					"message" : "Please correct listed errors!!"
# 					})
# 			query = ProductsubCategory.objects.filter(category=data["cat_id"]).order_by('-created_at')
# 			if query.count()==0:
# 				return Response(
# 					{
# 						"data" : [],
# 						"success": True,
# 						"message": "Category id is not valid to list out associated Sub-Catagory!!"
# 					}
# 					) 
# 			else:
# 				catwise_serializer = []
# 				for i in query:
# 					q_dict = {}
# 					q_dict["id"] = i.id
# 					q_dict["category"] = i.category_id
# 					q_dict["category_name"] = i.category.category_name
# 					q_dict["subcategory_name"] = i.subcategory_name
# 					q_dict["active_status"] = i.active_status
# 					q_dict["created_at"] = i.created_at
# 					q_dict["updated_at"] = i.updated_at
# 					catwise_serializer.append(q_dict)
# 			return Response(
# 					{
# 						"success": True,
# 						"data" : catwise_serializer,
# 						"message": "CatagoryWise Sub-Catagory listing api worked well!!"
# 					}
# 					)
# 		except Exception as e:
# 			print("CatagoryWise Sub-Catagory listing api Stucked into exception!!")
# 			print(e)
# 			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})


# class CityWiseAreaListing(APIView):
# 	"""
# 	CityWise Area listing Configuration POST API

# 		Authentication Required		: Yes
# 		Service Usage & Description	: This Api is used to provide all areas mapped with city.

# 		Data Post: {

# 			"id" 	    : "1"
# 		}

# 		Response: {

# 			"success": True,
# 			"data" :  serializer,
# 			"message": "CityWise Area listing api worked well!!"
# 		}

# 	"""
# 	permission_classes = (IsAuthenticated,)
# 	def post(self, request, format=None):
# 		try:
# 			data = request.data
# 			err_message = {}
# 			err_message["id"] = \
# 					validation_master_anything(data["id"],
# 					"City ID",contact_re, 1)
# 			if any(err_message.values())==True:
# 				return Response({
# 					"success": False,
# 					"error" : err_message,
# 					"message" : "Please correct listed errors!!"
# 					})
# 			query = AreaMaster.objects.filter(city=data["id"],active_status=1)
# 			if query.count()==0:
# 				return Response(
# 					{
# 						"success": False,
# 						"message": "City id is not valid to list out associated areas!!"
# 					}
# 					) 
# 			else:
# 				serializer = []
# 				for i in query:
# 					q_dict = {}
# 					q_dict["id"] = i.id
# 					q_dict["city"] = i.city_id
# 					q_dict["city_name"] = i.city.city
# 					q_dict["area"] = i.area
# 					q_dict["active_status"] = i.active_status
# 					q_dict["created_at"] = i.created_at
# 					q_dict["updated_at"] = i.updated_at
# 					serializer.append(q_dict)
# 			return Response(
# 					{
# 						"success": True,
# 						"data" : serializer,
# 						"message": "CityWise Area listing api worked well!!"
# 					}
# 					)
# 		except Exception as e:
# 			print("CityWise Area listing api Stucked into exception!!")
# 			print(e)
# 			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})