from django.urls import path
from ZapioApiV2.Brand.brand_create_update import (
												BrandCreation,
												BusinessType,
												CountryList,
												StateList,
												BrandActive,
												CityList)
from ZapioApiV2.Brand.all_tag import AllTag
from ZapioApiV2.Brand.all_subcategory import GetSubcategory
from ZapioApiV2.Brand.config import BrandConfig
from ZapioApiV2.Brand.log import BrandLog
from ZapioApiV2.Brand.putday import Putday
from ZapioApiV2.Brand.brand import dashboard
from ZapioApiV2.Brand.outlet import dashboardOutlet
from ZapioApiV2.Brand.brand_event import dashboardEvent


# Payment Module
from ZapioApiV2.PaymentMethod.currency import GetCurrency
from ZapioApiV2.PaymentMethod.payment_create_update import PaymentCreate
from ZapioApiV2.PaymentMethod.payment_list import PaymentList
from ZapioApiV2.PaymentMethod.payment_retrieve import PaymentRetrieve
from ZapioApiV2.PaymentMethod.payment_action import ActionPayment
from ZapioApiV2.PaymentMethod.payment_alllist import PaymentAllList
from ZapioApiV2.PaymentMethod.payment_status import PaymentStatus
from ZapioApiV2.PaymentMethod.subscriptionPayment import SubscriptionPayment

# Measurement Module
from ZapioApiV2.Measurement.unit_create_update import UnitCreationUpdation
from ZapioApiV2.Measurement.unit_retrieve import RetrieveUnit
from ZapioApiV2.Measurement.unit_action import ActionUnit
from ZapioApiV2.Measurement.unit_status import StatusUnit



# Primary Ingredient Module
from ZapioApiV2.PrimaryIngredient.primary_create_update import PrimaryIngredientCreationUpdation
from ZapioApiV2.PrimaryIngredient.primary_retrieve import RetrievePrimaryIngredient
from ZapioApiV2.PrimaryIngredient.primary_listing import listPrimaryIngredient
from ZapioApiV2.PrimaryIngredient.primary_action import ActionPrimaryIngredient
from ZapioApiV2.PrimaryIngredient.secondary_listing import listSecondaryIngredients


# Tax Module
from ZapioApiV2.Tax.tax_create_update import TaxCreationUpdation
from ZapioApiV2.Tax.tax_retrieve import RetrieveTax
from ZapioApiV2.Tax.tax_listing import listTax
from ZapioApiV2.Tax.tax_action import ActionTax



# Source Module
from ZapioApiV2.Ordersource.source_create_update import SourceCreationUpdation
from ZapioApiV2.Ordersource.source_retrieve import RetrieveSource
from ZapioApiV2.Ordersource.source_listing import listSource
from ZapioApiV2.Ordersource.source_action import ActionSource


# Primary Event Module
from ZapioApiV2.Event.event_create_update import EventCreationUpdation
from ZapioApiV2.Event.event_retrieve import RetrieveEvent
from ZapioApiV2.Event.event_listing import listEvent
from ZapioApiV2.Event.event_action import ActionEvent
from ZapioApiV2.Event.event_delete import DeleteEvent

# Event Tag Module
from ZapioApiV2.Event.Tag.tag_create_update import EventTagCreationUpdation
from ZapioApiV2.Event.Tag.tag_retrieve import RetrieveEventTag
from ZapioApiV2.Event.Tag.tag_listing import listEventTag
from ZapioApiV2.Event.Tag.tag_action import ActionEventTag
from ZapioApiV2.Event.Tag.tag_delete import DeleteEventTag
# from ZapioApiV2.Event.trigger import TriggerCreate



from ZapioApiV2.City.city_listing import listCity
from ZapioApiV2.City.city_locality import CityLocality
from ZapioApiV2.City.city_save import CitySave
from ZapioApiV2.City.state_listing import listState
from ZapioApiV2.City.business_listing import listBusiness
from ZapioApiV2.City.order_listing import listOrder


# Locality Module
from ZapioApiV2.Area.area_create_update import LocalityCreationUpdation
from ZapioApiV2.Area.area_retrieve import RetrieveLocality
from ZapioApiV2.Area.area_listing import listLocality
from ZapioApiV2.Area.area_action import ActionLocality



