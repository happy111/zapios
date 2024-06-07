from django.urls import path, include
from ZapioApi.Api.BrandApi.listing.listing import Variantlisting, AddonDetailslisting,\
FoodTypelisting, Citylisting,Countrylisting, SubCategorylisting,\
 Companylisting, FeatureListing,Productlistings

from ZapioApi.Api.BrandApi.listing.activelisting import VariantActive, FoodTypeActive,\
CategoryActive,AddonDetailsActive,Outletlisting,ActiveProductlisting,ActiveIngredient





from ZapioApi.Api.BrandApi.productdata.product import ProductListFilter
from ZapioApi.Api.BrandApi.productdata.taglist import ActiveTagList
from ZapioApi.Api.BrandApi.productdata.multiple_category_product import MultipleCategoryFilter


from ZapioApi.Api.BrandApi.profile.profile import ProfileUpdation


from ZapioApi.Api.Authorization.auth import BrandOutletlogin, BrandOutletlogout
from ZapioApi.Api.Authorization.google_auth import BrandOutletGooglelogin,BrandOutletGoogleSignup
from ZapioApi.Api.Authorization.api_generation import APIGenerationView

from ZapioApi.Api.Authorization.change_pwd import ChangePassword
from ZapioApi.Api.Authorization.otp_pwd import EmailOtp,VerifyOtp,ResetPassword



# from ZapioApi.Api.BrandApi.feature_product_create_update import Feature
from ZapioApi.Api.BrandApi.order.listing import Orderlisting
# from ZapioApi.Api.BrandApi.report.addon import AssociateAddon

from ZapioApi.Api.BrandApi.outletmgmt.outletwiselisting.category import OutletCategorylist
from ZapioApi.Api.BrandApi.outletmgmt.outletwiselisting.product import OutletProductlist
from ZapioApi.Api.BrandApi.outletmgmt.listing.outlet import OutletIdNamelisting
from ZapioApi.Api.BrandApi.outletmgmt.availability.category import BrandLevelCategory
from ZapioApi.Api.BrandApi.outletmgmt.availability.product import BrandLevelProductavail
from ZapioApi.Api.BrandApi.outletmgmt.is_open import OutletIsOpen
from ZapioApi.Api.BrandApi.outletmgmt.timing import OutletTiming
from ZapioApi.Api.BrandApi.outletmgmt.retrieve import OutletTimeRetrieval

from ZapioApi.Api.BrandApi.ordermgmt.listing import OrderListingData
from ZapioApi.Api.BrandApi.ordermgmt.retrieve import BrandOrderRetrieval
from ZapioApi.Api.BrandApi.ordermgmt.change_status import ChangeStatusData

from ZapioApi.Api.BrandApi.sound.sound import SoundStatus, ChangeSound

from ZapioApi.push import PushHome



# Notification
from ZapioApi.Api.BrandApi.notification.order_notification import (orderNotificationCount,
																	orderNotificationAll,
																	orderNotificationSeen)





# Delivery Charge Configuration
from ZapioApi.Api.BrandApi.deliverysetting.delivery_config import DeliveryConfig
from ZapioApi.Api.BrandApi.deliverysetting.delivery_edit import DeliveryEdit
from ZapioApi.Api.BrandApi.deliverysetting.delivery_action import DeliveryAction





# Offer setting Configuration
from ZapioApi.Api.BrandApi.offer.offer_create_update import OfferProduct
from ZapioApi.Api.BrandApi.offer.offer_retrieve import OfferRetrieve
from ZapioApi.Api.BrandApi.offer.offer_status import OfferProductaction
from ZapioApi.Api.BrandApi.offer.offer_list import OfferList


# Tag Module
from ZapioApi.Api.BrandApi.tag.tag_create_update import TagCreationUpdation
from ZapioApi.Api.BrandApi.tag.tag_retrieve import TagRetrieve
from ZapioApi.Api.BrandApi.tag.tag_action import TagAction
from ZapioApi.Api.BrandApi.tag.tag_list import TagList

from ZapioApi.Api.BrandApi.Import.customer_excel import CustomerImport
from ZapioApi.Api.BrandApi.Import.category_excel import CategoryImport
from ZapioApi.Api.BrandApi.Import.product_excel import ProductImport


