from django.urls import path
from .views import *


urlpatterns = [

   	path("country/list/",CountryList.as_view()),
 

   	]

