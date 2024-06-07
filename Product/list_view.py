from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.sites.shortcuts import get_current_site
from ZapioApi.Api.BrandApi.profile.profile import CompanySerializer
from Brands.models import Company
import requests

#Serializer for api
from rest_framework import serializers
from Product.models import *
from rest_framework.authtoken.models import Token
from Location.models import CityMaster, AreaMaster
from UserRole.models import ManagerProfile
from Outlet.models import *
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user,ProductStatus
from ZapioApi.api_packages import *
from zapio.settings import Media_Path
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q




class Productlisting(APIView):
	"""
	Product Listing POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to provide product Listing.

		Data Post: {

			"status"   ; "true"
		}

		Response: {

		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			user = request.user.id
			cid = get_user(user)
			if data['status'] == True:
				query = Product.objects.\
						filter(Q(Company_id=cid),Q(active_status=1),Q(is_hide=0)).order_by('-created_at')
			else:
				query = Product.objects.\
						filter(Company_id=cid,active_status=0,is_hide=0).order_by('-created_at')
			catagory_conf_data_serializer = []
			for q in query:
				q_dict = {}
				q_dict["id"] = q.id
				if q.food_type_id != None:
					domain_name = addr_set()
					f = FoodType.objects.filter(id=q.food_type_id)
					q_dict["FoodType_name"] = f[0].food_type
					q_dict["FoodType_image"] = domain_name + str(f[0].foodtype_image) 
				else:
					q_dict["FoodType_name"] = ''
				q_dict["priority"] = q.priority
				q_dict["product_code"] = q.product_code
				q_dict["product_name"] = q.product_name
				q_dict["product_desc"] = q.product_desc 
				pstatus = ProductStatus(q.id,cid)
				q_dict["product_weight"] = pstatus
				cat = q.product_categorys
				q_dict['category'] = []
				if len(cat) > 0:
					for index in cat:
						cat = {}
						cat_name = ProductCategory.objects.filter(id=index)[0]
						cat['id'] = cat_name.id
						cat['name'] = cat_name.category_name
						q_dict['category'].append(cat)
				else:
					pass
				sub = q.product_subcategorys
				q_dict['subcategory'] = []
				if len(sub) > 0:
					for index in sub:
						cat = {}
						cat_name = ProductsubCategory.objects.filter(id=index)[0]
						cat['id'] = cat_name.id
						cat['name'] = cat_name.subcategory_name
						q_dict['subcategory'].append(cat)
				else:
					pass
				chk_imag = ProductImage.objects.filter(product_id=q.id,primary_image=1)
				if chk_imag.count() > 0:
					q_dict['primary_image'] = Media_Path+str(chk_imag[0].product_image)
				else:
					q_dict['primary_image'] = None
				chk_img = ProductImage.objects.filter(product_id=q.id,primary_image=0)
				if chk_img.count() > 0:
					q_dict['multiple_image'] = []
					for index in chk_img:
						q_dict['multiple_image'].append(Media_Path+str(chk_imag[0].product_image))
				else:
					q_dict['multiple_image'] = []
				has_variant = q.has_variant
				variant_deatils = q.variant_deatils
				if has_variant == False:
					q_dict["price"] = q.price
					q_dict["compare_price"] = q.discount_price
					q_dict["is_customize"] = 0
				else:
					li =[]
					li2 = []
					if variant_deatils != None:
						for j in variant_deatils:
							li.append(j["price"])
							li2.append(j["discount_price"])
						q_dict["price"] = min(li)
						q_dict["compare_price"] = min(li2)
						q_dict["Variant_id"] = \
						Variant.objects.filter(variant__iexact=variant_deatils[0]["name"])[0].id
						q_dict["Variant_name"] = variant_deatils[0]["name"]
						q_dict["is_customize"] = 1
				q_dict['created_at'] = q.created_at.strftime("%d/%b/%y")
				if q.updated_at != None:
					q_dict['updated_at'] = q.updated_at.strftime("%d/%b/%y")
				q_dict["active_status"] = q.active_status
				catagory_conf_data_serializer.append(q_dict)
			return Response(
					{
						"success": True,
						"data" : catagory_conf_data_serializer,
						"message": "Product details fetching successful!!"
					}
					)
		except Exception as e:
			print("Product details configuration Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})



class CatagoryListing(APIView):
	"""
	Catagory listing Configuration POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to provide all Catagory within brand.

		Data Post: {

			"company_auth_id" 	    : "3",
			"status"   ; "true"
		}

		Response: {

			"success": True,
			"data" : catagory_conf_data_serializer,
			"message": "Catagory fetching successful!!"
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			user = request.user.id
			cid = get_user(user)
			if data['status'] == True:
				query = ProductCategory.objects.\
						filter(Company=cid,active_status=1,is_hide=0).order_by('-created_at')
			else:
				query = ProductCategory.objects.\
						filter(Company=cid,active_status=0,is_hide=0).order_by('-created_at')

			catagory_conf_data_serializer = []
			for q in query:
				q_dict = {}
				q_dict["id"] = q.id
				q_dict["category_name"] = q.category_name 
				q_dict["outlet_map"] = q.outlet_map
				q_dict["priority"] = q.priority
				q_dict["category_code"] = q.category_code
				scount = ProductsubCategory.objects.filter(category_id=q.id).count()
				if scount > 0:
					q_dict['sub_category_count'] = scount
				else:
					q_dict['sub_category_count'] = 0
				a = str(q.id)
				pcount = Product.objects.filter(product_categorys__exact=[str(a)],\
					Company_id=cid)
				if pcount.count() > 0:
					q_dict['product_count'] = pcount.count()
				else:
					q_dict['product_count'] = 0
				domain_name = addr_set()
				cat_img = str(q.category_image)
				if cat_img != "" and cat_img != None and cat_img != "null":
					full_path = domain_name + str(q.category_image)
					q_dict['category_image'] = full_path
				else:
					q_dict['category_image'] = ''
				q_dict["active_status"] = q.active_status
				catagory_conf_data_serializer.append(q_dict)
			return Response(
					{
						"success": True,
						"data" : catagory_conf_data_serializer,
						"message": "Catagory fetching successful!!"
					}
					)
		except Exception as e:
			print("Catagory listing configuration Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})



class SubCatagoryListing(APIView):
	"""
	Sub-Catagory listing Configuration POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to provide all Sub-Catagory within catagory.

		Data Post: {

			"cat_id" 	    : "3"
		}

		Response: {

			"success": True,
			"data" : subcatagory_conf_data_serializer,
			"message": "Sub-Catagory fetching successful!!"
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			err_message = {}
			err_message["cat_id"] = \
					validation_master_anything(data["cat_id"],
					"Catagory ID",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			query = ProductsubCategory.objects.filter(category=data["cat_id"]).order_by('-created_at')
			subcatagory_conf_data_serializer = []
			for q in query:
				q_dict = {}
				q_dict["id"] = q.id
				q_dict["category_id"] = q.category_id 
				q_dict["subcategory_name"] = q.subcategory_name
				q_dict["active_status"] = q.active_status
				domain_name = addr_set()
				sub_img = str(q.subcategory_image)
				if sub_img != "" and sub_img != None and sub_img != "null":
					full_path = domain_name + str(q.subcategory_image)
					q_dict['subcategory_image'] = full_path
				else:
					q_dict['subcategory_image'] = ''
				subcatagory_conf_data_serializer.append(q_dict)
			return Response(
					{
						"success": True,
						"data" : subcatagory_conf_data_serializer,
						"message": "Sub-Catagory fetching successful!!"
					}
					)
		except Exception as e:
			print("Sub-Catagory listing configuration Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})



class CatagoryWiseOutletListing(APIView):
	"""
	Catagory listing Configuration POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to provide all outlets mapped with catagory.

		Data Post: {

			"cat_id" 	    : "3"
		}

		Response: {

			"success": True,
			"data" : catwise_serializer,
			"message": "Catagorywise outlet fetching successful!!"
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			err_message = {}
			err_message["cat_id"] = \
					validation_master_anything(data["cat_id"],
					"Catagory ID",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			query = ProductCategory.objects.filter(id=data["cat_id"]).order_by('-created_at')
			if query.count()==0:
				return Response(
					{
						"success": False,
						"message": "Category id is not valid to list out associated outlets!!"
					}
					) 
			else:
				data_info = query[0].outlet_map
				catwise_serializer = []
				for i in data_info:
					q_dict = {}
					outlet_info = OutletProfile.objects.filter(id=i,active_status=1)
					q_dict["id"] = outlet_info[0].id
					q_dict["outlet_name"] = outlet_info[0].Outletname
					catwise_serializer.append(q_dict)
			return Response(
					{
						"success": True,
						"data" : catwise_serializer,
						"message": "Catagorywise outlet fetching successful!!"
					}
					)
		except Exception as e:
			print("Catagorywise outlet fetching Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})


class CatagoryWiseSubCategoryListing(APIView):
	"""
	CatagoryWise Sub-Catagory listing Configuration POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to provide all sub-category mapped with catagory.

		Data Post: {

			"cat_id" 	    : "3"
		}

		Response: {

			"success": True,
			"data" : catwise_serializer,
			"message": "CatagoryWise Sub-Catagory listing api worked well!!"
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			err_message = {}
			err_message["cat_id"] = \
					validation_master_anything(data["cat_id"],
					"Catagory ID",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			query = ProductsubCategory.objects.filter(category=data["cat_id"]).order_by('-created_at')
			if query.count()==0:
				return Response(
					{
						"data" : [],
						"success": True,
						"message": "Category id is not valid to list out associated Sub-Catagory!!"
					}
					) 
			else:
				catwise_serializer = []
				for i in query:
					q_dict = {}
					q_dict["id"] = i.id
					q_dict["category"] = i.category_id
					q_dict["category_name"] = i.category.category_name
					q_dict["subcategory_name"] = i.subcategory_name
					q_dict["active_status"] = i.active_status
					q_dict["created_at"] = i.created_at
					q_dict["updated_at"] = i.updated_at
					catwise_serializer.append(q_dict)
			return Response(
					{
						"success": True,
						"data" : catwise_serializer,
						"message": "CatagoryWise Sub-Catagory listing api worked well!!"
					}
					)
		except Exception as e:
			print("CatagoryWise Sub-Catagory listing api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})




class CityWiseAreaListing(APIView):
	"""
	CityWise Area listing Configuration POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to provide all areas mapped with city.

		Data Post: {

			"id" 	    : "1"
		}

		Response: {

			"success": True,
			"data" :  serializer,
			"message": "CityWise Area listing api worked well!!"
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			data = request.data
			err_message = {}
			err_message["id"] = \
					validation_master_anything(data["id"],
					"City ID",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			query = AreaMaster.objects.filter(city=data["id"],active_status=1)
			if query.count()==0:
				return Response(
					{
						"success": False,
						"message": "City id is not valid to list out associated areas!!"
					}
					) 
			else:
				serializer = []
				for i in query:
					q_dict = {}
					q_dict["id"] = i.id
					q_dict["city"] = i.city_id
					q_dict["city_name"] = i.city.city
					q_dict["area"] = i.area
					q_dict["active_status"] = i.active_status
					q_dict["created_at"] = i.created_at
					q_dict["updated_at"] = i.updated_at
					serializer.append(q_dict)
			return Response(
					{
						"success": True,
						"data" : serializer,
						"message": "CityWise Area listing api worked well!!"
					}
					)
		except Exception as e:
			print("CityWise Area listing api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})




class AssociateAddon(APIView):
	"""
	Associated addons POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to provide associated addon details within brand.

		Data Post: {
			"id"                   : "94"
		}

		Response: {

			"success": True, 
			"message": "Associated addons details api worked well!!",
			"data": final_result
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			mutable = request.POST._mutable
			request.POST._mutable = True
			data = request.data
			data["id"] = str(data["id"])
			err_message = {}
			err_message["addon"] = \
					validation_master_anything(data["id"],
					"Addon Group Name",contact_re, 1)
			if any(err_message.values())==True:
				return Response({
					"success": False,
					"error" : err_message,
					"message" : "Please correct listed errors!!"
					})
			addon_query = AddonDetails.objects.filter(id=data['id'])
			if addon_query.count() != 0:
				pass
			else:
				return Response(
					{
						"success": False,
	 					"message": "Addon Id is not valid!!"
					}
					)
			final_result = addon_query[0].associated_addons
			final_data = []
			for i in final_result:
				aa = {}
				if 'addon_name' in i:
					name = i['addon_name']
					aa['name'] = name
					aa['price'] = i['price']
					addon_data = Addons.objects.filter(Q(name=name),Q(addon_amount=aa['price']),\
						Q(addon_group_id=data['id']),Q(is_hide=0))
					if addon_data.count() > 0:
						aa['id'] = addon_data[0].id
						aa['identifier'] = addon_data[0].identifier
						aa['active_status'] = addon_data[0].active_status
						aa['is_hide'] = addon_data[0].is_hide

					final_data.append(aa)
			return Response({
						"success": True, 
						"message": "Associated addons details api worked well!!",
						"data": final_data,
						})
		except Exception as e:
			print("Associated addons Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})

