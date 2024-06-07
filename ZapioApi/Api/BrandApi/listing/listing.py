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







class CompanySerializer(serializers.ModelSerializer):
	def to_representation(self, instance):
		representation = super(CompanySerializer, self).to_representation(instance)
		representation['created_at'] = instance.created_at.strftime("%d/%b/%y")
		domain_name = addr_set()
		representation['company_logo'] = str(instance.company_logo)
		if representation['company_logo'] != "" and representation['company_logo'] != None:
			full_path = domain_name + str(instance.company_logo)
			representation['company_logo'] = full_path
		else:
			pass
		representation['company_landing_imge'] = str(instance.company_landing_imge)
		if representation['company_landing_imge'] != "" and representation['company_landing_imge'] != None:
			full_path_banner = domain_name + str(instance.company_landing_imge)
			representation['company_landing_imge'] = full_path_banner
		else:
			pass			
		if instance.updated_at != None:
			representation['updated_at'] = instance.updated_at.strftime("%d/%b/%y")
		else:
			pass
		return representation
	class Meta:
		model = Company
		fields = '__all__'

class VariantlistingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Variant
		fields = '__all__'

class FoodTypelistingSerializer(serializers.ModelSerializer):
	def to_representation(self, instance):
		representation = super(FoodTypelistingSerializer, self).to_representation(instance)
		representation['created_at'] = instance.created_at.strftime("%d/%b/%y")
		domain_name = addr_set()
		representation['foodtype_image'] = str(instance.foodtype_image)
		if representation['foodtype_image'] != "" and representation['foodtype_image'] != None\
			and representation['foodtype_image'] != "null":
			full_path = domain_name + str(instance.foodtype_image)
			representation['foodtype_image'] = full_path
		else:
			pass
		if instance.updated_at != None:
			representation['updated_at'] = instance.updated_at.strftime("%d/%b/%y")
		else:
			pass
		return representation

	class Meta:
		model = FoodType
		fields = '__all__'

class AddonDetailslistingSerializer(serializers.ModelSerializer):
	# variant_name = serializers.ReadOnlyField(source='product_variant.variant')

	# def to_representation(self, instance):
	# 	representation = super(AddonDetailslistingSerializer, self).to_representation(instance)
	# 	if instance.product_variant != None:
	# 		representation['addon_gr_name'] = \
	# 		str(instance.addon_gr_name)
	# 	else:
	# 		pass
	# 	return representation

	class Meta:
		model = AddonDetails
		fields = ['id','addon_gr_name','min_addons','max_addons','active_status','description']







class CitylistingSerializer(serializers.ModelSerializer):
	class Meta:
		model = CityMaster
		fields = ['id','city']

class CountrylistingSerializer(serializers.ModelSerializer):
	class Meta:
		model = CountryMaster
		fields = ['id','country']


class AreaMasterlslistingSerializer(serializers.ModelSerializer):
	class Meta:
		model = AreaMaster
		fields = '__all__'

class ProductlistingSerializer(serializers.ModelSerializer):
	category_name = serializers.ReadOnlyField(source='product_category.category_name')
	subcategory_name = serializers.ReadOnlyField(source='product_subcategory.subcategory_name')
	FoodType_name = serializers.ReadOnlyField(source='food_type.food_type')
	def to_representation(self, instance):
		representation = super(ProductlistingSerializer, self).to_representation(instance)
		representation['created_at'] = instance.created_at.strftime("%d/%b/%y")
		domain_name = addr_set()
		representation['product_image'] = str(instance.product_image)
		if representation['product_image'] != "" and representation['product_image'] != None\
			and representation['product_image'] != "null":
			full_path = domain_name + str(instance.product_image)
			representation['product_image'] = full_path
		else:
			pass
		if instance.updated_at != None:
			representation['updated_at'] = instance.updated_at.strftime("%d/%b/%y")
		else:
			pass
		return representation


	class Meta:
		model = Product
		fields = ['id','category_name','subcategory_name','FoodType_name','priority','product_code',\
				'product_name','product_desc','product_image','active_status','created_at','updated_at']

