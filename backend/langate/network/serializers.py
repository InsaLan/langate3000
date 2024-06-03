"""Data Serializers for the langate Network module"""
# pylint: disable=too-few-public-methods

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from langate.network.models import Device, UserDevice, DeviceManager
from langate.user.models import User

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


class FullDeviceSerializer(serializers.Serializer):
    """
    Serializer that can handle both UserDevice and Device objects.
    """
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    mac = serializers.CharField(max_length=17)
    whitelisted = serializers.BooleanField()
    ip = serializers.IPAddressField(allow_null=True)
    user = serializers.CharField(allow_null=True)
    area = serializers.CharField(allow_null=True)

    def to_representation(self, instance):
        """
        Convert the instance to a dictionary that can be used to create a Response.
        """
        representation = super().to_representation(instance)

        # If the instance is a Device, set ip, user, and area to None
        if isinstance(instance, UserDevice):
            representation['ip'] = instance.ip
            representation['user'] = instance.user.username
            representation['area'] = instance.area
        else:
            representation['ip'] = None
            representation['user'] = None
            representation['area'] = None

        return representation
