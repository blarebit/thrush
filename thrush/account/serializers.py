"""Account serializers."""
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from rest_framework import exceptions, serializers, status

from .models import Address, User


class ContentTypeSerializer(serializers.ModelSerializer):
    """Content type serializer."""

    class Meta:
        model = ContentType
        read_only_fields = ("name",)
        fields = (
            "id",
            "name",
            "app_label",
        )


class PermissionSerializer(serializers.ModelSerializer):
    """Permission serializer."""

    url = serializers.HyperlinkedIdentityField(view_name="account:permission-detail")
    content_type = ContentTypeSerializer(many=False)

    class Meta:
        model = Permission
        read_only_fields = (
            "url",
            "id",
            "name",
            "content_type",
            "codename",
        )
        fields = (
            "url",
            "id",
            "name",
            "content_type",
            "codename",
        )


class GroupSerializer(serializers.ModelSerializer):
    """Group serializer."""

    url = serializers.HyperlinkedIdentityField(view_name="account:group-detail")
    permissions = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.all(), many=True
    )

    class Meta:
        model = Group
        fields = (
            "url",
            "id",
            "name",
            "permissions",
        )


class AddressSerializer(serializers.ModelSerializer):
    """Address serializer."""

    url = serializers.HyperlinkedIdentityField(view_name="account:address-detail")

    class Meta:
        model = Address
        fields = (
            "url",
            "id",
            "user",
            "name",
            "country",
            "city",
            "state",
            "post_code",
            "address",
            "street",
            "house_number",
            "floor",
            "unit",
            "is_default",
        )


class UserSerializer(serializers.ModelSerializer):
    """User's profile serializer."""

    groups = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), many=True)
    addresses = AddressSerializer(many=True, read_only=True, source="address_user")
    permissions = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.all(), many=True, source="user_permissions"
    )

    class Meta:
        model = User
        read_ony_fields = ("last_login", "date_joined")
        fields = (
            "id",
            "username",
            "mobile",
            "email",
            "first_name",
            "last_name",
            "groups",
            "addresses",
            "permissions",
            "is_active",
            "last_login",
            "date_joined",
        )

    def _exists(self, query: Q):
        """Check user attribute existence.

        Raises:
            exceptions.ValidationError: if a user with an attribute exists.
        """
        if User.objects.filter(query, ~Q(user=self.context["request"].user)).exists():
            raise exceptions.ValidationError(
                detail={"message": "A user with this info already exists."},
                code=status.HTTP_400_BAD_REQUEST,
            )

    def validate(self, attrs):
        """DRF built-in method.

        Make sure an email is unique.
        """
        # Registration.
        if not self.instance:
            self._exists(Q(mobile=attrs["mobile"]))
            if attrs.get("username"):
                self._exists(Q(username=attrs["username"]))
        return super().validate(attrs)

    def create(self, validated_data):
        """DRF built-in method.

        Handles groups, permissions, and profile data.
        """
        groups = validated_data.pop("groups")
        permissions = validated_data.pop("user_permissions")

        user = User.objects.create_user(**validated_data)
        for group in groups:
            user.groups.add(group)
        for permission in permissions:
            user.user_permissions.add(permission)
        return user


class UserGeneralInfoSerializer(serializers.ModelSerializer):
    """User's public info serializer."""

    url = serializers.HyperlinkedIdentityField(view_name="account:user-detail")

    class Meta:
        model = User
        fields = (
            "url",
            "id",
            "first_name",
            "last_name",
            "is_active",
        )


class LoginSerializer(serializers.Serializer):
    """Login serializer."""

    username = serializers.CharField()
    password = serializers.CharField()


class RegisterSerializer(serializers.ModelSerializer):
    """Register serializer."""

    class Meta:
        model = User
        fields = ("username", "mobile", "email", "password")

    def to_representation(self, instance):
        """DRF built-in method."""
        return {
            "username": instance.username,
            "email": instance.email,
            "mobile": instance.mobile,
        }

    def validate(self, attrs):
        """Customized 'validate' method to encrypt password."""
        if attrs.get("password"):
            attrs["password"] = make_password(attrs["password"])
        return super().validate(attrs)


class ChangePasswordSerializer(serializers.Serializer):
    """Change password serializer."""

    username = serializers.CharField(required=False)
    old_password = serializers.CharField()
    new_password = serializers.CharField()

