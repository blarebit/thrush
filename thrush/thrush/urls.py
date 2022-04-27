"""URL Configuration.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from .views import health_check

schema_view = get_schema_view(
    openapi.Info(
        title="Thrush",
        default_version="v1",
        description="Admin Access Point API",
        terms_of_service="",
        contact=openapi.Contact(email="info@blarebit.com"),
        license=openapi.License(name="Apache-2.0"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    # Account.
    path("account/", include(("account.urls", "account"))),

    # Blog.
    path("blog/", include(("blog.urls", "blog"))),

    # Cart.
    # path("shop/", include(("shop.cart.urls", "cart"))),

    # Payment.
    # path("shop/", include(("shop.payment.urls", "payment"))),

    # Media (file/directory) manager.
    # path("file/", include(("file.urls", "file"))),

    # Page.
    # path("page/", include(("page.urls", "page"))),

    # Slideshow.
    # path("slideshow/", include(("slideshow.urls", "slideshow"))),

    # Products.
    # path("shop/products/", include(("shop.product.urls", "products"))),

    # # Price.
    # path("shop/price/", include(("shop.price.urls", "price"))),

    # Health check.
    path("health-check/", health_check),

    # Swagger.
    # path(
        # "swagger/",
        # schema_view.with_ui("swagger", cache_timeout=0),
        # name="schema-swagger-ui",
    # ),
]

if settings.ENVIRONMENT == "development":
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
