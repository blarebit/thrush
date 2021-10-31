"""Auth serializers."""
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers, exceptions, status

from .models import Profile


class ContentTypeSerializer(serializers.ModelSerializer):
    """Content type serializer."""

    class Meta:
        model = ContentType
        read_only_fields = ("name",)
        fields = (
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


class ProfileSerializer(serializers.ModelSerializer):
    """Profile serializer."""

    class Meta:
        model = Profile
        fields = (
            "mobile",
            "phone",
        )


class UserSerializer(serializers.ModelSerializer):
    """User serializer."""

    url = serializers.HyperlinkedIdentityField(view_name="account:user-detail")
    groups = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), many=True)
    permissions = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.all(), many=True, source="user_permissions"
    )
    profile = ProfileSerializer(many=False)

    class Meta:
        model = User
        read_ony_fields = ("last_login", "date_joined")
        fields = (
            "url",
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "groups",
            "permissions",
            "is_active",
            "last_login",
            "date_joined",
            "profile",
        )

    def validate(self, attrs):
        """DRF built-in method.

        Make sure an email is unique.
        """
        if User.objects.filter(email=attrs["email"]).exists():
            raise exceptions.ValidationError(
                detail={"message": "A user with that email already exists."},
                code=status.HTTP_400_BAD_REQUEST,
            )
        return super().validate(attrs)

    def create(self, validated_data):
        """DRF built-in method.

        Handles groups, permissions, and profile data.
        """
        profile = validated_data.pop("profile")
        groups = validated_data.pop("groups")
        permissions = validated_data.pop("user_permissions")

        user = User.objects.create_user(**validated_data)
        for group in groups:
            user.groups.add(group)
        for permission in permissions:
            user.user_permissions.add(permission)
        Profile.objects.create(**profile, user=user)
        return user


class LoginSerializer(serializers.Serializer):
    """Login serializer."""

    username = serializers.CharField()
    password = serializers.CharField()


class RegisterSerializer(serializers.ModelSerializer):
    """Register serializer."""

    class Meta:
        model = User
        fields = ("username", "email", "password")
        extra_kwargs = {"email": {"required": True}}

    def to_representation(self, instance):
        """DRF built-in method."""
        return {
            "username": instance.username,
            "email": instance.email,
        }

    def validate(self, attrs):
        """DRF built-in method.

        Make sure an email is unique.
        """
        if User.objects.filter(email=attrs["email"]).exists():
            raise exceptions.ValidationError(
                detail={"message": "A user with that email already exists."},
                code=status.HTTP_400_BAD_REQUEST,
            )
        return super().validate(attrs)


class ChangePasswordSerializer(serializers.Serializer):
    """Change password serializer."""

    username = serializers.CharField(required=False)
    old_password = serializers.CharField()
    new_password = serializers.CharField()