# Menu Module
from ZapioApiV2.Menu.menu_create_update import MenuCreationUpdation
from ZapioApiV2.Menu.menu_retrieve import RetrieveMenu
from ZapioApiV2.Menu.menu_listing import listMenu
from ZapioApiV2.Menu.menu_action import ActionMenu




urlpatterns = [

	path('brand/create/',BrandCreation.as_view()),
	path('brand/config/',BrandConfig.as_view()),
	path('customer/tag/',AllTag.as_view()),
	path('brand/log/',BrandLog.as_view()),
    path('brand/businesstype/',BusinessType.as_view()),
    path('brand/country/',CountryList.as_view()),
    path('brand/state/',StateList.as_view()),
    path('brand/city/',CityList.as_view()),
    path('brand/active/',BrandActive.as_view()),



   # Payment Method
	path('get/currency/',GetCurrency.as_view()),
	path('payment/create_update/',PaymentCreate.as_view()),
	path('payment/list/',PaymentList.as_view()),
	path('payment/retrieve/',PaymentRetrieve.as_view()),
	path('payment/action/',ActionPayment.as_view()),
	path('payment/alllist/',PaymentAllList.as_view()),
	path('payment/status/', PaymentStatus.as_view()),
	path('payment/subscription/',SubscriptionPayment.as_view()),
	# Measurement Module
	
	path('create_update/unit/',UnitCreationUpdation.as_view()),
	path('retrieve/unit/',RetrieveUnit.as_view()),
	path('action/unit/',ActionUnit.as_view()),
	path('listing/status/unit/',StatusUnit.as_view()),

	# Primary Ingredient Module
	path('create_update/primary/',PrimaryIngredientCreationUpdation.as_view()),
	path('retrieve/primary/',RetrievePrimaryIngredient.as_view()),
	path('listing/primary/',listPrimaryIngredient.as_view()),
	path('action/primary/',ActionPrimaryIngredient.as_view()),


	# path('listing/secondary/',listSecondaryIngredient.as_view()),
	path('listing/secondarys/',listSecondaryIngredients.as_view()),
	path('getsubcategory/',GetSubcategory.as_view()),


	# Tax Module
	path('create_update/tax/',TaxCreationUpdation.as_view()),
	path('retrieve/tax/',RetrieveTax.as_view()),
	path('listing/tax/',listTax.as_view()),
	path('action/tax/',ActionTax.as_view()),


	# Order Source Module
	path('create_update/source/',SourceCreationUpdation.as_view()),
	path('retrieve/source/',RetrieveSource.as_view()),
	path('listing/source/',listSource.as_view()),
	path('action/source/',ActionSource.as_view()),


	# Event Module
	path('create_update/event_type/',EventCreationUpdation.as_view()),
	path('retrieve/event_type/',RetrieveEvent.as_view()),
	path('listing/event_type/',listEvent.as_view()),
	path('action/event_type/',ActionEvent.as_view()),
	path('delete/event_type/',DeleteEvent.as_view()),


	# Event Tag Module
	path('create_update/event_tag/',EventTagCreationUpdation.as_view()),
	path('retrieve/event_tag/',RetrieveEventTag.as_view()),
	path('listing/event_tag/',listEventTag.as_view()),
	path('action/event_tag/',ActionEventTag.as_view()),
	path('delete/event_tag/',DeleteEventTag.as_view()),
	# path('trigger/',TriggerCreate.as_view()),



	path('listing/city/',listCity.as_view()),
	path('city/locality/',CityLocality.as_view()),
	path('listing/state/',listState.as_view()),



	# Menu Module
	path('create_update/menu/',MenuCreationUpdation.as_view()),
	path('retrieve/menu/',RetrieveMenu.as_view()),
	path('listing/menu/',listMenu.as_view()),
	path('action/menu/',ActionMenu.as_view()),

	# Locality Module
	path('create_update/locality/',LocalityCreationUpdation.as_view()),
	path('retrieve/locality/',RetrieveLocality.as_view()),
	path('listing/locality/',listLocality.as_view()),
	path('action/locality/',ActionLocality.as_view()),
	path('city/save/',CitySave.as_view()),
	path('businesstype/list/',listBusiness.as_view()),
	path('order/list/',listOrder.as_view()),
	path('day/',Putday.as_view()),

	
	path('brand/home/',dashboard.as_view()),
	path('outlet/home/',dashboardOutlet.as_view()),
	path('brand/event/',dashboardEvent.as_view()),
	# path('brand/dashboard/',DashboardData.as_view()),

]
