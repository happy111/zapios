from ZapioApi.Api.BrandApi.listing.listing import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.sites.shortcuts import get_current_site
from ZapioApi.Api.BrandApi.profile.profile import CompanySerializer
from Brands.models import Company
from Outlet.models import OutletProfile
from Product.models import Variant, FoodType, AddonDetails, Product, ProductsubCategory,\
ProductCategory
from django.db.models import Q
from rest_framework import serializers
from kitchen.models import Ingredient
from ZapioApi.Api.BrandApi.ordermgmt.order_fun import get_user

class CategorylistingSerializer(serializers.ModelSerializer):
	# company_name = serializers.ReadOnlyField(source='Company.company_name')
	class Meta:
		model = ProductCategory
		fields = '__all__'

class OutletlistingSerializer(serializers.ModelSerializer):
	# company_name = serializers.ReadOnlyField(source='Company.company_name')
	class Meta:
		model = OutletProfile
		fields = '__all__'


class ProductlistingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Product
		fields = '__all__'


class IngredientlistingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Ingredient
		fields = '__all__'


class CategoryActive(ListAPIView):
	"""
	Category listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of active Category data.
	"""
	permission_classes = (IsAuthenticated,)
	def get_queryset(self):
		user = self.request.user
		user = user.id
		cid = get_user(user)
		queryset = ProductCategory.objects.filter(active_status=1,Company=cid)\
		.order_by('-created_at')
		return queryset

	def list(self, request):
		queryset = self.get_queryset()
		serializer = CategorylistingSerializer(queryset, many=True)
		response_list = serializer.data 
		return Response({
					"success": True,
					"data" : response_list,
					"message" : "Category listing API worked well!!"})




class FoodTypeActive(ListAPIView):
	"""
	FoodType listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of active FoodType data.
	"""
	permission_classes = (IsAuthenticated,)
	queryset = FoodType.objects.filter(active_status=1).order_by('-created_at')
	serializer_class = FoodTypelistingSerializer



class VariantActive(ListAPIView):
	"""
	Active Variant listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of active Variant data within brand.
	"""
	permission_classes = (IsAuthenticated,)

	def get_queryset(self):
		user = self.request.user
		user = user.id
		cid = get_user(user)
		queryset = Variant.objects.filter(active_status=1).order_by('-created_at')
		return queryset.filter(Company=cid)

	def list(self, request):
		queryset = self.get_queryset()
		serializer = VariantlistingSerializer(queryset, many=True)
		response_list = serializer.data 
		return Response({
					"success": True,
					"data" : response_list,
					"message" : "Variant listing API worked well!!"})

class AddonDetailsActive(ListAPIView):
	"""
	Active AddonDetails listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of Active AddonDetails data within brand.
	"""
	permission_classes = (IsAuthenticated,)
	serializer_class = AddonDetailslistingSerializer

	def get_queryset(self):
		user = self.request.user
		user = user.id
		cid = get_user(user)
		queryset = AddonDetails.objects.filter(active_status=1).order_by('-created_at')
		print("vvvvvvvvvvvvvvvv",queryset)
		return queryset.filter()


class Outletlisting(ListAPIView):
	"""
	Active Outlet listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of Active Outlet data within brand.
	"""
	permission_classes = (IsAuthenticated,)
	serializer_class = OutletlistingSerializer

	def get_queryset(self):
		user = self.request.user.id
		cid = get_user(user)
		queryset = OutletProfile.objects.filter(active_status=1).order_by('-created_at')
		return queryset.filter(Company=cid)


class ActiveProductlisting(APIView):
	"""
	Product listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of active Products.
	"""
	permission_classes = (IsAuthenticated,)
	def get(self, request, format=None):
		try:
			user = request.user.id
			cid = get_user(user)
			record = Product.objects.filter(active_status=1,Company=cid)
			if record.count() == 0:
				return Response(
				{
					"success": False,
 					"message": "Required product data is found!!"
				}
				)
			else:
				final_result = []
				for q in record:
					q_dict = {}
					q_dict["id"] =  q.id
					q_dict["product_with_cat"] = \
					str(q.product_name)+" | "+str(q.product_category.category_name) 
					final_result.append(q_dict)
			return Response({
						"success": True, 
						"message": "Active product data listing api worked well!!",
						"data": final_result,
						})
		except Exception as e:
			print("Active product data listing Api Stucked into exception!!")
			print(e)
			return Response({"success": False, "message": "Error happened!!", "errors": str(e)})


class ActiveIngredient(ListAPIView):

	"""
	Active Ingredient listing GET API

		Authentication Required		: Yes
		Service Usage & Description	: This Api is used for listing of active Ingredient data within brand.
	"""
	permission_classes = (IsAuthenticated,)

	def get_queryset(self):
		user = self.request.user
		user = user.id
		cid = get_user(user)
		queryset = Ingredient.objects.filter(active_status=1).order_by('-created_at')
		return queryset.filter(company=cid)

	def list(self, request):
		queryset = self.get_queryset()
		serializer = IngredientlistingSerializer(queryset, many=True)
		response_list = serializer.data 
		return Response({
					"success": True,
					"data" : response_list,
					"message" : "Ingredient listing API worked well!!"})


