from django.urls import path
from .views import *


urlpatterns = [
	path('payment/setting/',PaymentConfig.as_view()),
	path('payment/edit/',PaymentEdit.as_view()),
	path('payment/retrieve/',PaymentRetrieve.as_view()),
	path('payment/action/',PaymentAction.as_view()),
	path('activetax/listing/',ActiveTaxlisting.as_view()),
	path('deliverycharge/setting/',DeliveryConfig.as_view()),
	path('deliverycharge/edit/',DeliveryEdit.as_view()),
	path('deliverycharge/action/',DeliveryAction.as_view()),
	path('onlinepayment/list/',PaymentList.as_view()),
	path('onlinepayment/action/',PaymentAction.as_view()),
	path('autofetch/address/',AutoFetch.as_view()),
	path('autofetch/pincode/address/',AutoFetchAddress.as_view()),


]