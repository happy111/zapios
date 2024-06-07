from django.urls import path, include
from .views import *

urlpatterns = [
    path("list/", SubscriptionListingAPI.as_view()),
 	path("payment/config/", PaymentConfig.as_view()),
 	path("payment/create/", PaymentCreateAPI.as_view()),
 	path("payment/process/", PaymentProcess.as_view()),

]
