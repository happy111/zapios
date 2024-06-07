# from django.urls import path
# from ZapioApi.Api.urbanpiper.listing.outlet import UrbanOutletListing, UnInitiatedOutletListing
# from ZapioApi.Api.urbanpiper.listing.synced_outlet import SyncedOutletListing
# from ZapioApi.Api.urbanpiper.attach import UrbanOutletAttach
# from ZapioApi.Api.urbanpiper.sync.outlet import OutletToSync
# from ZapioApi.Api.urbanpiper.action.action import OutletAction
# from ZapioApi.Api.urbanpiper.menu.cat_attach import CatAttach
# from ZapioApi.Api.urbanpiper.menu.product_attach import ProductAttach
# from ZapioApi.Api.urbanpiper.listing.synced_menu import SyncedProduct, SyncedCat

# from ZapioApi.Api.urbanpiper.sync.menu import MenuSync


# urlpatterns = [

# 	path('listing/outlet/',UrbanOutletListing.as_view()),
# 	path('listing/not_initiated_outlet/',UnInitiatedOutletListing.as_view()),
# 	path('listing/synced_outlet/',SyncedOutletListing.as_view()),
# 	path('listing/category/',SyncedCat.as_view()),
# 	path('listing/product/',SyncedProduct.as_view()),

# 	path('attach/outlet/',UrbanOutletAttach.as_view()),
# 	path('attach/category/',CatAttach.as_view()),
# 	path('attach/products/',ProductAttach.as_view()),

# 	path('sync/outlet/',OutletToSync.as_view()),
# 	path('action/outlet/',OutletAction.as_view()),

# 	path('sync/menu/',MenuSync.as_view()),


# 	# path('activelisting/usertype/',UserTypeActiveListing.as_view()),
# 	# path('retrieval/usertype/',UserTypeRetrieval.as_view()),
# 	# path('createupdate/usertype/',UserTypeCreationUpdation.as_view()),
# 	# path('action/usertype/',UserTypeAction.as_view()),

# 	# path('listing/profile/',ManagersListing.as_view()),
# 	# path('retrieval/profile/',ManagerRetrieval.as_view()),
# 	# path('createupdate/profile/',ManagerCreationUpdation.as_view()),
# 	# path('action/profile/',ManagerAction.as_view()),

# 	# path('listing/Module/',ModuleListing.as_view()),
# 	# path('listing/MainRoute/',MainRouteListing.as_view()),
# 	# path('listing/Route/',RouteListing.as_view()),
# 	# path('listing/SubRoute/',SubRouteListing.as_view()),
# ]