"""URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
"""
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="AAP",
        default_version="v1",
        description="Admin Access Point API",
        terms_of_service="",
        contact=openapi.Contact(email="info@blarebit.com"),
        license=openapi.License(name=""),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Account.
    path("account/", include(("account.urls", "account"))),

    # Blog.
    path("blog/", include(("blog.urls", "blog"))),

    # Page.
    path("page/", include(("page.urls", "page"))),

    # Swagger.
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
