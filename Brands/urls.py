from django.urls import path, include
from .views import *

urlpatterns = [
    path("page/create/", PageCreate.as_view()),
    path("page/retrieve/<int:pk>/", PageRetrieveAPI.as_view()),
    path("page/list/", PageListingAPI.as_view()),
  	path("page/action/", PageActionAPI.as_view()),

  	# Home Page
  	path("home/create/", HomeCreate.as_view()),
    path("home/retrieve/", HomeRetrieveAPI.as_view()),
    path("menu/view/", MenuView.as_view()),
    path("menu/count/", MenuCount.as_view()),
    path("menu/checkout/", CountCheckout.as_view()),
    path('brand/dashboard/',DashboardData.as_view()),
    path('brand/outofrange/',OutOfRangeData.as_view()),
    path('brand/ordersource/report/',SourceReportData.as_view()),
    path('brand/paymentmethod/report/',PaymentReportData.as_view()),
    path('brand/allevent/',EventData.as_view()),
    path('brand/review/',ReviewData.as_view()),
    path('brand/datewise_report/',DateWiseReport.as_view()),




]