from ZapioApi.Api.BrandApi.is_open import BrandOpen



# Report
from ZapioApi.Api.BrandApi.report.csv_order import Ordercsv
from ZapioApi.Api.BrandApi.report.product_report import ProductReport
from ZapioApi.Api.BrandApi.report.product_csv import ProductReportCsv
from ZapioApi.Api.BrandApi.report.staff_report import StaffCSVReport,AllAttandanceList
from ZapioApi.Api.BrandApi.report.staff_detail import StaffReport
from ZapioApi.Api.BrandApi.report.all_rider import Allrider,RiderCsv,Riderlist
from ZapioApi.Api.BrandApi.report.outlet_performance import OutletPerformance
from ZapioApi.Api.BrandApi.report.addon_report import AddonReport
from ZapioApi.Api.BrandApi.report.addon_csv import AddonReportCsv
from ZapioApi.Api.BrandApi.report.addon_csv1 import Addoncsv
from ZapioApi.Api.BrandApi.report.payment import PaymentReport
from ZapioApi.Api.BrandApi.report.payment_csv import PaymentReportCsv
from ZapioApi.Api.BrandApi.report.alloutlet import AllOutlet
from ZapioApi.Api.BrandApi.report.rating import RatingCSV
from ZapioApi.Api.BrandApi.report.outlet_log import AllLog
from ZapioApi.Api.BrandApi.report.log_csv import AllLogCsv
from ZapioApi.Api.BrandApi.report.ingredient_report import IngredientReport



from ZapioApi.Api.BrandApi.ReceiveConfiguration.receive_list import ReceiveList
from ZapioApi.Api.BrandApi.ordermgmt.edit_order import EditOrder
from ZapioApi.Api.BrandApi.ordermgmt.order_retrieve import OrderRetrieve
from ZapioApi.Api.BrandApi.ordermgmt.allstatus import OrderStatus



