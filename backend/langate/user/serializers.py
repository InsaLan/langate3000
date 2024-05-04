"""Data Serializers for the langate User module"""
# pylint: disable=too-few-public-methods

from django.contrib.auth import authenticate
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for an User"""

    class Meta:
        """Meta class, used to set parameters"""

        model = User
        exclude = ("password",)
        # fields = ['url', 'username', 'email', 'groups']


class UserRegisterSerializer(serializers.ModelSerializer):
    """Serializer for a register for submission"""

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password_validation = serializers.CharField(write_only=True, required=True)

    class Meta:
        """Meta class, used to set parameters"""

        model = User
        fields = [
            "username",
            "is_active",
            "is_staff",
            "is_superuser",
            "password",
            "password_validation",
        ]

        read_only_fields = ("is_superuser", "is_active", "is_staff")
        write_only_fields = ("name", "password", "password_validation")

    def validate(self, data):
        """
        Validate user registration (password shall be confirmed)
        """
        if data["password"] != data["password_validation"]:
            raise serializers.ValidationError(_("Passwords do not match"))
        return data

    def create(self, data):
        user_object = User.objects.create_user(**data)
        user_object.save()
        return user_object


class UserLoginSerializer(serializers.Serializer):
    """Serializer for a login form submission"""

    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        """Meta class, used to set parameters"""

        model = User

    def check_validity(self, data):
        """
        Checks thats:
            - Username & Password combination gives a good user
            - The account has not been deactivated
        """
        user = authenticate(username=data["username"], password=data["password"])
        if user is not None:
            if not user.is_active:
                raise serializers.ValidationError(_("User account is disabled"))
        return user


class PermissionSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for a django Permission"""

    class Meta:
        """Meta class, used to set parameters"""

        model = Permission
        exclude = ("content_type",)


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    """Serializer for a django Group (used with Permissions)"""

    class Meta:
        """Meta class, used to set parameters"""

        model = Group
        exclude = ()
        # fields = ['url', 'name']
