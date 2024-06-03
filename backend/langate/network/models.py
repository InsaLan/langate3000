import random, logging

from django.contrib.auth.base_user import AbstractBaseUser as AbstractBaseUser

from django.db import models
from django.utils.translation import gettext_lazy as _

from langate.user.models import User
from langate.modules import netcontrol

logger = logging.getLogger(__name__)

def generate_dev_name():
    """
        Generate a random device name based on a list of names
    """
    try:
        with open("assets/misc/device_names.txt", "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
            return random.choice(lines)

    except FileNotFoundError:
        return "Computer"


class Device(models.Model):
    """
    A device is a machine connected to the network
    """

    name = models.CharField(max_length=100)
    mac = models.CharField(max_length=17)
    whitelisted = models.BooleanField(default=False)

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
    def create_device(mac, name, whitelisted=False):
        """
        Create a device with the given mac address and name
        """
        if not name:
            name = generate_dev_name()

        netcontrol.query("connect", { "mac": mac, "name": name })
        logger.info("Connected device %s (the mac %s has been connected)", name, mac)

        device = Device.objects.create(mac=mac, name=name, whitelisted=whitelisted)
        return device

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

        netcontrol.query("connect_user", { "mac": mac, "name": user.username })

        logger.info(
            "Connected device %s (owned by %s) at %s to the internet.",
            mac,
            user.username,
            ip
        )

        device = UserDevice.objects.create(mac=mac, name=name, user=user, ip=ip, area=area)
        return device
