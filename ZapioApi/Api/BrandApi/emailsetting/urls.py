from django.urls import path, include

from ZapioApi.Api.BrandApi.emailsetting.email_config import EmailConfig
from ZapioApi.Api.BrandApi.emailsetting.email_edit import EmailEdit
from ZapioApi.Api.BrandApi.emailsetting.email_action import EmailAction
from ZapioApi.Api.BrandApi.emailsetting.coupon import CouponData


urlpatterns = [
	#Email Setting
	path('setting/',EmailConfig.as_view()),
	path('edit/',EmailEdit.as_view()),
	path('action/',EmailAction.as_view()),
	path('coupon/',CouponData.as_view()),


]


