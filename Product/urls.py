from django.urls import path
from .views import *
from .action_view import *
from .list_view import *

urlpatterns = [

   	path("category/create/",CategoryCreationUpdation.as_view()),
   	path("category/delete/",CategoryDelete.as_view()),
   	path("view_data/category/",CategoryView.as_view()),

	path('create_data/subcatagory/',SubCategoryCreation.as_view()),
	path('update_data/subcatagory/',SubCategoryUpdation.as_view()),
	path('createupdate_data/foodtype/',FoodTypeCreationUpdation.as_view()),
	path('createupdate_data/variant/',VariantCreationUpdation.as_view()),
	path('createupdate_data/addonassociation/',AddonAssociateCreationUpdation.as_view()),
	path('createupdate_data/product/',ProductCreationUpdation.as_view()),

   # Delete API
	path('delete/category_image/',CategoryDeleteImage.as_view()),
   	path('delete/subcategory/',SubcategoryDelete.as_view()),
	path('delete/product/',ProductDelete.as_view()),
	path('delete/addon/',AddonDelete.as_view()),


	path('retrieval_data/category/',CategoryRetrieval.as_view()),
	path('retrieval_data/subcategory/',SubCategoryRetrieval.as_view()),
	path('retrieval_data/foodtype/',FoodTypeRetrieval.as_view()),
	path('retrieval_data/variant/',VariantRetrieval.as_view()),
	path('retrieval_data/AddonDetails/',AddonDetailsRetrieval.as_view()),
	path('retrieval_data/product/',ProductRetrieval.as_view()),
	path('retrieval_data/featureProduct/',FeatureRetrieval.as_view()),
	path('retrieval_data/addon/',AddonRetrieval.as_view()),
   

	path('action/product/',ProductAction.as_view()),
	path('action/Category/',CategoryAction.as_view()),
	path('action/subcategory/',SubCategoryAction.as_view()),
	path('action/variant/',VariantAction.as_view()),
	path('action/AddonDetails/',AddonDetailsAction.as_view()),
	path('action/foodtype/',FoodTypeAction.as_view()),
	path('action/FeaturedProduct/',FeatureAction.as_view()),


	path('listing_data/product/',Productlisting.as_view()),
	path('configuration_data/catagory_data/',CatagoryListing.as_view()),
	path('configuration_data/subcatagory_data/',SubCatagoryListing.as_view()),
	path('configuration_data/catwise_outlet_data/',CatagoryWiseOutletListing.as_view()),
	path('configuration_data/catwise_subcat_data/',CatagoryWiseSubCategoryListing.as_view()),
	path('configuration_data/citywise_area_data/',CityWiseAreaListing.as_view()),
	path('addons/associate/',AssociateAddon.as_view()),
	path('rating/update/',RatingUpdate.as_view()),

	### Addon Api
	path('create/addons/',AddonCreation.as_view()),
	path('list/addons/',AddonListApi.as_view()),
	path('update/addons/',AddonUpdation.as_view()),
	path('retrieve/addons/<int:pk>',AddonRetrieve.as_view()),
	path('action/addons/',AddonAction.as_view()),

	path('create/addon_group/',AddongroupCreation.as_view()),
	path('update/addon_group/',AddongroupUpdation.as_view()),
	path('list/addon_group/',AddongroupListApi.as_view()),

   	]

