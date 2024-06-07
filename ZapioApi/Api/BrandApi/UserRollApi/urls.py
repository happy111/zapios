from django.urls import path
from ZapioApi.Api.BrandApi.UserRollApi.all_menu import AllMenu
from ZapioApi.Api.BrandApi.UserRollApi.savepermission import SavePermission
from ZapioApi.Api.BrandApi.UserRollApi.save_roll import SaveRoll

from ZapioApi.Api.BrandApi.UserRollApi.all_billmenu import BillAllMenu
from ZapioApi.Api.BrandApi.UserRollApi.savebillpermission import BillSavePermission


urlpatterns = [
	path('allmenu/',AllMenu.as_view()),
	path('savepermission/',SavePermission.as_view()),
	path('save/roll/',SaveRoll.as_view()),


	# Bill menu
	path('bill/allmenu/',BillAllMenu.as_view()),
	path('bill/savepermission/',BillSavePermission.as_view()),


]