urlpatterns = [

	# API Endpoints for brand manager for data listing
	path('listing_data/variant/',Variantlisting.as_view()),
	path('listing_data/AddonDetails/',AddonDetailslisting.as_view()),
	path('listing_data/FoodType/',FoodTypelisting.as_view()),
	path('listing_data/City/',Citylisting.as_view()),
	path('listing_data/Country/',Countrylisting.as_view()),
	path('listing_data/SubCategory/',SubCategorylisting.as_view()),
	# path('listing_data/product/',Productlisting.as_view()),
	path('listing/product/',Productlistings.as_view()),


	path('listing_data/company/',Companylisting.as_view()),
	path('listing_data/feature_product/',FeatureListing.as_view()),


	path('brandprofile/updation/',ProfileUpdation.as_view()),

	# API Endpoints for brand manager for active item listing
	path('Activelisting/variant/',VariantActive.as_view()),
	path('Activelisting/FoodType/',FoodTypeActive.as_view()),
	path('Activelisting/Category/',CategoryActive.as_view()),
	path('Activelisting/AddonDetails/',AddonDetailsActive.as_view()),
	path('Activelisting/Outlet/',Outletlisting.as_view()),
	path('Activelisting/Product/',ActiveProductlisting.as_view()),
	path('Activelisting/Ingredient/',ActiveIngredient.as_view()),

	#API Endpoints for brand manager for product data filter
	path('filterlisting/product/',ProductListFilter.as_view()),
	path('filterlisting/multiplecategory/product/',MultipleCategoryFilter.as_view()),
	path('filterlisting/ActiveTags/',ActiveTagList.as_view()),


	path('order/listing/',Orderlisting.as_view()),

	#API Endpoints for authentication
	path('brand_outlet/login/',BrandOutletlogin.as_view()),
	path('brand_outlet/google/login/',BrandOutletGooglelogin.as_view()),
	path('brand_outlet/google/signup/',BrandOutletGoogleSignup.as_view()),
	path('brand_outlet/api/generation/',APIGenerationView.as_view()),

	path('brand_outlet/logout/',BrandOutletlogout.as_view()),
	path('brand_outlet/ChangePassword/',ChangePassword.as_view()),
	path('brand_outlet/IsOpen/',BrandOpen.as_view()),
	path('brand_outlet/otp/',EmailOtp.as_view()),
	path('brand_outlet/verifyotp/',VerifyOtp.as_view()),
	path('brand_outlet/resetpassword/',ResetPassword.as_view()),

	
	#API Endpoints for outletmgnt
	path('outletmgmt/OutletListing/',OutletIdNamelisting.as_view()),
	path('outletmgmt/Category/',OutletCategorylist.as_view()),
	path('outletmgmt/Product/',OutletProductlist.as_view()),
	path('outletmgmt/Categoryavail/',BrandLevelCategory.as_view()),
	path('outletmgmt/Productavail/',BrandLevelProductavail.as_view()),
	path('outletmgmt/IsOpen/',OutletIsOpen.as_view()),
	path('outletmgmt/Timing/',OutletTiming.as_view()),
	path('outletmgmt/TimeRetrieval/',OutletTimeRetrieval.as_view()),

	#API Endpoints for ordermgnt
	path('ordermgnt/Order/',OrderListingData.as_view()),
	path('ordermgnt/Retrieval/',BrandOrderRetrieval.as_view()),
	path('ordermgnt/ChangeStatus/',ChangeStatusData.as_view()),
	path('ordermgnt/ratingcsv/',RatingCSV.as_view()),

	#API Endpoints for Sound Effect on order recieving
	path('sound/status/',SoundStatus.as_view()),
	path('sound/ChangeStatus/',ChangeSound.as_view()),
	path('pushnotify/', PushHome.as_view()),


	# Notification All Api
	path('notification/ordercount/',orderNotificationCount.as_view()),
	path('notification/seen/',orderNotificationSeen.as_view()),
	path('notification/all/',orderNotificationAll.as_view()),



	# Theme Setting
	path('deliverycharge/setting/',DeliveryConfig.as_view()),
	path('deliverycharge/edit/',DeliveryEdit.as_view()),
	path('deliverycharge/action/',DeliveryAction.as_view()),


	# Offer setting
	path('offer/product/save/',OfferProduct.as_view()),
	path('offer/product/action/',OfferProductaction.as_view()),
	path('offer/product/retrieve/',OfferRetrieve.as_view()),
	path('offer/product/list/',OfferList.as_view()),


	# Tag Module
	path('tag/createupdate_data/',TagCreationUpdation.as_view()),
	path('tag/action/',TagAction.as_view()),
	path('tag/list/',TagList.as_view()),
	path('tag/retrieve/',TagRetrieve.as_view()),


	path('customer/import/',CustomerImport.as_view()),
	path('category/import/',CategoryImport.as_view()),
	path('product/import/',ProductImport.as_view()),


	# Report Session
	path('product/report/',ProductReport.as_view()),
	path('product/report/csv/',ProductReportCsv.as_view()),
	path('addon/report/',AddonReport.as_view()),
	path('addon/report/csv/',AddonReportCsv.as_view()),
	path('ordermgnt/Order/csv/',Ordercsv.as_view()),
	path('ordermgnt/addon/csv1/',Addoncsv.as_view()),
	path('ordermgnt/payment/report/',PaymentReport.as_view()),
	path('ordermgnt/payment/report/csv/',PaymentReportCsv.as_view()),
	path('ordermgnt/outlet/',AllOutlet.as_view()),
	path('ordermgnt/log/',AllLog.as_view()),
	path('ordermgnt/log/csv/',AllLogCsv.as_view()),
	path('staff/csv/',StaffCSVReport.as_view()),
	path('staff/list/',AllAttandanceList.as_view()),
	path('staff/report/',StaffReport.as_view()),
	path('rider/all/',Allrider.as_view()),
	path('rider/csv/',RiderCsv.as_view()),
	path('rider/list/',Riderlist.as_view()),
	path('outlet/performance/',OutletPerformance.as_view()),
	path('receive/list/',ReceiveList.as_view()),
	path('ingredient/consumption_report/csv/',IngredientReport.as_view()),




	# Order Moduel
	path('order/edit/',EditOrder.as_view()),
	path('order/retrieve/',OrderRetrieve.as_view()),
	path('order/allstatus/',OrderStatus.as_view()),

]
