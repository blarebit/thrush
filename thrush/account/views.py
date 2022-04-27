"""Account views."""
from base.permissions import ThrushDjangoModelPermissions
from base.views import BaseViewSet
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django_filters import rest_framework as filters
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status, views, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .models import Address, User
from .serializers import (
    AddressSerializer,
    ChangePasswordSerializer,
    ContentTypeSerializer,
    GroupSerializer,
    LoginSerializer,
    PermissionSerializer,
    RegisterSerializer,
    UserSerializer,
    UserPublicInfoSerializer,
)


class ContentTypeFilter(filters.FilterSet):
    """Content type filter."""

    name = filters.CharFilter(field_name="model")

    class Meta:
        model = ContentType
        fields = ("name", "app_label")


class ContentTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """Content type view set."""

    permission_classes = [permissions.IsAuthenticated, ThrushDjangoModelPermissions]
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeSerializer
    filterset_class = ContentTypeFilter


class UserViewSet(BaseViewSet):
    """User view set."""

    permission_classes = [permissions.IsAuthenticated, ThrushDjangoModelPermissions]
    serializer_class = UserSerializer
    filterset_fields = (
        "username",
        "mobile",
        "first_name",
        "last_name",
        "email",
        "is_staff",
        "is_active",
        "date_joined",
    )


class UserPublicInfoViewSet(viewsets.ReadOnlyModelViewSet):
    """User public info view set."""

    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
    serializer_class = UserPublicInfoSerializer
    lookup_field = "id"


class GroupViewSet(BaseViewSet):
    """Group view set."""

    permission_classes = [permissions.IsAuthenticated, ThrushDjangoModelPermissions]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filterset_fields = ("name",)


class AddressViewSet(BaseViewSet):
    """Address view set."""

    permission_classes = [permissions.IsAuthenticated, ThrushDjangoModelPermissions]
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    filterset_fields = (
        "country",
        "city",
        "state",
        "post_code",
        "address",
        "street",
        "house_number",
        "floor",
        "unit",
    )

    # def get_queryset(self):
    #     """Only fetch address-related users."""
    #     return User.objects.filter(user=self.kwargs["user_pk"])


class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    """Permission view set."""

    permission_classes = [permissions.IsAuthenticated, ThrushDjangoModelPermissions]
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    filterset_fields = ("name", "codename")


class LoginView(views.APIView):
    """Login view."""

    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        """Handle POST method to authenticate a user."""
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(
            username=serializer.data["username"],
            password=serializer.data["password"],
        )
        if not user:
            return Response(
                data={"message": "invalid username or password"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not user.is_active:
            return Response(
                data={"message": "user is not activated yet"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        token = Token.objects.get_or_create(user=user)
        return Response(data={"token": token[0].key})


class LogoutView(views.APIView):
    """Logout view."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Handle GET request to logout a user."""
        request.user.auth_token.delete()
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangePasswordView(views.APIView):
    """Change a user's password view."""

    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(request_body=ChangePasswordSerializer)
    def patch(self, request):
        """Handle PATCH request to update a user's password."""
        serializer = ChangePasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if (
            serializer.data.get("username")
            and request.user.username != serializer.data["username"]
            and not request.user.has_perm("auth.change_user")
        ):
            return Response(
                {"message": "permission denied"}, status=status.HTTP_403_FORBIDDEN
            )

        if not request.user.has_perm("auth.change_user"):
            user = authenticate(
                username=serializer.data.get("username", request.user.username),
                password=serializer.data["old_password"],
            )
            if not user:
                return Response(
                    data={"message": "invalid username or password"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        else:
            if serializer.data.get("username"):
                user = User.objects.get(username=serializer.data["username"])
            else:
                user = request.user
        user.set_password(serializer.data["new_password"])
        user.save()
        return Response({"message": "password has been updated"})


class MyProfileView(generics.RetrieveAPIView, generics.UpdateAPIView):
    """User profile view."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        """DRF built-in method.

        Only return the current logged-in user object.
        """
        return self.request.user


class RegisterView(generics.CreateAPIView):
    """Register user view."""

    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


class VerifyView(views.APIView):
    """Verify account view."""

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        """Verify user email or phone number."""
        # Get the verification code.
        verification_code = request.query_params.get("code")
        if not verification_code:
            return Response(
                {"message": "verification code is empty"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Find in cache.
        user_id = cache.get(verification_code)
        if not user_id:
            return Response(
                {"message": "invalid verification code"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Activate the user.
        try:
            user = User.objects.get(id=int(user_id))
            user.is_active = True
            user.save()
        except User.DoesNotExist:
            return Response(
                {"message": "user not found"}, status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            {"message": "user has been successfully activated"},
            status=status.HTTP_200_OK,
        )
