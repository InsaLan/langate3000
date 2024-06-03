"""
Network module. This module is responsible for the device and user connexion management.
"""

import sys, logging

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

from ..modules import netcontrol

logger = logging.getLogger(__name__)

class NetworkConfig(AppConfig):
    """Configuration of the Network Django App"""

    name = "langate.network"
    verbose_name = _("Network module")
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        """
            Reconnecting devices registered in the Device set but not in the Ipset
            This is important when for example the Ipset is flushed, you want the users that are already
            registered on the gate to be automatically reconnected when the gate restarts.
            This is important to maintain the consistency between the device state from django's point of view
            and the device state from the Ipset's point of view.
        """
        from langate.network.models import Device, UserDevice

        print(sys.argv)

        if not any(
            x in sys.argv
            for x in
            [
                'pylint_django',
                'makemigrations',
                'migrate',
                'shell',
                'createsuperuser',
                'flush',
                'collectstatic',
                'test',
            ]
        ):

            logger.info(_("[PortalConfig] Adding previously connected devices to the ipset"))

            for dev in Device.objects.all():
                connect_res = netcontrol.query("connect_user", {"mac": dev.mac, "name": dev.name})
                if not connect_res["success"]:
                    # If the device is a User device, we want to add it to the ipset
                    userdev = UserDevice.objects.filter(mac=dev.mac).first()
                    if userdev is not None:
                        logger.info(
                            "[PortalConfig] Could not connect device %s owned by user %s",
                            dev.mac,
                            userdev.user.username
                        )
                    else:
                        logger.info("[PortalConfig] Could not connect device %s", dev.mac)

                if dev.whitelisted:
                    mark_res = netcontrol.query("set_mark", {"mac": dev.mac, "mark": 100})
                    if not mark_res["success"]:
                        logger.info("[PortalConfig] Could not set mark 0 for device %s", dev.name)
