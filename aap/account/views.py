"""Auth views."""
import random
import redis
from django.conf import settings
from base.permissions import AAPDjangoModelPermissions
from django.contrib.auth import authenticate, logout
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django_filters import rest_framework as filters
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status, views, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from .models import User, Address
from .serializers import (
    ChangePasswordSerializer,
    ContentTypeSerializer,
    GroupSerializer,
    LoginSerializer,
    PermissionSerializer,
    RegisterSerializer,
    UserSerializer,
    AddressSerializer,
)


class ContentTypeFilter(filters.FilterSet):
    """Content type filter."""

    name = filters.CharFilter(field_name="model")

    class Meta:
        model = ContentType
        fields = ("name", "app_label")


class ContentTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """Content type view set."""

    permission_classes = [permissions.IsAuthenticated, AAPDjangoModelPermissions]
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeSerializer
    filterset_class = ContentTypeFilter


class UserViewSet(viewsets.ModelViewSet):
    """User view set."""

    permission_classes = [permissions.IsAuthenticated, AAPDjangoModelPermissions]
    queryset = User.objects.all()
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


class GroupViewSet(viewsets.ModelViewSet):
    """Group view set."""

    permission_classes = [permissions.IsAuthenticated, AAPDjangoModelPermissions]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filterset_fields = ("name",)


class AddressViewSet(viewsets.ModelViewSet):
    """Address view set."""

    permission_classes = [permissions.IsAuthenticated, AAPDjangoModelPermissions]
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    filterset_fields = ("country", "city", "state", "post_code", "address", "street", "house_number", "floor", "unit",)

    # def get_queryset(self):
    #     """Only fetch address-related users."""
    #     return User.objects.filter(user=self.kwargs["user_pk"])


class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    """Permission view set."""

    permission_classes = [permissions.IsAuthenticated, AAPDjangoModelPermissions]
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
                username=serializer.data.get("username") or request.user,
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


class Verify(views.APIView):
    """ٰVerify view."""

    redis_host = settings.REDIS_HOST
    redis_port = settings.REDIS_PORT
    redis_password = settings.REDIS_PASS

    permission_classes = [permissions.AllowAny]

    # @swagger_auto_schema(request_body=LoginSerializer)
    # @swagger_auto_schema(request_body="")
    def get(self, request):
        """Handle GET method to verify user's email or phone number."""
        # serializer = LoginSerializer(data=request.data)
        user_id = self.request.user.id
        code = random.randint(100000, 999999)
        verify_it = list(request.query_params.keys())[0]

        if verify_it in ('phone', 'email'):
            # Redis dictionary data
            verify_dict = {
                "user_id": user_id,
                "code": code,
                "verify": verify_it,
            }
            self.set_redis(verify_dict)
            self.verify_email(code) if verify_it == 'email' else self.verify_phone(code)
        elif verify_it == 'code':
            # Lookup the code in redis and find user_id, then verify it
            verify_dict = self.get_redis(request.query_params)
            User.objects.filter(id=user_id).update(
                'email_verified' if verify_it == 'email' else 'mobile_verified=True'
            )
            return Response({"Message": "You are verified!"}, status=status.HTTP_200_OK)
        else:
            return Response({"Error": "You just can verify email or phone!"}, status=status.HTTP_400_BAD_REQUEST)

        # if not serializer.is_valid():
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #
        # user = authenticate(
        #     username=serializer.data["username"],
        #     password=serializer.data["password"],
        # )
        # if not user:
        #     return Response(
        #         data={"message": "invalid username or password"},
        #         status=status.HTTP_401_UNAUTHORIZED,
        #     )
        #
        # token = Token.objects.get_or_create(user=user)
        # return Response(data={"token": token[0].key})
        return Response()

    def verify_email(self, *args):
        pass

    def verify_phone(self, *args):
        pass

    def set_redis(self, *args):
        """Redis Program"""

        # step 3: create the Redis Connection object
        try:

            # The decode_repsonses flag here directs the client to convert the responses from Redis into Python strings
            # using the default encoding utf-8.  This is client specific.
            r = redis.StrictRedis(
                host=self.redis_host,
                port=self.redis_port,
                password=self.redis_password,
                decode_responses=True
            )

            # step 4: Set the hello message in Redis
            # r.set("msg:hello", "Hello Redis!!!")
            r.set("verify_code:"+str(args[0]["code"]), args[0])

        except Exception as e:
            return Response({"Error": e}, status=status.HTTP_400_BAD_REQUEST)

    def get_redis(self, *args):
        """Redis Program"""

        # step 3: create the Redis Connection object
        try:

            # The decode_repsonses flag here directs the client to convert the responses from Redis into Python strings
            # using the default encoding utf-8.  This is client specific.
            r = redis.StrictRedis(
                host=self.redis_host,
                port=self.redis_port,
                password=self.redis_password,
                decode_responses=True
            )

            # step 5: Retrieve the hello message from Redis
            # msg = r.get("msg:hello")
            # print(msg)
            return r.get("verify_code:"+str(args[0]["code"]))

        except Exception as e:
            return Response({"Error": e}, status=status.HTTP_400_BAD_REQUEST)
