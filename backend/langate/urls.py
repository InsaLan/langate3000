"""langate URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from os import getenv

from django.urls import re_path
from django.contrib import admin
from django.views.generic.base import RedirectView
from django.urls import include, path
from rest_framework import routers
from rest_framework import permissions

router = routers.DefaultRouter()
# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path("", include(router.urls)),
    path("user/", include("langate.user.urls")),
]
if getenv("DEV", "1") == "1":
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi

    schema_view = get_schema_view(
        openapi.Info(
            title="langate API",
            default_version='',
            description="Cette API est l'API de la langate. Elle permet de gérer les utilisateurs, et leur permet de s'authentifier.",
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )

    urlpatterns += [
        re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
        path("swagger/", schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path("redoc/", schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-ui'),
    ]

# Set admin site url correctly for the admin panel
admin.site.site_url = getenv("HTTP_PROTOCOL", "http") + "://" + getenv("WEBSITE_HOST", "localhost")
