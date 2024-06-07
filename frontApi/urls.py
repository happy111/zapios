from django.urls import path
from frontApi.views import FeatureListing,LogoBanner,FrontLogin
from frontApi.track_order import TrackOrder
from frontApi.order.order import OrderData

from frontApi.nearestOutlet.outlet import RestaurantMapView
from frontApi.nearestOutlet.nearest_outlet import NearestMapView

from frontApi.nearestOutlet.order_otp import OrderOtp,VerifyOtp,MphinOtp,VerifyMpin
from frontApi.nearestOutlet.customer_profile import CustomeProfile
from frontApi.nearestOutlet.customer_rating import CustomeRating

from frontApi.configuration.config import ConfigView
from frontApi.configuration.feature import FeatureProductList
from frontApi.configuration.all_config import ConfigDataView
from frontApi.configuration.google_analytics import GoogleAnalytics
from frontApi.menu.category import CatListing
from frontApi.menu.product import FullProductList, ProductDetails
from frontApi.menu.recommend import ProductRecommend
from frontApi.menu.customization import CustomeMgmt
from frontApi.coupon.discounts import CouponcodeView
from frontApi.paymentsetting.payment_config import PaymentConfig
from frontApi.order.distance_check import DistanceCheck
from frontApi.LiveFeed.stream import OutletCam
from frontApi.LiveFeed.allOutlets import ALLOutlets
from frontApi.nearestOutlet.order_now import DeliveryView
from frontApi.nearestOutlet.order_latter import OrderLatter
from frontApi.coupon.coupon_list import Couponlisting
from . views import *



urlpatterns = [
	path('logobanner/',LogoBanner.as_view()),
	path('trackorder/',TrackOrder.as_view()),
	path('order/place/',OrderData.as_view()),
	path('order/otp/',OrderOtp.as_view()),
	path('order/mpin/',MphinOtp.as_view()),

	path('otp/verify/',VerifyOtp.as_view()),
	path('mpin/verify/',VerifyMpin.as_view()),
	path('login/',FrontLogin.as_view()),
	path('distance/check/',DistanceCheck.as_view()),
	path('outlet/OutletDetail/',RestaurantMapView.as_view()),
	path('outlet/nearestOutlet/',NearestMapView.as_view()),
	path('outlet/alloutlets/',AllOutletsView.as_view()),


	path('outlet/delivery/',DeliveryView.as_view()),
	path('configuration/',ConfigView.as_view()),
	path('featureproduct/',FeatureProductList.as_view()),
	path('customer/cat_list/',CatListing.as_view()),
	path('customer/menu_list_filter/',FullProductList.as_view()),
	path('customer/customize_data/',CustomeMgmt.as_view()),
	path('customer/profile/',CustomeProfile.as_view()),
	path('customer/rating/',CustomeRating.as_view()),
	path('Couponcode/',CouponcodeView.as_view()),
	path('payment/setting/',PaymentConfig.as_view()),
	
	
	# config data company wise
	path('configuration/all/',ConfigDataView.as_view()),
	path('configuration/google/analytics/',GoogleAnalytics.as_view()),
	path('outlet/stream/', OutletCam.as_view()),
	path('all/stream/listing/', ALLOutlets.as_view()),
	path('product/recommend/', ProductRecommend.as_view()),
	path('product/<int:pk>/', ProductDetails.as_view()),
	path('order/latter/',OrderLatter.as_view()),
	path('coupon/list/',Couponlisting.as_view()),
	path('listing/menu/',listMenu.as_view()),

]