class ProductsubCategorySerializer(serializers.ModelSerializer):
	category_name = serializers.ReadOnlyField(source='category.category_name')

	def to_representation(self, instance):
		representation = super(ProductsubCategorySerializer, self).to_representation(instance)
		representation['created_at'] = instance.created_at.strftime("%d/%b/%y")
		
		domain_name = addr_set()
		representation['subcategory_image'] = str(instance.subcategory_image)
		if representation['subcategory_image'] != "" and representation['subcategory_image'] != None\
			and representation['subcategory_image'] != "null":
			full_path = domain_name + str(instance.subcategory_image)
			representation['subcategory_image'] = full_path
		else:
			representation['subcategory_image'] = ''

		if instance.updated_at != None:
			representation['updated_at'] = instance.updated_at.strftime("%d/%b/%y")
		else:
			pass
		return representation

	class Meta:
		model = ProductsubCategory
		fields = ['id','category_name','category_id','priority','description','subcategory_name','active_status','created_at','updated_at']

	# def get_cat_id(self, obj):
	# 	print("pppppppppppppppp",obj.id)



def site_addr(request):
	current_site = get_current_site(request)
	domain = current_site.domain
	return domain


class Variantlisting(ListAPIView):
	"""
	Variant listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of Variant data within brand.
	"""
	permission_classes = (IsAuthenticated,)
	serializer_class = VariantlistingSerializer

	def get_queryset(self):
		user = self.request.user.id
		ch_brand = Company.objects.filter(auth_user_id=user)
		if ch_brand.count() > 0:
			nuser=user
		else:
			pass
		ch_cashier = ManagerProfile.objects.filter(auth_user_id=user)
		if ch_cashier.count() > 0:
			company_id = ch_cashier[0].Company_id
			auth_user_id = Company.objects.filter(id=company_id)[0].auth_user_id
			nuser=auth_user_id
		else:
			pass
		queryset = Variant.objects.all().order_by('-created_at')
		return queryset.filter(Company__auth_user=nuser)


class FoodTypelisting(ListAPIView):
	"""
	FoodType listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of FoodType data.
	"""
	permission_classes = (IsAuthenticated,)
	queryset = FoodType.objects.all().order_by('-created_at')
	serializer_class = FoodTypelistingSerializer







