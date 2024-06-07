from django.urls import path
from .views import *


urlpatterns = [
	path('listing/usertype/',UserTypeListing.as_view()),
	path('activelisting/usertype/',UserTypeActiveListing.as_view()),
	path('retrieval/usertype/',UserTypeRetrieval.as_view()),
	path('createupdate/usertype/',UserTypeCreationUpdation.as_view()),
	path('action/usertype/',UserTypeAction.as_view()),

	path('listing/profile/',ManagersListing.as_view()),
	path('retrieval/profile/',ManagerRetrieval.as_view()),
	path('createupdate/profile/',ManagerCreationUpdation.as_view()),
	path('action/profile/',ManagerAction.as_view()),

	path('listing/Module/',ModuleListing.as_view()),
	path('listing/MainRoute/',MainRouteListing.as_view()),
	path('listing/Route/',RouteListing.as_view()),
	path('listing/SubRoute/',SubRouteListing.as_view()),
	path('hide/profile/',ManagerHide.as_view()),

]