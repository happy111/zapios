import re,json,os
from rest_framework.status import (
	HTTP_200_OK,
	HTTP_406_NOT_ACCEPTABLE,
	HTTP_400_BAD_REQUEST,
	HTTP_404_NOT_FOUND,
	HTTP_500_INTERNAL_SERVER_ERROR,
)
from rest_framework.generics import (
	CreateAPIView,
	ListAPIView,
	RetrieveAPIView,
	UpdateAPIView,
	DestroyAPIView,
)
from rest_framework.views import APIView
from rest_framework.response import Response
from Outlet.models import OutletProfile
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from ZapioApi.api_packages import *
from datetime import datetime
from django.db.models import Q
from django.db.models import Max
from ZapioApi.Api.BrandApi.Validation.category_error_check import *
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user
from Product.models import *
from Configuration.models import *
from ZapioApi.Api.BrandApi.Validation.product_error_check import *
from kitchen.models import RecipeIngredient
from .serializers import *
from django.db import transaction
from django.http import Http404
from django.utils.translation import gettext_lazy



class CategoryCreationUpdation(APIView):
	"""
	Category Creation & Updation POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create & update product category within brand.

		Data Post: {
			"id"                   : "1"(Send this key in update record case,else it is not required!!)
			"category_name"		   : "Pizza",
			"category_code"		   : "123456",
			"company_auth_id" 	   : "3",
			"category_image"       : "a.jpg"
			"priority"             : "1"
			"description"		   : ""
		}

		Response: {

			"success": True, 
			"message": "Category Added Successfully!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			auth_id = request.user.id
			data["category_code"] = data["category_code"].strip()
			validation_check = err_check(data)
			cid = get_user(auth_id)
			data['Company'] = cid
			if validation_check != None:
				return Response(validation_check) 
			unique_check = unique_record_check(data,cid)
			if unique_check != None:
				return Response(unique_check)
			if "id" in data:
				category_record = ProductCategory.objects.filter(id=data['id'])
				if category_record.count() == 0:
					return Response(
					{
						"success": False,
						"message": "Category data is not valid to update!!"
					}
					)
				else:
					if 'category_image' in data:
						if data["category_image"] == '':
							data["category_image"] = category_record[0].category_image
						else:
							pass
					data["updated_at"] = datetime.now()
					category_serializer = \
					ProductCategorySerializer(category_record[0],data=data,partial=True)
					if category_serializer.is_valid():
						data_info = category_serializer.save()
						final_result = []
						final_result.append(category_serializer.data)
						return Response({
									"success": True, 
									"message": gettext_lazy("Category Edited Successfully!!"),
									"data": final_result,
									})
					else:
						print("something went wrong!!")
						return Response({
							"success": False, 
							"message": str(category_serializer.errors),
							})
			else:
				data['active_status'] = 1
				category_serializer = ProductCategorySerializer(data=data)
				if category_serializer.is_valid():
					data_info = category_serializer.save()
				else:
					print("something went wrong!!")
					return Response({
						"success": False, 
						"message": str(category_serializer.errors),
						})
			final_result = []
			final_result.append(category_serializer.data)
			return Response({
						"success": True, 
						"message": gettext_lazy("Category Added Successfully!!"),
						# "data": final_result,
						})
		except Exception as e:
			print("Category creation/updation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})


class CategoryView(APIView):
	"""
	Category view POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for view of category data within brand.

		Data Post: {
			"id"                   : "3"
		}

		Response: {

			"success": True, 
			"message": "Category retrieval api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			data["id"] = str(data["id"])
			auth_id = request.user.id
			cid = get_user(auth_id)
			err_message = {}
			err_message["id"] = \
					validation_master_anything(data["id"],
					"Category Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			category_record = ProductCategory.objects.filter(id=data['id'])
			if category_record.count() == 0:
				return Response(
				{
					"success": False,
					"message": "Required Category data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				q_dict = {}
				q_dict["id"] = category_record[0].id
				q_dict["category_name"] = category_record[0].category_name
				q_dict["category_code"] = category_record[0].category_code
				q_dict["description"] = category_record[0].description
				q_dict["priority"] = category_record[0].priority
				q_dict["active_status"] = category_record[0].active_status
				domain_name = addr_set()
				cat_img = str(category_record[0].category_image)
				if cat_img != "" and cat_img != None and cat_img != "null":
					full_path = domain_name + str(cat_img)
					q_dict['category_image'] = full_path
				else:
					q_dict['category_image'] = ''
				q_dict["subcategory"] = []
				scount = ProductsubCategory.objects.filter(category_id=data['id'])
				if scount.count() > 0:
					for index in scount:
						sub = {}
						sub['name'] = index.subcategory_name
						q_dict["subcategory"].append(sub)
				else:
					pass
				a = str(data['id'])
				q_dict["product"] = []
				pcount = Product.objects.filter(Q(product_categorys__icontains=a),Q(Company=cid))
				if pcount.count() > 0:
					for index in pcount:
						pro = {}
						pro['name'] = index.product_name
						q_dict["product"].append(pro)
				else:
					pass
				final_result.append(q_dict)
			return Response({
						"success": True, 
						"message": "Category retrieval api worked well!!",
						"data": final_result,
						})
		except Exception as e:
			print("Category retrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})



class CategoryDelete(APIView):
	"""
	Category Delete POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to delete category .

		Data Post: {
			"id"                   : 1
		}

		Response: {

			"success": True,
			"message": "Category delete api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			data["id"] = str(data["id"])
			err_message = {}
			err_message["id"] = \
					validation_master_anything(data["id"],
					"Category Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			category_record = ProductCategory.objects.filter(id=data['id'])
			if category_record.count() == 0:
				return Response(
				{
					"success": False,
					"message": "Required Category data is not valid to delete!!"
				}
				)
			else:
				scount = ProductsubCategory.objects.filter(category_id=data['id'])
		
				if scount.count() == 0:
					pass
				else:
					return Response(
						{
							"success": False,
							"message": "Category data mapping to subcategory!!"
						}
				  )
				a = str(data['id'])
				pcount = Product.objects.filter(product_categorys__exact=[str(a)])

				if pcount.count() > 0:
					return Response(
						{
							"success": False,
							"message": "Category data mapping to product!!"
						}
					)
				else:
					pass
				category_record.update(is_hide=1)
				return Response({
						"success": True, 
						"message": "Delete Successfully!!",
						})
		except Exception as e:
			print("Category deleted Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})




class AddonDelete(APIView):
	"""
	Addon Delete POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to delete addon .

		Data Post: {
			"id"                   : 1
		}

		Response: {

			"success": True,
			"message": "Addon delete api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			data["id"] = str(data["id"])
			err_message = {}
			err_message["id"] = \
					validation_master_anything(data["id"],
					"Addon Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			addon_record = Addons.objects.filter(id=data['id'])
			if addon_record.count() == 0:
				return Response(
				{
					"success": False,
					"message": "Required Addon data is not valid to delete!!"
				}
				)
			else:
				addon_record.update(is_hide=1)
				return Response({
						"success": True, 
						"message": "Delete Successfully!!",
						})
		except Exception as e:
			print("Addon deleted Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})




class ProductDelete(APIView):
	"""
	Product Delete POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to delete product.

		Data Post: {
			"id"                   : 1
		}

		Response: {

			"success": True,
			"message": "Product delete api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			data["id"] = str(data["id"])
			err_message = {}
			err_message["id"] = \
					validation_master_anything(data["id"],
					"Product Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			product_record = Product.objects.filter(id=data['id'])
			if product_record.count() == 0:
				return Response(
				{
					"success": False,
					"message": "Required Product data is not valid to delete!!"
				}
				)
			else:
				product_record.update(is_hide=1)
				return Response({
						"success": True, 
						"message": "Delete Successfully!!",
						})
		except Exception as e:
			print("Product deleted Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})



class SubcategoryDelete(APIView):
	"""
	Subcategory Delete POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to delete subcategory .

		Data Post: {
			"id"                   : 1
		}

		Response: {

			"success": True,
			"message": "Subcategory delete api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			data["id"] = str(data["id"])
			err_message = {}
			err_message["id"] = \
					validation_master_anything(data["id"],
					"Subcategory Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			category_record = ProductsubCategory.objects.filter(id=data['id'])
			if category_record.count() == 0:
				return Response(
				{
					"success": False,
					"message": "Required Subcategory data is not valid to delete!!"
				}
				)
			else:
				a = str(data['id'])
				pcount = Product.objects.filter(product_subcategorys__icontains=a)
				if pcount.count() > 0:
					return Response(
						{
							"success": False,
							"message": "This Subcategory associate with products!!"
						}
					)
				else:
					pass
				category_record.update(is_hide=1)
				return Response({
						"success": True, 
						"message": "Delete Successfully!!",
						})
		except Exception as e:
			print("Subcategory deleted Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})





class CategoryRetrieval(APIView):
	"""
	Category retrieval POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of category data within brand.

		Data Post: {
			"id"                   : "3"
		}

		Response: {

			"success": True, 
			"message": "Category retrieval api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			data["id"] = str(data["id"])
			err_message = {}
			err_message["id"] = \
					validation_master_anything(data["id"],
					"Category Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			category_record = ProductCategory.objects.filter(id=data['id'])
			if category_record.count() == 0:
				return Response(
				{
					"success": False,
					"message": "Required Category data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				q_dict = {}
				q_dict["id"] = category_record[0].id
				q_dict["category_name"] = category_record[0].category_name
				q_dict["category_code"] = category_record[0].category_code
				q_dict["description"] = category_record[0].description
				q_dict["priority"] = category_record[0].priority
				q_dict["active_status"] = category_record[0].active_status
				domain_name = addr_set()
				cat_img = str(category_record[0].category_image)
				if cat_img != "" and cat_img != None and cat_img != "null":
					full_path = domain_name + str(cat_img)
					q_dict['category_image'] = full_path
				else:
					q_dict['category_image'] = ''
				final_result.append(q_dict)
			return Response({
						"success": True, 
						"message": "Category retrieval api worked well!!",
						"data": final_result,
						})
		except Exception as e:
			print("Category retrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})




class SubCategoryRetrieval(APIView):
	"""
	Sub-Category retrieval POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of subcategory data within brand.

		Data Post: {
			"id"                   : "1"
		}

		Response: {

			"success": True, 
			"message": "Sub-Category retrieval api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			err_message = {}
			err_message["id"] = \
					validation_master_anything(data["id"],
					"Category Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = ProductsubCategory.objects.filter(id=data['id'])
			if record.count() == 0:
				return Response(
				{
					"success": False,
					"message": "Required Sub-Category data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				q_dict = {}
				q_dict["id"] = record[0].id
				q_dict["cat_id"] = record[0].category_id
				q_dict["category_name"] = record[0].category.category_name
				q_dict["subcategory_name"] = record[0].subcategory_name
				q_dict["active_status"] = record[0].active_status
				q_dict["created_at"] = record[0].created_at
				q_dict["updated_at"] = record[0].updated_at
				if record[0].description == None:
					q_dict["description"] = ''
				else:
					q_dict['description'] = record[0].description
				if record[0].priority == None:
					q_dict["priority"] = ''
				else:
					q_dict['priority'] = record[0].priority
				domain_name = addr_set()
				sub_img = str(record[0].subcategory_image)
				if sub_img != "" and sub_img != None and sub_img != "null":
					full_path = domain_name + str(sub_img)
					q_dict['subcategory_image'] = full_path
				else:
					q_dict['subcategory_image'] = ''


				final_result.append(q_dict)
			return Response({
						"success": True, 
						"message": "Sub-Category retrieval api worked well!!",
						"data": final_result,
						})
		except Exception as e:
			print("Sub-Category retrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})




class FoodTypeRetrieval(APIView):
	"""
	FoodType retrieval POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of FoodType data.

		Data Post: {
			"id"                   : "1"
		}

		Response: {

			"success": True, 
			"message": "FoodType retrieval api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			err_message = {}
			err_message["id"] = \
					validation_master_anything(data["id"],
					"FoodType Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = FoodType.objects.filter(id=data['id'])
			if record.count() == 0:
				return Response(
				{
					"success": False,
					"message": "Provided FoodType data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				q_dict = {}
				q_dict["id"] = record[0].id
				q_dict["food_type"] = record[0].food_type
				full_path = addr_set()
				q_dict["foodtype_image"] = record[0].foodtype_image
				if q_dict["foodtype_image"] != None and q_dict["foodtype_image"]!="":
					q_dict["foodtype_image"] = full_path+str(q_dict["foodtype_image"])
				else:
					q_dict["foodtype_image"] = None
				q_dict["active_status"] = record[0].active_status
				q_dict["created_at"] = record[0].created_at
				q_dict["updated_at"] = record[0].updated_at
				final_result.append(q_dict)
			return Response({
						"success": True, 
						"message": "FoodType retrieval api worked well!!",
						"data": final_result,
						})
		except Exception as e:
			print("FoodType retrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})




class VariantRetrieval(APIView):
	"""
	Variant retrieval POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of Variant data within brand.

		Data Post: {
			"id"                   : "1"
		}

		Response: {

			"success": True, 
			"message": "Variant retrieval api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			err_message = {}
			err_message["id"] = \
					validation_master_anything(data["id"],
					"Variant Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = Variant.objects.filter(id=data['id'])
			if record.count() == 0:
				return Response(
				{
					"success": False,
					"message": "Provided Variant data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				q_dict = {}
				q_dict["id"] = record[0].id
				q_dict["variant"] = record[0].variant
				q_dict["description"] = record[0].description
				q_dict["Company"] = record[0].Company_id
				q_dict["Company_name"] = record[0].Company.company_name
				q_dict["active_status"] = record[0].active_status
				q_dict["created_at"] = record[0].created_at
				q_dict["updated_at"] = record[0].updated_at
				final_result.append(q_dict)
			return Response({
						"success": True, 
						"message": "Variant retrieval api worked well!!",
						"data": final_result,
						})
		except Exception as e:
			print("Variant retrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})



class AddonDetailsRetrieval(APIView):
	"""
	AddonDetails retrieval POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of AddonDetails data.

		Data Post: {
			"id"                   : "1"
		}

		Response: {

			"success": True, 
			"message": "AddonDetails retrieval api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			err_message = {}
			err_message["id"] = \
					validation_master_anything(data["id"],
					"AddonDetails Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = AddonDetails.objects.filter(id=data['id'])
			if record.count() == 0:
				return Response(
				{
					"success": False,
					"message": "Provided AddonDetails data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				q_dict = {}
				q_dict["id"] = record[0].id
				q_dict["addon_gr_name"] = record[0].addon_gr_name
				q_dict["addon_gr_name_details"] = []
				q_dict["min_addons"] = record[0].min_addons
				q_dict["max_addons"] = record[0].max_addons
				q_dict["description"] = record[0].description
				q_dict["addons"] = record[0].addons
				q_dict["associated_addons_details"] = []
				if q_dict["addons"] != None:
					if len(q_dict["addons"]) != 0:
						for i in q_dict["addons"]:
							addon_data = Addons.objects.filter(id=i)
							if addon_data.count() > 0:
								associated_addons_dict = {}
								associated_addons_dict["label"] = addon_data[0].name
								associated_addons_dict["price"] = addon_data[0].addon_amount
								associated_addons_dict["value"] = addon_data[0].id
								q_dict["associated_addons_details"].append(associated_addons_dict)

					else:
						pass
				else:
					pass
				q_dict["active_status"] = record[0].active_status
				q_dict["created_at"] = record[0].created_at
				q_dict["updated_at"] = record[0].updated_at
				final_result.append(q_dict)
			return Response({
						"success": True, 
						"message": "AddonDetails retrieval api worked well!!",
						"data": final_result,
						})
		except Exception as e:
			print("AddonDetails retrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})



class ProductRetrieval(APIView):
	"""
	Product retrieval POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of Product data.

		Data Post: {
			"id"                   : "60"
		}

		Response: {

			"success": True, 
			"message": "Product retrieval api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			err_message = {}
			err_message["id"] = \
					validation_master_anything(data["id"],
					"Product Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = Product.objects.filter(id=data['id'])
			if record.count() == 0:
				return Response(
				{
					"success": False,
					"message": "Provided Product data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				q_dict = {}
				q_dict["id"] = record[0].id
				q_dict["cat_detail"] = []
				catDetail = record[0].product_categorys
				if catDetail !=None:
					for index in catDetail:
						cat_dict = {}
						cat_dict["label"] = ProductCategory.objects.filter(id=index)[0].category_name
						cat_dict['value'] = int(index)
						q_dict["cat_detail"].append(cat_dict)
				q_dict["subcat_detail"] = []
				subcatDetail = record[0].product_subcategorys
				if subcatDetail !=None:
					for index in subcatDetail:
						subcat_dict = {}
						subcat_dict["label"] = ProductsubCategory.objects.filter(id=index)[0].subcategory_name
						subcat_dict['value'] = int(index)
						q_dict["subcat_detail"].append(subcat_dict)
				else:
					q_dict["subcat_detail"] = []
				if record[0].spice != None:
					q_dict["spice_detail"] = []
					spice_dict = {}
					spice_dict["label"] = record[0].spice
					spice_dict["key"] = record[0].spice
					spice_dict["value"] = record[0].spice
					q_dict["spice_detail"].append(spice_dict)
				else:
					q_dict["spice_detail"] = []
				q_dict['pin']  = record[0].primaryIngredient_deatils
				va = q_dict['pin']
				if va != None:
					for v in va:
						if 'pingredient' in v:
							pin = v['pingredient']
							r = RecipeIngredient.objects.filter(id=pin)
							if r.count() > 0:
								pname = r[0]
								v['primaryIng'] = {}
								v['primaryIng']["label"] = pname.name
								v['primaryIng']["key"] = pin
								v['primaryIng']["value"] = pin
						if 'unit' in v:
							pin = v['unit']
							u = Unit.objects.filter(id=pin)
							if u.count() > 0:
								pname = u[0]
								v['unit'] = {}
								v['unit']["label"] = pname.unit_name
								v['unit']["key"] = pin
								v['unit']["value"] = pin
						del v["pingredient"]
					q_dict['pin'] = va
				q_dict["product_schema"] = record[0].product_schema
				ps = q_dict['product_schema']
				if ps !=None:
					for v in ps:
						if 'unit' in v:
							pin = v['unit']
							pname = Unit.objects.filter(id=pin)[0]
							v['unit'] = {}
							v['unit']["label"] = pname.unit_name
							v['unit']["key"] = pin
							v['unit']["value"] = pin
					q_dict['product_schema'] = ps
				else:
					pass
				if record[0].delivery_option != None:
					q_dict["delivery_option"] = record[0].delivery_option
				else:
					q_dict['delivery_option'] = ''
				q_dict["product_name"] = record[0].product_name
				q_dict["food_type"] = record[0].food_type.food_type
				q_dict["foodtype_detail"] = []
				food_dict = {}
				food_dict["label"] = record[0].food_type.food_type
				food_dict["key"] = record[0].food_type_id
				food_dict["value"] = record[0].food_type_id
				q_dict["foodtype_detail"].append(food_dict)
				q_dict["priority"] = record[0].priority
				q_dict["video_url"] = record[0].video_url
				q_dict["product_image"] = record[0].product_image
				q_dict["ordering_code"] = record[0].ordering_code
				full_path = addr_set()
				if q_dict["product_image"] != None and q_dict["product_image"]!="":
					q_dict["product_image"] = full_path+str(q_dict["product_image"])
				else:
					q_dict["product_image"] = None
				q_dict["product_video"] = record[0].pvideo
				full_path = addr_set()
				if q_dict["product_video"] != None and q_dict["product_video"]!="":
					q_dict["product_video"] = full_path+str(q_dict["product_video"])
				else:
					q_dict["product_video"] = None
				q_dict["product_image"] = []
				pimg = ProductImage.objects.filter(product_id=data['id'])
				if pimg.count() > 0:
					for index in pimg:
						full_path = addr_set()
						fimgs = full_path+str(index.product_image)
						q_dict["product_image"].append(fimgs)
				q_dict["product_code"] = record[0].product_code
				q_dict["product_desc"] = record[0].product_desc
				q_dict["kot_desc"] = record[0].kot_desc
				q_dict["has_variant"] = record[0].has_variant
				q_dict["price"] = record[0].price
				q_dict["is_recommended"] = record[0].is_recommended
				q_dict["discount_price"] = record[0].discount_price
				q_dict["variant_deatils"] = record[0].variant_deatils
				q_dict["is_recommended"] = record[0].is_recommended
				q_dict["packing_charge"] = record[0].packing_charge
				q_dict["short_desc"] = record[0].short_desc
				va = q_dict["variant_deatils"] 
				if va != None:
					for v in va:
						if "name" in v:
							v_name = v["name"]
							v["name"] = {}
							v["name"]["id"] = v_name
							p_id= record[0].id
							v["name"]["label"] = v_name
							v["name"]["key"] = v_name
							v["dis"] = v["discount_price"]
							v_id = Variant.objects.filter(variant=v_name)[0].id
							v_addon = v["addon_group"]
							v["addonGroup"] = []
							if len(v_addon) != 0:
								for i in v_addon:
									v_addon_dict = {}
									addon_q = AddonDetails.objects.filter(id=i)
									if addon_q.count() > 0:
										v_addon_dict["value"] = addon_q[0].id
										v_addon_dict["key"] = addon_q[0].id
										v_addon_dict["label"] = addon_q[0].addon_gr_name
										v["addonGroup"].append(v_addon_dict)
									else:
										pass
							else:
								pass
							del v["addon_group"]
							del v["discount_price"]
						else:
							pass
					q_dict["variant_deatils"] = va
				else:
					pass
				addons_detail = record[0].addpn_grp_association
				q_dict["addon_details"] = []
				if addons_detail != None:
					for q in addons_detail:
						addon_q = AddonDetails.objects.filter(id=q)
						if addon_q.count() > 0:
							addon_dict = {}
							addon_dict["value"] = addon_q[0].id
							addon_dict["key"] = addon_q[0].id
							addon_dict["label"] = addon_q[0].addon_gr_name
							addon_dict["associated_addons"] = addon_q[0].addons
							q_dict["addon_details"].append(addon_dict)
						else:
							pass
				else:
					pass
				tag_detail  = record[0].tags
				q_dict["tags"] = []
				if tag_detail != None:
					for i in tag_detail:
						tag_q = Tag.objects.filter(id=i)
						if tag_q.count() > 0:
							tag_dict = {}
							tag_dict["value"] = tag_q[0].id
							tag_dict["key"] = tag_q[0].id
							tag_dict["label"] = tag_q[0].tag_name
							q_dict["tags"].append(tag_dict)
						else:
							pass
				else:
					pass
				platform_detail  = record[0].included_platform
				q_dict["platform_detail"] = []
				if platform_detail != None:
					for i in platform_detail:
						tag_dict = {}
						tag_dict["value"] = i
						tag_dict["key"] = i
						tag_dict["label"] = i
						q_dict["platform_detail"].append(tag_dict)
				else:
					pass
				allergen_detail  = record[0].allergen_Information
				q_dict["allergen_Information"] = []
				if allergen_detail != None:
					for i in allergen_detail:
						in_dict = {}
						in_dict["value"] = i
						in_dict["key"] = i
						in_dict["label"] = i
						q_dict["allergen_Information"].append(in_dict)
				else:
					pass
				tax_detail = record[0].tax_association
				q_dict["tax_association"] = []
				if tax_detail != None:
					for i in tax_detail:
						tax_q = TaxSetting.objects.filter(id=i)
						if tax_q.count() != 0:
							tax_dict = {}
							tax_dict["value"] = tax_q[0].id
							tax_dict["key"] = tax_q[0].id
							tax_dict["label"] = str(tax_q[0].tax_name)+" | "+str(tax_q[0].tax_percent)+"%" 
							q_dict["tax_association"].append(tax_dict)
						else:
							pass
				else:
					pass
				q_dict['packaging_amount'] = record[0].packing_amount
				q_dict['price_types'] = []
				if record[0].price_type != None:
					dic = {}
					dic['label'] = record[0].price_type
					dic['value'] = record[0].price_type
					q_dict['price_types'].append(dic)

				packageTax = record[0].package_tax
				q_dict["package_tax"] = []
				if packageTax != None:
					for i in packageTax:
						tax_q = TaxSetting.objects.filter(id=i)
						if tax_q.count() != 0:
							tax_dict = {}
							tax_dict["value"] = tax_q[0].id
							tax_dict["key"] = tax_q[0].id
							tax_dict["label"] = str(tax_q[0].tax_name)+" | "+str(tax_q[0].tax_percent)+"%" 
							q_dict["package_tax"].append(tax_dict)
						else:
							pass
				else:
					pass
				q_dict["is_tax"] = record[0].is_tax


				final_result.append(q_dict)
			if final_result:
				return Response({
							"success": True, 
							"message": "Product retrieval api worked well!!",
							"data": final_result,
							})
			else:
				return Response({
							"success": True, 
							"message": "No product data found!!"
							})
		except Exception as e:
			print("Product retrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})





class FeatureRetrieval(APIView):
	"""
	Features Product retrieval POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of Feature products data.

		Data Post: {
			"id"                   : "60"
		}

		Response: {

			"success": True, 
			"message": "Feature Product retrieval api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			err_message = {}
			err_message["id"] = \
					validation_master_anything(str(data["id"]),
					"Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = FeatureProduct.objects.filter(id=data['id'])
			if record.count() == 0:
				return Response(
				{
					"success": False,
					"message": "Provided Feature Product data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				q_dict = {}
				q_dict["id"] = record[0].id
				q_dict["outlet_detail"] = []
				outlet_dict = {}
				outlet_dict["label"] = record[0].outlet.Outletname
				outlet_dict["key"] = record[0].outlet_id
				outlet_dict["value"] = record[0].outlet_id
				q_dict["outlet_detail"].append(outlet_dict)
				feature_detail  = record[0].feature_product
				q_dict["feature_detail"] = []
				if feature_detail != None:
					for i in feature_detail:
						q = Product.objects.filter(id=i)
						feature_dict = {}
						feature_dict["value"] = q[0].id
						feature_dict["key"] = q[0].id
						feature_dict["label"] = q[0].product_name
						q_dict["feature_detail"].append(feature_dict)
				else:
					pass
				final_result.append(q_dict)
			if final_result:
				return Response({
							"success": True, 
							"message": "Feature Product retrieval api worked well!!",
							"data": final_result,
							})
			else:
				return Response({
							"success": True, 
							"message": "No product data found!!"
							})
		except Exception as e:
			print("Feature Product retrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})



class AddonRetrieval(APIView):
	"""
	Addon retrieval POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for retrieval of Addon data within brand.

		Data Post: {
			"id"                   : "1"
		}

		Response: {

			"success": True, 
			"message": "Addon retrieval api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			err_message = {}
			err_message["id"] = \
					validation_master_anything(data["id"],
					"Addon Id",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			record = Addons.objects.filter(id=data['id'])
			if record.count() == 0:
				return Response(
				{
					"success": False,
					"message": "Provided Addon data is not valid to retrieve!!"
				}
				)
			else:
				final_result = []
				q_dict = {}
				q_dict["id"] = record[0].id
				q_dict["name"] = record[0].name
				q_dict["identifier"] = record[0].identifier
				q_dict["addon_amount"] = record[0].addon_amount
				q_dict["priority"] = record[0].priority
				q_dict["active_status"] = record[0].active_status
				q_dict["created_at"] = record[0].created_at
				q_dict["updated_at"] = record[0].updated_at
				final_result.append(q_dict)
			return Response({
						"success": True, 
						"message": "Addon retrieval api worked well!!",
						"data": final_result,
						})
		except Exception as e:
			print("Addon retrieval Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})




class SubCategoryCreation(APIView):
	"""
	Sub Category Creation POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create product sub category associated with
		category.

		Data Post: {
			"category"		       : "3",
			"subcategory_name"	   : ["Special Pizza","Combo Pizza"]
			"subcategory_image"    : "a.jpg"
			"description"		   : "da",
			"priority"             : "1"

		}

		Response: {

			"success": True, 
			"message": "Sub-Category creation api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			auth_id = request.user.id
			cid = get_user(auth_id)
			data['Company'] = cid
			err_message = {}
			data['name']    =     json.loads(data["name"])
			data['priority'] =   json.loads(data['priority'])
			err_message["category"] =\
				validation_master_anything(data["category"],
					"Category",contact_re, 1)
			
			if len(data["name"]) != 0:
				for k in data['name']:
					a = data['name'].count(k)
					if a > 1:
						err_message["duplicate_subcat"] = \
							"Same Sub-Category not allow!!"
			else:
				pass
			
			if len(data["name"]) != 0:
				for i in data["name"]:
					err_message["subcategory_name"] = \
						validation_master_anything(i,
						"Sub-Category name",alpha_re, 3)
					if data["category"] != "":
						record_check = ProductsubCategory.objects.filter(Q(subcategory_name__iexact=i),\
													Q(category=data["category"]),Q(Company_id=cid))
						if record_check.count() != 0:
							err_message["duplicate_subcat"] = \
							"This subcategory already exist under this category!!"
							break
					if err_message["subcategory_name"] != None:
						break
			else:
				err_message["subcategory_name"] = validation_master_anything("t",
						"Sub-Category name",alpha_re, 3)
			if len(data["priority"]) != 0:
				ch_pri = []
				for i in data["priority"]:
					err_message["priority"] = validation_master_anything(i,
						"Priority",contact_re, 1)
					if err_message["priority"] == None:
						ch_pri.append(i)
						priority_check = ProductsubCategory.objects.filter(Q(priority=int(i)),\
												Q(Company_id=cid))
						if priority_check.count() != 0:
							max_priority = \
							ProductsubCategory.objects.filter(Company_id=cid).aggregate(Max('priority'))
							suggestion = max_priority["priority__max"] + 1
							err_message["priority_check"] = \
							"This priority is already assigned to other Subcategory..You can try "+str(suggestion)+" as priority!!"
				for k in ch_pri:
					if ch_pri.count(k) > 1:
						err_message['priority_duplicate'] = "Same priority now allow!!"
			else:
				pass
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			cat_query = ProductCategory.objects.filter(id=data["category"])
			if cat_query.count() != 0:
				pass
			else:
				return Response(
					{
						"success": False,
						"message": "Category is not valid!!"
					}
					)
			k =0
			for p in data["priority"]:
				img = 'image'+str(k)
				fimg = data[img]
				dp = 'description'+str(k)
				desc = data[dp]
				s_name = data['name'][k]
				create_record = ProductsubCategory.objects.create(category_id=data["category"],\
												subcategory_name=s_name,subcategory_image=fimg,
												Company_id=cid,
												priority=p,
												description=desc,active_status=1)
				k = k + 1
			return Response({
						"success": True, 
						"message": "Sub-Category has been created successfully!!"
						})
		except Exception as e:
			print("Sub-Category creation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})


class SubCategoryUpdation(APIView):
	"""
	Sub Category Updation POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to update product sub category associated with
		category.

		Data Post: {
			"id"                   : "1",
			"category"		       : "3",
			"subcategory_name"	   : "Special Pizza",
			"description"          : "dsdadas"
			"subcategory_image"    : ""
		}

		Response: {

			"success": True, 
			"message": "Sub-Category Updation api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			mutable = request.POST._mutable
			request.POST._mutable = True
			from django.db.models import Q
			data = request.data
			auth_id = request.user.id
			cid = get_user(auth_id)
			err_message = {}
			err_message["id"] = \
					validation_master_anything(str(data["id"]),
					"Sub-Category Id",contact_re, 1)
			err_message["category"] = \
					validation_master_anything(str(data["category"]),
					"Category",contact_re, 1)
			err_message["subcategory_name"] = \
					validation_master_anything(data["subcategory_name"],
					"Sub-Category name",alpha_re, 3)
			
			print("vvvvvvvvvvvvvvvvvvvvvvvvvv",err_message)

			err_message["priority"] = \
			only_required(data["priority"],"Priority")
			if type(data["subcategory_image"]) != str:
				im_name_path =  data["subcategory_image"].file.name
				im_size = os.stat(im_name_path).st_size
				if im_size > 1000*1024:
					err_message["image_size"] = "Subcategory image can'nt excced the size more than 10kb!!"
			else:
				data["subcategory_image"] = ''
			
			if data['priority'] != '':
				priority_check = ProductsubCategory.objects.filter(~Q(id=data["id"]),\
									Q(priority=int(data["priority"])),Q(Company_id=cid))

				if priority_check.count() != 0:
					max_priority = \
					ProductsubCategory.objects.filter(Company_id=cid).aggregate(Max('priority'))
					suggestion = max_priority["priority__max"] + 1
					err_message["priority_check"] = \
					"This priority is already assigned to other Subcategory..You can try "+str(suggestion)+" as priority!!"
				else:
					pass
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			cat_query = ProductCategory.objects.filter(id=data["category"])
			

			if cat_query.count() != 0:
				pass
			else:
				return Response(
					{
						"success": False,
						"message": "Category is not valid!!"
					}
					)
			sucat_query = ProductsubCategory.objects.filter(id=data["id"])
			if sucat_query.count() != 0:
				pass
			else:
				return Response(
					{
						"success": False,
						"message": "Sub-Category id is not valid to update!!"
					}
					)
			unique_check = \
			ProductsubCategory.objects.filter(~Q(id=data["id"]),Q(category=data["category"]),\
									Q(subcategory_name__iexact=data['subcategory_name']))
			if unique_check.count()==0:
				if data["subcategory_image"] == None:
					data["subcategory_image"] = sucat_query[0].subcategory_image
				else:
					pass
				serializer = SubCategorySerializer(sucat_query[0],data=data,partial=True)
				if serializer.is_valid():
					data_info = serializer.save()
				else:
					print("something went wrong!!",serializer.errors)
					return Response({
						"success": False, 
						"message": str(serializer.errors),
						})
			else:
				err_message = {}
				err_message["duplicate_subcat"] = "Sub-Category with this name already exists!!" 
				return Response({
						"success": False, 
						"error" : err_message,
						"message" : "Please correct listed errors!!"
						})
			final_result = []
			final_result.append(serializer.data)
			return Response({
						"success": True, 
						"data" : final_result,
						"message": gettext_lazy("Sub-Category has been updated successfully!!")
						})
		except Exception as e:
			print("Sub-Category updation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})



class FoodTypeCreationUpdation(APIView):
	"""
	FoodType Creation & Updation POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create & update Food Type.

		Data Post: {
			"id"                   : "1"(Send this key in update record case,else it is not required!!)
			"food_type"		       : "Veg",
			"foodtype_image"	   : "veg.jpg"(type:image)
		}

		Response: {

			"success": True, 
			"message": "Food Type creation/updation api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			err_message = {}
			if type(data["foodtype_image"]) != str:
				im_name_path =  data["foodtype_image"].file.name
				im_size = os.stat(im_name_path).st_size
				if im_size > 10*1024:
					err_message["image_size"] = "Food type logo can'nt excced the size more than 10kb!!"
			else:
				data["foodtype_image"] = None
			err_message["food_type"] = \
					validation_master_anything(data["food_type"],
					"Food type",alpha_re, 2)
			if "id" in data:
				unique_check = FoodType.objects.filter(~Q(id=data["id"]),\
								Q(food_type__iexact=data["food_type"]))
			else:
				unique_check = FoodType.objects.filter(Q(food_type__iexact=data["food_type"]))
			if unique_check.count() != 0:
				err_message["unique_check"] = "Food type with this name already exists!!"
			else:
				pass
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			data["active_status"] = 1
			if "id" in data:
				FoodType_record = FoodType.objects.filter(id=data['id'])
				if FoodType_record.count() == 0:
					return Response(
					{
						"success": False,
						"message": "Food Type data is not valid to update!!"
					}
					)
				else:
					if data["foodtype_image"] == None:
						data["foodtype_image"] = FoodType_record[0].foodtype_image
					else:
						pass
					data["updated_at"] = datetime.now()
					FoodType_serializer = \
					FoodTypelistingSerializer(FoodType_record[0],data=data,partial=True)
					if FoodType_serializer.is_valid():
						data_info = FoodType_serializer.save()
					else:
						print("something went wrong!!")
						return Response({
							"success": False, 
							"message": str(FoodType_serializer.errors),
							})
			else:
				FoodType_serializer = FoodTypelistingSerializer(data=data)
				if FoodType_serializer.is_valid():
					data_info = FoodType_serializer.save()
				else:
					print("something went wrong!!")
					return Response({
						"success": False, 
						"message": str(FoodType_serializer.errors),
						})
			final_result = []
			final_result.append(FoodType_serializer.data)
			return Response({
						"success": True, 
						"message": gettext_lazy("Food Type creation/updation api worked well!!"),
						"data": final_result,
						})
		except Exception as e:
			print("Food Type creation/updation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})




class VariantCreationUpdation(APIView):
	"""
	Variant Creation & Updation POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create & update product Variant within brand.

		Data Post: {
			"id"                   : "1"(Send this key in update record case,else it is not required!!)
			"variant"		   	   : "Large"
		}

		Response: {

			"success": True, 
			"message": "Variant creation/updation api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			user = request.user.id
			cid = get_user(user)
			data['Company'] = cid			
			err_message = {}
			err_message["variant"] = \
					validation_master_anything(data["variant"],
					"Variant name",username_re, 3)
			unique_check = Variant.objects.filter(variant__iexact=data["variant"],
											Company=cid)
			if unique_check.count() != 0 and "id" not in data:
				err_message["unique_check"] = "Variant with this name already exists!!"
			else:
				pass
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			company_query = Company.objects.filter(id=cid)
			if company_query.count() != 0:
				data["Company"] = cid
			else:
				return Response(
					{
						"success": False,
						"message": "Company is not valid!!"
					}
					)
			if "id" in data:
				variant_record = Variant.objects.filter(id=data['id'])
				if variant_record.count() == 0:
					return Response(
					{
						"success": False,
						"message": "Category data is not valid to update!!"
					}
					)
				else:
					unique_check = \
					Variant.objects.filter(~Q(id=data["id"]),\
									Q(variant__iexact=data['variant']),\
									Q(Company=cid))
					if unique_check.count() == 0:
						data["updated_at"] = datetime.now()
						variant_serializer = \
						VariantSerializer(variant_record[0],data=data,partial=True)
						if variant_serializer.is_valid():
							data_info = variant_serializer.save()
							info_msg = gettext_lazy("Vriant updated successfully!!")
						else:
							print("something went wrong!!")
							return Response({
								"success": False, 
								"message": str(variant_serializer.errors),
								})
					else:
						err_message = {}
						err_message["unique_check"] = "Variant with this name already exists!!"
						return Response({
									"success": False,
									"error" : err_message,
									"message" : "Please correct listed errors!!"
									})
			else:
				variant_serializer = VariantSerializer(data=data)
				if variant_serializer.is_valid():
					data_info = variant_serializer.save()
					info_msg = gettext_lazy("Vriant created successfully!!")
				else:
					print("something went wrong!!")
					return Response({
						"success": False, 
						"message": str(variant_serializer.errors),
						})
			final_result = []
			final_result.append(variant_serializer.data)
			return Response({
						"success": True, 
						"message": info_msg,
						"data": final_result,
						})
		except Exception as e:
			print("Variant creation/updation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})





class AddonAssociateCreationUpdation(APIView):
	"""
	Addon Details Creation & Updation POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create & update addon details within brand.

		Data Post: {
			"id"                   : "1",
			"associated_addons"    : [
				{
									"addon_name" : "Vegeterain Topping",
									"price"      : "45"
			},
			{
									"addon_name" : "Shudh Shakahari",
									"price"      : "25"
			}]
		}

		Response: {

			"success": True, 
			"message": "Addon group Association creation/updation api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			mutable = request.POST._mutable
			addon_data = {}
			request.POST._mutable = True
			data = request.data
			err_message = {}
			user = request.user.id
			cid = get_user(user)
			data['Company'] = cid
			err_message["id"] = \
					validation_master_anything(data["id"],
					"Addon Group",contact_re, 1)
			alld = AddonDetails.objects.filter(id=data['id'],Company=cid, active_status=1)
			if alld.count() == 0:
				return Response({
					"success": False,
					"message" : "Addon Group is not valid!!"		
					})
			addon_record = Addons.objects.filter(addon_group=data["id"])
			if addon_record.count() > 0:
				addon_record.delete()
			else:
				pass
			if len(data["associated_addons"]) != 0:
				for i in data['associated_addons']:
					if "addon_name" in i and "price" in i:
						pass
					else:
						err_message["addon_detail"] = \
					"addon name, price is not set!!"
						break
					err_message["addon_name"] = only_required(i["addon_name"],"Addon name")
					try:
						i["price"] = float(i["price"])
					except Exception as e:
						err_message["price"] = "Price is not valid!!"
					if i['price'] < 0:
						err_message["price"] = "Price is not valid!!"
					if any(err_message.values())==True:
						break
					addon_data['name']          = i['addon_name']
					addon_data['addon_amount']  = i['price']
					addon_data['addon_group']  = data['id']
					addon_data['identifier']  = data['identifier']
					addon_data['Company']  = cid
					addon_serializer = AddonSerializer(data=addon_data)
					if addon_serializer.is_valid():
						data_info = addon_serializer.save()
					else:
						print("something went wrong!!",addon_serializer.errors)
						return Response({
							"success": False, 
							"message": str(addon_serializer.errors),
							})			
			else:
				err_message["addon_detail"] = \
					"addon name, price is not set!!"
			if any(err_message.values())==True:
				return Response({
								"success": False,
								"error" : err_message,
								"message" : "Please correct listed errors!!"
							})
			addon_grp = {}
			addon_grp["associated_addons"] = data["associated_addons"]
			addon_serializer = \
			AddonDetailsSerializer(alld[0],data=addon_grp,partial=True)
			if addon_serializer.is_valid():
				data_info = addon_serializer.save()
				info_msg = "Addon Updated Successfully!!"
			else:
				print("something went wrong!!")
				return Response({
					"success": False, 
					"message": str(addon_serializer.errors),
					})
			return Response({
						"success": True, 
						"message": gettext_lazy("Addon Updated Successfully!!"),
						})
		except Exception as e:
			print("Addon group Association creation/updation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})






class ProductCreationUpdation(APIView):
	"""
	Product Creation & Updation POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create & update products.

		Data Post: {
			"id"                           : "1"(Send this key in update record case,else it is not required!!)
			"product_categorys"		       :  [],
			"product_subcategorys"          : [],
			"product_name"	       		   : "Cheese Burst",
			"food_type"                    : "1",
			"priority"                     : "1",
			"product_code"                 : "",
			"product_desc"                 : "",
			"kot_desc"                     : "",
			"short_desc"                   : "",
			"product_image"                : "pizza.jpg",
			"has_variant"                  : "true",
			"price"                        : "",
			"discount_price"               : "",
			"packing_charge"               : "",
			"variant_deatils"              : [
				{
									"name"           : "Large",
									"price"          : "245",
									"discount_price" : "209",
									"addon_group"    : [1,2,3]
			}],
			"addpn_grp_association"        : [1]
			"tax_association"              : [1,2],
			"tags"						   : [1,2],
			"is_recommended"               : "true",
			"included_platform"			   : ["swiggy","zomato"],
			"allergen_Information"		  : ["egg",""],
			"spice"                        : "dds",
			"primaryIngredient_deatils"    : [],
			"secondary_ingredient"         : [],
			"product_schema"              : [
				{
					"name"              : "calories",
					"quantity"          : "10",
					"unit"              : "gm",
								
			   }],
			"delivery_option"              : [
				{
					"isDelivery"              : "true",
					"isDineIn"                : "false",
					"isTakeaway"              : "true",
								
			   }],

		}

		Response: {

			"success": True, 
			"message": "Product creation/updation api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			auth_id = request.user.id
			cid = get_user(auth_id)
			if data['tab'] == str(0):
				data9 = json.loads(data["product_categorys"])
				data10 = json.loads(data["product_subcategorys"])
				data5 = json.loads(data["tax_association"])
				data["product_categorys"] = data9
				data["product_subcategorys"] = data10
				data["tax_association"] = data5
				validation_check = err_tab_check(data)
				if validation_check != None:
					return Response(validation_check)
				unique_check = unique_record_tab_check(data, cid)
				if unique_check != None:
					return Response(unique_check)
				data["active_status"] = 1
				if "id" in data:
					record = Product.objects.filter(id=data['id'])
					if record.count() == 0:
						return Response(
						{
							"success": False,
							"message": "Product data is not valid to update!!"
						}
						)
					else:
						record = Product.objects.filter(id=data['id'])
						p_query = \
						record.update(product_categorys=data["product_categorys"],\
						product_subcategorys=data["product_subcategorys"],
						product_name=data["product_name"],\
						food_type_id=data["food_type"],
						product_code=data["product_code"],
						ordering_code=data['ordering_code'],
						Company_id=cid,
						tax_association=data["tax_association"]
						)
						return Response(
								{
							"success": True,
							"message": "Product is created successfully!!!!",
							"product_id": data['id']
								}
							)
				else:
					chk_p = Product.objects.filter(Company_id=cid)
					if chk_p.count() > 0:
						max_priority = Product.objects.filter(Company_id=cid).aggregate(Max('priority'))
						priority = max_priority["priority__max"] + 1
					else:
						priority = 0
					p_query = \
					Product.objects.create(product_categorys=data["product_categorys"],\
					product_subcategorys=data["product_subcategorys"],
					product_name=data["product_name"],\
					food_type_id=data["food_type"],
					priority=priority,
					product_code=data["product_code"],
					Company_id=cid,
					tax_association=data["tax_association"]
					)
					return Response(
							{
					"success": True,
					"message": "Product is created successfully!!!!",
					"product_id": p_query.id
							}
							)
			if data['tab'] == str(1):
				record = Product.objects.filter(id=data['id'])
				data2 = json.loads(data["addpn_grp_association"])
				data3 = json.loads(data["variant_deatils"])
				data["addpn_grp_association"] = data2
				data["variant_deatils"] = data3
				validation_check = err_tab1_check(data)
				if validation_check != None:
					return Response(validation_check)
				unique_check = unique_record_tab1_check(data, cid)
				if unique_check != None:
					return Response(unique_check)
				data["updated_at"] = datetime.now()
				update_data = record.update(has_variant=data["has_variant"],
				price=data["price"],\
				variant_deatils=data["variant_deatils"],
				addpn_grp_association=data["addpn_grp_association"],\
				updated_at=datetime.now(),
				discount_price=data["discount_price"]
				)


				return Response(
							{
					"success": True,
					"message": "Product is created successfully!!!!",
					"product_id": data['id']
							}
							)
			if data['tab'] == str(2):
				record = Product.objects.filter(id=data['id'])
				data["updated_at"] = datetime.now()
				update_data = record.update(product_desc=data["product_desc"],
					kot_desc=data["kot_desc"],
					short_desc=data['short_desc'],
				)
				return Response(
							{
					"success": True,
					"message": "Product is created successfully!!!!",
					"product_id": data['id']
							}
							)
			if data['tab'] == str(3):
				record = Product.objects.filter(id=data['id'])
				data2 = json.loads(data["addpn_grp_association"])
				data4 = json.loads(data["tags"])
				data13 = json.loads(data["delivery_option"])
				data8 = json.loads(data["primaryIngredient_deatils"])
				data11 = json.loads(data["product_schema"])
				data6 = json.loads(data["included_platform"])
				data7 = json.loads(data["allergen_Information"])
				data["addpn_grp_association"] = data2
				data["tags"] = data4
				data["included_platform"] = data6
				data["allergen_Information"] = data7
				data["primaryIngredient_deatils"] = data8
				data["product_schema"] = data11			
				data["delivery_option"] = data13
				data["updated_at"] = datetime.now()
				validation_check = err_tag_check(data)
				if validation_check != None:
					return Response(validation_check)
				if data["is_recommended"] == "true":
					data["is_recommended"]= 1
				else:
					data["is_recommended"]= 0
				update_data = \
					record.update(
					is_recommended=data["is_recommended"],
					included_platform = data["included_platform"],
					allergen_Information=data['allergen_Information'],
					spice=data['spice'],
					primaryIngredient_deatils=data['primaryIngredient_deatils'],
					product_schema = data['product_schema'],
					delivery_option = data['delivery_option'],
					tags=data["tags"]
					)
				return Response(
							{
					"success": True,
					"message": "Product is created successfully!!!!",
					"product_id": data['id']
							}
							)
			if data['tab'] == str(4):
				record = Product.objects.filter(id=data['id'])
				validation_check = err_image_check(data)
				if validation_check != None:
					return Response(validation_check)
				if data["product_video"] != None and data["product_video"] != "":
					product = Product.objects.get(id=data["id"])
					product.pvideo = data["product_video"]
					product.save()
				else:
					pass
				video_url = record.update(video_url=data['video_url'])
				if "image0" not in data and "image1" not in data and "image2" not in data \
					and "image3" not in data and "image4" not in data:
					pass
				else:
					i_query = ProductImage.objects.filter(product_id=data['id'])
					i_query.delete()
					if "image0" in data:
						i_query = ProductImage.objects.create(product_image=data['image0'],\
								product_id=data['id'],primary_image=1)
					if "image1" in data:
						i_query = ProductImage.objects.create(product_image=data['image1'],\
								product_id=data['id'],primary_image=0)
					if "image2" in data:
						i_query = ProductImage.objects.create(product_image=data['image2'],\
							product_id=data['id'],primary_image=0)
					if "image3" in data:
						i_query = ProductImage.objects.create(product_image=data['image3'],\
							product_id=data['id'],primary_image=0)
					if "image4" in data:
						i_query = ProductImage.objects.create(product_image=data['image4'],\
							product_id=data['id'],primary_image=0)
				return Response(
							{
					"success": True,
					"message": "Product is created successfully!!!!",
					"product_id": data['id']
							}
							)
			if data['tab'] == str(5):
				err_message = {}
				data10 = json.loads(data["package_tax"])
				data['package_tax'] = data10
				if data['packing_amount'] == 'null':
					data['packing_amount'] =''
				record = Product.objects.filter(id=data['id'])
				if data['price_type'] == 'Fixed Price' or data['price_type'] == 'Percentage Price':
					err_message["packing_amount"] = only_required(data["packing_amount"],"Packaging Amount")
					if float(data['packing_amount']) < 0:
						err_message["packing_amount"] = "Packaging charge is not valid!!"

					if data['isPackageTax'] =='true' :
						if len(data['package_tax']) == 0:
							err_message["package_tax"] = 'Please choose applicable tax(es)!!'
					else:
						pass
					if any(err_message.values())==True:
						return Response({
							"success": False,
							"error" : err_message,
							"message" : "Please correct listed errors!!"
							})
					if data['isPackageTax'] == 'true':
						data['isPackageTax'] = 1
					else:
						data['isPackageTax'] = 0
					record.update(price_type=data['price_type'],packing_amount=data['packing_amount'],\
						package_tax=data['package_tax'],is_tax=data['isPackageTax'])
				return Response(
							{
					"success": True,
					"message": gettext_lazy("Product is created successfully!!!!"),
					"product_id": data['id']
							})

		except Exception as e:
			print("Product creation/updation Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})


class RatingUpdate(APIView):
	"""

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			import random
			arr = [3.8, 3.9, 4.0, 4.1, 4.3, 4.5]
			auth_id = request.user.id
			cid = get_user(auth_id)
			product_data = Product.objects.filter(Company_id=cid)
			for index in product_data:
				record = Product.objects.filter(id=index.id)
				rating =  random.choice(arr)
				s=record.update(rating=rating)
			return Response(
							{
					"success": True,
							})
		except Exception as e:
			print("Product creation/updation Api Stucked into exception!!")
			print(e)





class AddonCreation(APIView):
	"""
	Addon post API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create addon.


		Request Body for update(Put method)

		Data Post: {

			"name"		                   :  "Pizza",
			"addon_amount"                 

		}
	"""
	serializer_class = AddonSerializer
	queryset = Addons.objects.all()
	def post(self, request):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			serializer = AddonSerializer(data=data)
			if serializer.is_valid(raise_exception=True):
				serializer.save()
				return Response(
					{"success": True, 
					"message": gettext_lazy("Addon is created successfully!!")},
					status=HTTP_200_OK,
				)
		except Exception as e:
			return Response(
				{"success": False, "message": str(e)}, status=HTTP_406_NOT_ACCEPTABLE
			)


class AddonUpdation(APIView):
	"""
	Addon Updation PUT API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to  update Addon.


		Request Body for update(Put method)

		Data Post: {
			"id"                   		   : "1",
			"name"		                   : "Pizza",
			"addon_amount"		           : "50",   (optional)

		}
	"""
	serializer_class = AddonSerializer
	queryset = Addons.objects.all()
	def put(self, request):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			addon = Addons.objects.filter(id=data["id"])
			if addon.count() == 0:
				raise Exception(gettext_lazy("No Major Addons with given id."))
			serializer = AddonSerializer(addon[0], data=data, partial=True)
			if serializer.is_valid(raise_exception=True):
				serializer.save()
				return Response(
					{"success": True, "message": gettext_lazy("Addons Updated.")},
					status=HTTP_200_OK,
				)
		except Exception as e:
			return Response(
				{"success": False, "message": str(e)}, status=HTTP_406_NOT_ACCEPTABLE
			)

class AddonListApi(ListAPIView):
	"""
	Addon List API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to get a list of addons.

	"""
	permission_classes = (IsAuthenticated,)
	serializer_class = AddonSerializer
	queryset = Addons.objects.all().order_by('id')

class AddonRetrieve(RetrieveAPIView):
	"""
	Addon Retrieve API View

		Service usage and description : This API is used to retrieve addon info.
		Authentication Required : YES
	"""
	permission_classes = (IsAuthenticated,)
	serializer_class = AddonsSerializer
	queryset = Addons.objects.all()




class AddongroupCreation(APIView):
	"""
	Addon group post API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to create addon group.


		Request Body for create(Post method)

		Data Post: {
			"addon_gr_name"                : "text"
			"min_addons"				   : ""
			"max_addons"				   : ""
			"description"				   : ""
			"addons"		               :  [],
			"addon_amount"                 

		}
	"""
	serializer_class = AddongroupSerializer
	queryset = Addons.objects.all()
	def post(self, request):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			serializer = AddongroupSerializer(data=data)
			if serializer.is_valid(raise_exception=True):
				serializer.save()
				return Response(
					{"success": True, 
					"message": gettext_lazy("Addon group is created successfully!!")},
					status=HTTP_200_OK,
				)
		except Exception as e:
			return Response(
				{"success": False, "message": str(e)}, status=HTTP_406_NOT_ACCEPTABLE
			)



class AddongroupUpdation(APIView):
	"""
	Addon group Updation PUT API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to  update Addon group.


		Request Body for update(Put method)

		Data Post: {
			"id"                   		   : "1",
			"addon_gr_name"                : "text"
			"min_addons"				   : ""
			"max_addons"				   : ""
			"description"				   : ""
			"addons"		               :  [],
               

		}
	"""
	serializer_class = AddonDetailsSerializer
	queryset = AddonDetails.objects.all()
	def put(self, request):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			addon = AddonDetails.objects.filter(id=data["id"])
			if addon.count() == 0:
				raise Exception(gettext_lazy("No Major Addons with given id."))
			serializer = AddongroupSerializer(addon[0], data=data, partial=True)
			if serializer.is_valid(raise_exception=True):
				serializer.save()
				return Response(
					{"success": True, "message": gettext_lazy("Addon group Updated.")},
					status=HTTP_200_OK,
				)
		except Exception as e:
			return Response(
				{"success": False, "message": str(e)}, status=HTTP_406_NOT_ACCEPTABLE
			)

class AddongroupListApi(ListAPIView):
	"""
	Addon Group List API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to get a list of addon group.

	"""
	permission_classes = (IsAuthenticated,)
	serializer_class = AddongroupSerializer
	queryset = AddonDetails.objects.all().order_by('id')




class CategoryDeleteImage(DestroyAPIView):
    """
    Cateory image Deletion DELETE API

        Service Usage and Description : This API is used to delete cateory.
        Authentication Required : YES

        Data : {
            "id" : "1"
        }

        Response : {
            "success" : True,
            "message" : "Category Image Deleted."
        }
    """

    permission_classes = (IsAuthenticated,)
    serializer_class = ProductsubCategorySerializer

    def get_queryset(self):
        queryset = ProductCategory.objects.filter(id=self.request.data["id"])
        return queryset

    def delete(self, request):
        try:
            category = self.get_queryset()
            if category.count() == 0:
                raise Exception("No Category with given id.")
            category_data = ProductCategory.objects.filter(id=self.request.data["id"])
            category_data.update(category_image=None)
            return Response(
                {"success": True, "message": "Category Deleted."},
                status=HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"success": False, "message": str(e)}, status=HTTP_406_NOT_ACCEPTABLE
            )
