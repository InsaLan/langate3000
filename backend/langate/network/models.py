import random, logging
import re

from django.contrib.auth.base_user import AbstractBaseUser as AbstractBaseUser

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from langate.user.models import User
from langate.settings import netcontrol
from langate.settings import SETTINGS

from .utils import generate_dev_name, get_mark

logger = logging.getLogger(__name__)


def validate_mac(mac):
    """
    Validate a MAC address
    """
    if not re.match(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$', mac):
        raise ValidationError(_("Invalid MAC address"))


class Device(models.Model):
    """
    A device is a machine connected to the network
    """

    name = models.CharField(max_length=50)
    mac = models.CharField(
      max_length=17,
      unique=True,
      validators=[validate_mac]
    )
    whitelisted = models.BooleanField(default=False)
    mark = models.IntegerField(default=SETTINGS["marks"][0]["value"])

class UserDevice(Device):
    """
    A user device is a device that is connected to the network by a user
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ip = models.GenericIPAddressField(blank=False)

class DeviceManager(models.Manager):
    """
    Manager for the Device and UserDevice models
    """

    @staticmethod
    def create_device(mac, name, whitelisted=False, mark=None):
        """
        Create a device with the given mac address and name
        """
        if not name:
            name = generate_dev_name()
        if not mark:
            mark = SETTINGS["marks"][0]["value"]

        # Validate the MAC address
        validate_mac(mac)

        netcontrol.connect_user(mac, mark, name)
        logger.info("Connected device %s (the mac %s has been connected)", name, mac)

        try:
            device = Device.objects.create(mac=mac, name=name, whitelisted=whitelisted, mark=mark)
            device.save()
            return device
        except Exception as e:
            netcontrol.disconnect_user(mac)
            raise ValidationError(
              _("There was an error creating the device. Please try again.")
            ) from e

    @staticmethod
    def delete_device(mac):
        """
        Delete a device with the given mac address
        """
        netcontrol.disconnect_user(mac)
        logger.info("Disconnected device %s from the internet.", mac)

        device = Device.objects.get(mac=mac)
        device.delete()
        return device

    @staticmethod
    def create_user_device(user: User, ip, name=None):
        """
        Create a device with the given mac address
        """
        if not name:
            name = generate_dev_name()

        r = netcontrol.get_mac(ip)
        mac = r["mac"]

        # Validate the MAC address
        validate_mac(mac)

        mark = get_mark(user)
        netcontrol.connect_user(mac, mark, user.username)

        logger.info(
            "Connected device %s (owned by %s) at %s to the internet.",
            mac,
            user.username,
            ip
        )

        try:
            device = UserDevice.objects.create(mac=mac, name=name, user=user, ip=ip, mark=mark)
            device.save()
            return device
        except Exception as e:
            netcontrol.disconnect_user(mac)
            raise ValidationError(
              _("There was an error creating the device. Please try again.")
            ) from e

    @staticmethod
    def delete_user_device(Device):
        """
        Delete a device with the given mac address
        """
        return DeviceManager.delete_device(Device.mac)

    @staticmethod
    def edit_device(device: Device, mac, name, mark=None):
        """
        Edit the status of a device
        """
        # If name is provided, update it
        if name and name != device.name:
            device.name = name
        if mac and mac != device.mac:
            validate_mac(mac)
            # Disconnect the old MAC
            netcontrol.disconnect_user(device.mac)
            # Connect the new MAC
            netcontrol.connect_user(mac, device.mark, device.name)
            device.mac = mac
        if mark and mark != device.mark:
            # Check if the mark is valid
            if mark not in [m["value"] for m in SETTINGS["marks"]]:
                raise ValidationError(_("Invalid mark"))
            device.mark = mark
            netcontrol.set_mark(device.mac, mark)

        try:
            device.save()
        except Exception as e:
            raise ValidationError(_("The data provided is invalid")) from e
