"""Data Serializers for the langate Network module"""
# pylint: disable=too-few-public-methods

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Device, UserDevice

class DeviceSerializer(serializers.ModelSerializer):
    """Serializer for a Device"""

    class Meta:
        """Meta class, used to set parameters"""

        model = Device
        exclude = ()


class UserDeviceSerializer(serializers.ModelSerializer):
    """Serializer for an UserDevice"""

    class Meta:
        """Meta class, used to set parameters"""

        model = UserDevice
        exclude = ()
