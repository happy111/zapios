from django.urls import path
from Customers.Api.Authorization.registration import CustomerRegistration, OtpVerificationemail
from Customers.Api.Authorization.signin import CustomerSignin, CustomerSignout
from . views import *


urlpatterns = [
	#API Endpoints for authentication
	path('registration/',CustomerRegistration.as_view()),
	path('OtpVerificationemail/apiview/', OtpVerificationemail.as_view()),
	path('signin/apiview/', CustomerSignin.as_view()),
	path('signout/apiview/', CustomerSignout.as_view()),


	path('Active/listing/', ActiveCustomer.as_view()),
	path('All/listing/', Userlisting.as_view()),
	path('Action/', CustomerAction.as_view()),
	path('OrderAnalysis/retrieve/', OrderAnalysis.as_view()),
	path('OrderHistory/listing/', CustomerOrders.as_view()),

]