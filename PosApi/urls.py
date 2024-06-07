from django.urls import path, include
from PosApi.Api.Authorization.pos_login import Poslogin, Poslogout
from PosApi.Api.Authorization.pos_userdetail import PosUserDetail
from PosApi.Api.Authorization.pos_changepassword import Changepassword
from PosApi.Api.Authorization.profile_update import ProfileUpdate
from PosApi.Api.order.order_detail import OrderDetail
from PosApi.Api.outletmgmt.listing.outlet_list import AllOutlet
from PosApi.Api.outletmgmt.nearest_outlet import RestaurantMapView


from PosApi.Api.outletmgmt.availability.product import PosLevelProductavail
from PosApi.Api.outletmgmt.availability.category import PosLevelCategory

from PosApi.Api.outletmgmt.outletwiselisting.product import OutletProductlist
from PosApi.Api.outletmgmt.outletwiselisting.category import OutletCategorylist
from PosApi.Api.outletmgmt.is_open import OutletIsOpen
from PosApi.Api.order.order_process import ProcessList
from PosApi.Api.order.order import OrderProcess
from PosApi.Api.order.order_edit import EditOrderProcess
from PosApi.Api.order.csv_order import Ordercsv

from PosApi.Api.outletmgmt.receive_retrieve import ReceiveRetrieve


from PosApi.Api.ordermgmt.listing import OrderListingData
from PosApi.Api.ordermgmt.order_log import OrderLogData
from PosApi.Api.ordermgmt.change_status import ChangeStatusData
from PosApi.Api.ordermgmt.retrieve import BrandOrderRetrieval
from PosApi.Api.Customer.customer_search import CustomerList
from PosApi.Api.Customer.customer_registration import CustomerRegister
from PosApi.Api.Customer.customer_order import CustomerWiseOrder

from PosApi.Api.menu.customization import CustomeMgmt
from PosApi.Api.notification.notification import (
    orderNotificationCount,
    orderAccepted,
    orderNotificationSeen,
)
from PosApi.Api.coupon.discounts import CouponcodeView
from PosApi.Api.coupon.all_discount import AllDiscount
from PosApi.Api.order.order_settle import OrderSettle
from PosApi.Api.order.order_orderid_update import OrderIDUpdate
from PosApi.Api.order.settlebill import OrderBillSettle

from PosApi.Api.order.detail import UserDetail

#  Rider Api

from PosApi.Api.Rider.allrider import RiderList
from PosApi.Api.Rider.assign_rider import AsignRider
from PosApi.Api.Rider.rider_detail import RiderDetail

# Temperature tracking
from PosApi.Api.tempTracker.latest_temp import TempRetrieve
from PosApi.Api.tempTracker.add_temp import TempAdd
from PosApi.Api.tempTracker.invoice_data import InovoiceData
from PosApi.Api.tempTracker.allergen_data import AllergenInformation
from PosApi.Api.tempTracker.package_data import PackageCharge
from PosApi.Api.tempTracker.all_city import AllCity


from attendance import views
from . views import *


urlpatterns = [
    path("user/login/", Poslogin.as_view()),
    path("user/logout/", Poslogout.as_view()),
    # path("user/logged/", loggedUser.as_view()),


    path("user/posuser/list/", PosUserDetail.as_view()),
    path("user/posuser/cpass/", Changepassword.as_view()),
    path("user/profile/update/", ProfileUpdate.as_view()),
    path("user/orderdetail/", OrderDetail.as_view()),
    # Outlet List
    path("outletmgmt/list/", AllOutlet.as_view()),
    path("outletmgmt/Categoryavail/", PosLevelCategory.as_view()),
    path("outletmgmt/Productavail/", PosLevelProductavail.as_view()),
    path("outletmgmt/Categorylist/", OutletCategorylist.as_view()),
    path("outletmgmt/Productlist/", OutletProductlist.as_view()),
    path("outletmgmt/IsOpen/", OutletIsOpen.as_view()),
    path("outletmgmt/receipt/", ReceiveRetrieve.as_view()),
    path('outletmgmt/nearestOutlet/',RestaurantMapView.as_view()),

    # Order Management
    path("order/processlist/", ProcessList.as_view()),
    path("ordermgnt/Order/", OrderListingData.as_view()),
    path("ordermgnt/Order/log/", OrderLogData.as_view()),
    path("ordermgnt/Retrieval/", BrandOrderRetrieval.as_view()),
    path("ordermgnt/ChangeStatus/", ChangeStatusData.as_view()),
    path("ordermgnt/Orderprocess/", OrderProcess.as_view()),
    path("ordermgnt/editorder/", EditOrderProcess.as_view()),

   

    path("order/settle/", OrderSettle.as_view()),
    path("order/billsettle/", OrderBillSettle.as_view()),
    # Product Customize
    path("product/customize_data/", CustomeMgmt.as_view()),
    # New Order Notification
    path("ordernotification/list/", orderNotificationCount.as_view()),
    path("ordernotification/accepted/", orderAccepted.as_view()),
    path("ordernotification/seen/", orderNotificationSeen.as_view()),
    # New Order Notification
    path("customer/list/", CustomerList.as_view()),
    path("customer/registration/", CustomerRegister.as_view()),
    path("customer/order/", CustomerWiseOrder.as_view()),
    path("couponcode/", CouponcodeView.as_view()),
    path("alldiscount/", AllDiscount.as_view()),
    path("outletid/update/", OrderIDUpdate.as_view()),
    # Rider API
    path("rider/outletwiserider/", RiderList.as_view()),
    path("rider/outletwiserider/assign/", AsignRider.as_view()),
    path("detail/", UserDetail.as_view()),
    path("rider/orderdetail/", RiderDetail.as_view()),

    # Temperature API
    path("temp/inovoicedata/", InovoiceData.as_view()),
    path("temp/retrieve/", TempRetrieve.as_view()),
    path("temp/add/", TempAdd.as_view()),
    path("allergen/", AllergenInformation.as_view()),
    path("package/charge/", PackageCharge.as_view()),
    path("city/", AllCity.as_view()),


    path("attendance/logout/", views.AttendanceLogout.as_view()),
    path("attendance/create/", views.AttendanceCreate.as_view()),
    path("attendance/list/", views.AttendanceList.as_view()),
    path("attendance/update/", views.AttendanceUpdate.as_view()),


    # Report
    path("order/csv/", Ordercsv.as_view()),
    path('payment/list/',PaymentList.as_view()),
    path('listing/source/',listSource.as_view()),

    #Eion Integration
    path("eion/order/list/", EionOrderListingData.as_view()),
    path("eion/order/reports/", EionOrderListingDataReports.as_view()),
    path("eion/aizo/link/", AizotecEionUnlinkAPI.as_view()),
    path("eion/aizo/productlist/", FullProductListEion.as_view()),
    path("eion/aizo/outletlist/", RestaurantMapViewEion.as_view()),
]


