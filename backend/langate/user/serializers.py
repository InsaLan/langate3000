"""Data Serializers for the langate User module"""
# pylint: disable=too-few-public-methods

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _

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
