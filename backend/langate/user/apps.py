"""
User module. Meant to manage registering, login, email confirmation, password
resets,..."""

import logging, sys

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)

class UserConfig(AppConfig):
    """Configuration of the User Django App"""

    name = "langate.user"
    verbose_name = _("User module")
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self):
        """Adding all users to the Prometheus counter.
        """
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
            from langate.user.models import User, users_counter

            users_count = User.objects.count()
            logger.info(_(f"[PortalConfig] Loaded {users_count} users"))
            users_counter.inc(amount=users_count)
