from django.urls import path
from History.Api.coupon_history import  historyCoupon,brandhistoryCoupon
from History.Api.customer_history import historyCustomer


urlpatterns = [
	path('outlet/couponHistory/',historyCoupon.as_view()),
	path('brand/couponHistory/',brandhistoryCoupon.as_view()),
	path('outlet/customerHistory/',historyCustomer.as_view()),
]