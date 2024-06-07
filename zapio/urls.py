"""zapio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
	1. Import the include() function: from django.urls import include, path
	2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from zapio import settings
from django.conf.urls.static import static
from rest_framework.documentation import include_docs_urls
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# path ('manager/', include('ZapioApi.Api.BrandApi.managers.urls')),

schema_view = get_schema_view(
    openapi.Info(
        title="AizoTec APIDocs Swagger",
        default_version="v1",
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=False,
 #   permission_classes=(permissions.IsAuthenticated,),
    # authentication_classes=(authentication.SessionAuthentication,),
)

urlpatterns = [
    path("jet/", include("jet.urls", "jet")),
    path(
        "jet/dashboard/", include("jet.dashboard.urls", "jet-dashboard")
    ),  # Django JET dashboard URLS
    path("", admin.site.urls),
    path("accounts/", include("rest_framework.urls")),
    # path('apidocs/', get_schema_view()),
    path(
        "apidocs/",
        include_docs_urls(
            title="Zapio 2.0 APIs Doc",
            permission_classes=(permissions.IsAuthenticated,),
        ),
    ),
    path(
        "apidocs-swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    # path('apidocs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path("chaining/", include("smart_selects.urls")),
    path("api/", include("ZapioApi.urls")),
    path('api/customer/', include('Customers.urls')),
    path("api/front/", include("frontApi.urls")),
    path("api/dashboard/", include("ZapioApiV2.urls")),
    
    path("api/outlet/", include("Outlet.urls")),
    path("api/history/", include("History.urls")),
    path("api/notification/", include("Notification.urls")),
    path("api/Outletkitchen/", include("kitchen.urls")),
    path("api/pos/", include("PosApi.urls")),
    # path("api/test/", include("PosApi1.urls")),

    path("api/emailsetting/", include("ZapioApi.Api.BrandApi.emailsetting.urls")),
    path("api/UserRoll/", include("ZapioApi.Api.BrandApi.UserRollApi.urls")),
    path("api/v2/", include("ZapioApiV2.urls")),
    path("api/v2/", include("Brands.urls")),
    path("api/subscription/", include("Subscription.urls")),
    path("api/product/", include("Product.urls")),
    path("api/configuration/", include("Configuration.urls")),
    path("api/discount/", include("discount.urls")),
    path("api/manager/", include("UserRole.urls")),
    path("api/location/", include("Location.urls"))

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
