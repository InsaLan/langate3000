import sys

from datetime import datetime

from django.contrib.auth import login, logout
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import PermissionDenied, BadRequest
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET
from rest_framework import generics, permissions, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator  # Add this import

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from langate.user.serializers import (
    UserLoginSerializer,
    UserSerializer,
)

from langate.user.models import User, Role
from langate.network.models import Device, UserDevice

from langate.network.serializers import DeviceSerializer, UserDeviceSerializer, FullDeviceSerializer

class StaffPermission(permissions.BasePermission):
    """
    Custom permission to only allow staff or admin to access the view
    """

    def has_permission(self, request, view):
        """
        Check if the user has the permission to access the view
        """
        if request.user.is_authenticated:
            return request.user.role in [Role.ADMIN, Role.STAFF]
        return False

class DeviceList(generics.ListCreateAPIView):
    """
    API endpoint that allows devices to be viewed or created.
    """
    serializer_class = FullDeviceSerializer
    permission_classes = [StaffPermission]

    def get_queryset(self):
        """
        Return a list of all UserDevice and Device objects.
        """
        user_devices = UserDevice.objects.all()
        # devices that are not in user_devices
        devices = Device.objects.exclude(id__in=user_devices.values_list('id', flat=True))

        queryset = list(user_devices) + list(devices)

        # order by id
        queryset = sorted(queryset, key=lambda x: x.id)

        return queryset

    def post(self, request):
        """
        Create a new User device
        """
        serializer = FullDeviceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeviceDetail(generics.RetrieveAPIView):
    """
    API endpoint that allows a device to be viewed, updated, or deleted.
    """
    serializer_class = FullDeviceSerializer
    permission_classes = [StaffPermission]

    def get(self, request, pk):
        """
        Get a device by its primary key
        """
        try:
            device = UserDevice.objects.get(pk=pk)
            serializer = FullDeviceSerializer(device)
            return Response(serializer.data)
        except UserDevice.DoesNotExist:
            try:
                device = Device.objects.get(pk=pk)
                serializer = FullDeviceSerializer(device)
                return Response(serializer.data)
            except Device.DoesNotExist:
                return Response({"error": _("Device not found")}, status=status.HTTP_404_NOT_FOUND)

class DeviceWhitelist(generics.ListAPIView):
    """
    API endpoint that allows devices to be viewed.
    Creation of Whitelist devices need to be done with the DeviceList view.
    """
    queryset = Device.objects.filter(whitelisted=True)
    serializer_class = DeviceSerializer
    permission_classes = [StaffPermission]
