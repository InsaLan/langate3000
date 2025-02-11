"""Data Serializers for the langate User module"""
# pylint: disable=too-few-public-methods

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for an User"""

    class Meta:
        """Meta class, used to set parameters"""

        model = User
        exclude = ("password",)
        read_only_fields = ("date_joined",)
        # fields = ['url', 'username', 'email', 'groups']

class UserRegisterSerializer(serializers.ModelSerializer):
    """Serializer for a registration form submission"""

    class Meta:
        """Meta class, used to set parameters"""

        model = User
        read_only_fields = ("date_joined",)
        fields = "__all__"

    def create(self, validated_data):
        """
        Create a new user with the given data
        """
        if not "username" in validated_data:
            raise serializers.ValidationError(_("A username is required"))
        if not "password" in validated_data:
            raise serializers.ValidationError(_("A password is required"))
        validate_password(validated_data["password"])
        user = User.objects.create_user(**validated_data)
        return user

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
                raise serializers.ValidationError(_("User account disabled"))
        return user
