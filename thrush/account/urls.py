"""Auth URLs."""
from django.urls import include, path
from rest_framework import routers

from .views import (
    AddressViewSet,
    ChangePasswordView,
    ContentTypeViewSet,
    GroupViewSet,
    LoginView,
    LogoutView,
    MyProfileView,
    PermissionViewSet,
    RegisterView,
    UserViewSet,
    VerifyView,
)

router = routers.DefaultRouter()
router.register("users", UserViewSet, basename="user")
router.register("address", AddressViewSet, basename="address")
router.register("groups", GroupViewSet, basename="group")
router.register("permissions", PermissionViewSet, basename="permission")
router.register("content_types", ContentTypeViewSet, basename="content_type")

urlpatterns = [
    path("", include(router.urls)),
    path("me/", MyProfileView.as_view(), name="profile"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("password/", ChangePasswordView.as_view(), name="password"),
    path("verify/", VerifyView.as_view(), name="verification"),
]
