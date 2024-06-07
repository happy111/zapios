from django.urls import path

from .views import *
from Outlet.Api.Authorization.create_update_delivery import (DeliveryAction,
																DeliveryBoyRegistration,
																DeliveryBoyListing,
																DeliveryBoyRetrieval,
																DeliveryActiveListing)

from Outlet.Api.order.listing import  OrderListingData
from Outlet.Api.order.change_order_status import  ChangeStatusData
from Outlet.Api.order.retrieve_order import  OrderRetrieval
from Outlet.Api.Authorization.profile import  OutletRetrieve

from Outlet.Api.Authorization.onoff import  outletOnOff, Outlet_Is_open

from Outlet.Api.listing.product import Productlist
from Outlet.Api.listing.category import Categorylist
from Outlet.Api.availability.product import Productavail
from Outlet.Api.availability.category import Category


urlpatterns = [
	path('deliveryboy/registration/',DeliveryBoyRegistration.as_view()),
	path('deliveryboy/listdata/',DeliveryBoyListing.as_view()),
	path('action/DeliveryBoy/',DeliveryAction.as_view()),
	path('activeListing/DeliveryBoy/',DeliveryActiveListing.as_view()),
	path('retrieval_data/delivery_boy/',DeliveryBoyRetrieval.as_view()),
	path('orderlisting/',OrderListingData.as_view()),
	path('orderStatuschange/',ChangeStatusData.as_view()),
	path('retrievalOrder/',OrderRetrieval.as_view()),
	path('retrieve/outlet/', OutletRetrieve.as_view()),
	path('onoff/',outletOnOff.as_view()),
	path('listing/product/',Productlist.as_view()),
	path('listing/category/',Categorylist.as_view()),
	path('availability/product/',Productavail.as_view()),
	path('availability/Category/',Category.as_view()),
	path('is_open/',Outlet_Is_open.as_view()),
	path('retrieval_data/outlet/',OutletRetrieval.as_view()),
	path('brand_outlet/outlet_creation/',OutletCreation.as_view()),
	path('brand_outlet/outlet_updation/',OutletUpdation.as_view()),
	path('action/Outlet/',OutletAction.as_view()),
	path('configuration_data/outlet_data/',OutletListing.as_view()),
	path('hide/outlet/',OutletHide.as_view()),
	path('urbanpiper/profile/',UrbanPiperOutletDetails.as_view())
]

