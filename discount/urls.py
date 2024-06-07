from django.urls import path
from .views import *


urlpatterns = [

	path('coupon/create_update/',CouponCreationUpdation1.as_view()),
	path('quantitycombo/create_update/',QuantityComboCreationUpdation.as_view()),
	path('percentcombo/create_update/',PercentComboCreationUpdation.as_view()),
	path('coupon/listing/',Couponlisting1.as_view()),
	path('QuantityCombo/listing/',QuantityCombolisting.as_view()),
	path('PercentCombo/listing/',PercentCombolisting.as_view()),
	path('coupon/retrieve/',CouponRetrieval1.as_view()),
	path('QuantityCombo/retrieve/',QuantityComboRetrieval.as_view()),
	path('PercentCombo/retrieve/',PercentComboRetrieval.as_view()),
	path('coupon/action/',CouponAction.as_view()),
	path('QuantityCombo/action/',QuantityComboAction.as_view()),
	path('PercentCombo/action/',PercentComboAction.as_view()),


	path('create_update/',CouponCreationUpdation.as_view()),
	path('retrieve/',CouponRetrieval.as_view()),
	path('list/',Couponlisting.as_view()),
	path('action/',CouponActions.as_view()),

	path('reason/createupdate_data/',ReasonCreationUpdation.as_view()),
	path('reason/action/',ReasonAction.as_view()),
	path('reason/list/',ReasonList.as_view()),
	path('reason/retrieve/',ReasonRetrieve.as_view()),


]


