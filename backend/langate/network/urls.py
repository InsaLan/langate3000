"""url for network"""
from django.urls import path

from . import views

urlpatterns = [
    path("devices/", views.DeviceList.as_view(), name="device-list"),
    path("userdevices/", views.UserDeviceList.as_view(), name="user-devices"),
    path("devices/<int:pk>/", views.DeviceDetail.as_view(), name="device-detail"),
    path("devices/whitelist/", views.DeviceWhitelist.as_view(), name="device-whitelist"),
]
