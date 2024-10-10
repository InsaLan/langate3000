import random, logging
import re

from django.contrib.auth.base_user import AbstractBaseUser as AbstractBaseUser

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from langate.user.models import User
from langate.modules import netcontrol

from langate.settings import SETTINGS

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

    name = models.CharField(max_length=100)
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

    # Area of the device, i.e. LAN or WiFi
    area = models.CharField(max_length=4, default="LAN")

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

        netcontrol.query("connect", { "mac": mac, "name": name })
        netcontrol.query("set_mark", { "mac": mac, "mark": mark })
        logger.info("Connected device %s (the mac %s has been connected)", name, mac)

        try:
            device = Device.objects.create(mac=mac, name=name, whitelisted=whitelisted, mark=mark)
            device.save()
            return device
        except Exception as e:
            netcontrol.query("disconnect_user", { "mac": mac })
            raise ValidationError(
              _("There was an error creating the device. Please try again.")
            ) from e

    @staticmethod
    def delete_device(mac):
        """
        Delete a device with the given mac address
        """
        netcontrol.query("disconnect_user", { "mac": mac })
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

        r = netcontrol.query("get_mac", { "ip": ip })
        mac = r["mac"]
        area = "LAN"

        # Validate the MAC address
        validate_mac(mac)

        netcontrol.query("connect_user", { "mac": mac, "name": user.username })

        logger.info(
            "Connected device %s (owned by %s) at %s to the internet.",
            mac,
            user.username,
            ip
        )

        try:
            device = UserDevice.objects.create(mac=mac, name=name, user=user, ip=ip, area=area)
            device.save()
            return device
        except Exception as e:
            netcontrol.query("disconnect_user", { "mac": mac })
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
    def edit_whitelist_device(device: Device, mac, name, mark=None):
        """
        Edit the whitelist status of a device
        """
        # If name is provided, update it
        if name and name != device.name:
            device.name = name
        if mac and mac != device.mac:
          validate_mac(mac)
          # Disconnect the old MAC
          netcontrol.query("disconnect_user", { "mac": device.mac })

          # Connect the new MAC
          netcontrol.query("connect", { "mac": mac, "name": device.name })
          device.mac = mac
        if mark and mark != device.mark:
            device.mark = mark

        device.save()

def generate_dev_name():
    """
        Generate a random device name based on a list of names
    """
    try:
        with open("assets/misc/device_names.txt", "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
            taken_names = Device.objects.values_list("name", flat=True)

            if len(taken_names) < len(lines) :
                n = random.choice(lines)
                while n in taken_names:
                    n = random.choice(lines)
                return n

            else:
                return random.choice(lines)

    except FileNotFoundError:
        return "MISSINGNO"