class AddonDetailslisting(APIView):
	"""
	AddonDetails POST API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to provide AddonDetails.

		Data Post: {

			"status"   ; "true"
		}

		Response: {

			"success": True,
			"data" : AddonDetails_data_serializer,
			"message": "Addon detail successful!!"
		}

	"""
	permission_classes = (IsAuthenticated,)
	def post(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			user = request.user.id
			is_outlet = OutletProfile.objects.filter(auth_user_id=user)
			is_brand = Company.objects.filter(auth_user_id=user)
			is_cashier = ManagerProfile.objects.filter(auth_user_id=user)
			if is_cashier.count() > 0:
				cid = ManagerProfile.objects.filter(auth_user_id=user)[0].Company_id
			else:
				pass
			if is_outlet.count() > 0:
				outlet = OutletProfile.objects.filter(auth_user_id=user)
				cid = outlet[0].Company_id
			else:
				pass
			if is_brand.count() > 0:
				outlet = Company.objects.filter(auth_user_id=user)
				cid = outlet[0].id
			else:
				pass
			if data['status'] == True:
				query = AddonDetails.objects.\
						filter(Company_id=cid,active_status=1).order_by('-created_at')
			else:
				query = AddonDetails.objects.\
						filter(Company_id=cid,active_status=0).order_by('-created_at')

			catagory_conf_data_serializer = []
			for q in query:
				q_dict = {}
				q_dict["id"] = q.id
				q_dict["description"] = q.description 
				q_dict["active_status"] = q.active_status
				q_dict["max_addons"] = q.max_addons
				q_dict["min_addons"] = q.min_addons
				q_dict["priority"] = q.priority
				q_dict["addon_gr_name"] = q.addon_gr_name
				addon_data = Addons.objects.filter(addon_group_id=q.id)
				if addon_data.count() > 0:
					q_dict["count_addon"] = addon_data.count()
				else:
					q_dict["count_addon"] = 0
				a = Variant.objects.filter(id=q.product_variant_id)
				if a.count() > 0:
					q_dict["variant_name"] = a[0].variant
				else:
					q_dict["variant_name"] = ''


				catagory_conf_data_serializer.append(q_dict)
			return Response(
					{
						"success": True,
						"data" : catagory_conf_data_serializer,
						"message": "Addon details fetching successful!!"
					}
					)
		except Exception as e:
			print("Addon details configuration Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})

class Citylisting(ListAPIView):
	"""
	City listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of Cities.
	"""
	permission_classes = (IsAuthenticated,)

	def get_queryset(self):
		queryset = CityMaster.objects.filter(active_status=1)
		return queryset

	def list(self, request):
		queryset = self.get_queryset()
		serializer = CitylistingSerializer(queryset, many=True)
		response_list = serializer.data 
		return Response({
					"success": True,
					"data" : response_list,
					"message" : "City listing API worked well!!"})

class Countrylisting(ListAPIView):
	"""
	Country listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of Country.
	"""
	permission_classes = (IsAuthenticated,)

	def get_queryset(self):
		queryset = CountryMaster.objects.filter(active_status=1)
		return queryset

	def list(self, request):
		queryset = self.get_queryset()
		serializer = CountrylistingSerializer(queryset, many=True)
		response_list = serializer.data 
		return Response({
					"success": True,
					"data" : response_list,
					"message" : "Country listing API worked well!!"})



class Productlistings(APIView):
	"""
	Product Listing get API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used to provide product Listing.

	    Params:  {
			"page_no": 1,
			"page_size": 10,
			"status"  : True,
			"product_name" : "",
			"filter_by"    : "product_name",
			"sort"        : 
			"sort_by"     : 'id/ product_name'
		}

		Response: {

		}

	"""
	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			from Brands.models import Company
			data = request.data
			user = request.user.id
			cid = get_user(user)
			status= self.request.GET.get("status")
			p_no  = self.request.GET.get("page_no")
			p_size = self.request.GET.get("page_size")
			product_name     = self.request.GET.get("product_name")
			filter_by        = self.request.GET.get("filter_by")
			sort             = self.request.GET.get("sort")
			sort_by          = self.request.GET.get("sort_by")
			page_no = 1
			page_size = 10
			if status == 'true':
				query = Product.objects.\
						filter(Company_id=cid,active_status=1,is_hide=0).order_by('-created_at')
			else:
				query = Product.objects.\
						filter(Company_id=cid,active_status=0,is_hide=0).order_by('-created_at')

			if product_name != None and filter_by != None:
				query = query.filter(product_name__icontains=product_name)
		
			if sort != None and sort_by != None:
				if sort == 'ascending':
					query = query.order_by(sort_by)
				else:
					query = query.order_by('-'+str(sort_by))
			if p_no != None:
				page_no = int(self.request.GET.get("page_no"))
			if p_size != None:
				page_size = int(self.request.GET.get("page_size"))
			try:
				if page_size > 200:
					page_size = 200
				pages = Paginator(query, page_size)
				query_data = pages.page(page_no)
			except PageNotAnInteger:
				page_no = 1
				query_data = pages.page(page_no)
			except EmptyPage:
				page_no = pages.num_pages
				query_data = pages.page(page_no)

			page_count = pages.count
			page_info = {
				"page_no": page_no,
				"page_size": page_size,
				"total_pages" : pages.num_pages
			}
			final_data = []
			catagory_conf_data_serializer = []
			for q in range(len(query_data.object_list)):
				q_dict = {}
				q_dict["id"] = query_data[q].id
				if query[q].food_type_id != None:
					domain_name = addr_set()
					f = FoodType.objects.filter(id=query_data[q].food_type_id)
					q_dict["FoodType_name"] = f[0].food_type
					q_dict["FoodType_image"] = domain_name + str(f[0].foodtype_image) 
				else:
					q_dict["FoodType_name"] = ''
				q_dict["priority"] = query_data[q].priority
				q_dict["product_code"] = query_data[q].product_code
				q_dict["product_name"] = query_data[q].product_name
				q_dict["product_desc"] = query_data[q].product_desc 
				pstatus = ProductStatus(query_data[q].id,cid)
				q_dict["product_weight"] = pstatus
				cat = query_data[q].product_categorys
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
				try:
					sub = query_data[q].product_subcategorys
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
				except Exception as e:
					pass
				chk_imag = ProductImage.objects.filter(product_id=query_data[q].id,primary_image=1)
				if chk_imag.count() > 0:
					q_dict['primary_image'] = Media_Path+str(chk_imag[0].product_image)
				else:
					q_dict['primary_image'] = None
				chk_img = ProductImage.objects.filter(product_id=query_data[q].id,primary_image=0)
				if chk_img.count() > 0:
					q_dict['multiple_image'] = []
					for index in chk_img:
						q_dict['multiple_image'].append(Media_Path+str(chk_imag[0].product_image))
				else:
					q_dict['multiple_image'] = []
				has_variant = query_data[q].has_variant
				variant_deatils = query_data[q].variant_deatils
				if has_variant == False:
					q_dict["price"] = query_data[q].price
					q_dict["compare_price"] = query_data[q].discount_price
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
				q_dict['created_at'] = query_data[q].created_at.strftime("%d/%b/%y")
				if query_data[q].updated_at != None:
					q_dict['updated_at'] = query_data[q].updated_at.strftime("%d/%b/%y")
				q_dict["active_status"] = query_data[q].active_status
				catagory_conf_data_serializer.append(q_dict)
			return Response(
					{
						"success": True,
						"data" : catagory_conf_data_serializer,
						"page": page_info,
						"message": "Product details fetching successful!!"
					}
					)
		except Exception as e:
			print("Product details configuration Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})

















class SubCategorylisting(APIView):
	"""
	Sub-Category listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of Sub-Category.
	"""
	permission_classes = (IsAuthenticated,)

	def get(self,request):
		user = self.request.user
		cat_id = request.GET.get('id')
		user = user.id
		cid = get_user(user)
		if cat_id:
			queryset = ProductsubCategory.objects.filter(category__Company=cid,category_id=cat_id).order_by('-created_at')
		else:
			queryset = ProductsubCategory.objects.filter(category__Company=cid).order_by('-created_at')

		serializer = ProductsubCategorySerializer(queryset, many=True)
		response_list = serializer.data 
		return Response({
					"success": True,
					"data" : response_list,
					"message" : "Sub-Category listing API worked well!!"})













class Companylisting(ListAPIView):
	"""
	Company detail listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for providing the profile details of brand.
	"""
	permission_classes = (IsAuthenticated,)

	def get_queryset(self):
		user = self.request.user
		auth_id = user.id
		Company_id = get_user(auth_id)
		queryset = Company.objects.filter(active_status=1, id=Company_id)
		return queryset

	def list(self, request):
		queryset = self.get_queryset()
		serializer = CompanySerializer(queryset, many=True)
		response_list = serializer.data 
		return Response({
					"success": True,
					"data" : response_list,
					"message" : "Company profile detail API worked well!!"})



class FeatureListing(APIView):
	"""
	User listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of featured product data within brand.
	"""
	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			user = request.user.id
			ch_brand = Company.objects.filter(auth_user_id=user)
			if ch_brand.count() > 0:
				nuser=user
			else:
				pass
			ch_cashier = ManagerProfile.objects.filter(auth_user_id=user)
			if ch_cashier.count() > 0:
				company_id = ch_cashier[0].Company_id
				auth_user_id = Company.objects.filter(id=company_id)[0].auth_user_id
				nuser=auth_user_id
			else:
				pass
			record = FeatureProduct.objects.filter(company__auth_user=nuser)
			final_result = []
			if record.count() > 0:
				for i in record:
					feature_dict = {}
					feature_dict['outlet'] = i.outlet.Outletname
					feature_dict['id'] = i.id
					featured = i.feature_product
					featured_list = []
					if len(featured) != 0:
						for j in featured:
							q = Product.objects.filter(id=j,active_status=1)
							featured_list\
							.append(q[0].product_name+" | "+q[0].product_category.category_name)
					else:
						feature_dict["featured"] = None
					if len(featured_list) != 0:
						feature_dict["featured"] = \
						', '.join([str(elem) for elem in featured_list])
					else:
						feature_dict["featured"] = None
					feature_dict['active_status'] = i.active_status
					final_result.append(feature_dict)
				return Response({
						"success": True, 
						"data": final_result})
			else:
				return Response({
						"success": True, 
						"data": []})
		except Exception as e:
			print("Feature listing Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})






