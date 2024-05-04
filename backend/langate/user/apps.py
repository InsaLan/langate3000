"""
User module. Meant to manage registering, login, email confirmation, password
resets,..."""

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UserConfig(AppConfig):
    """Configuration of the User Django App"""

    name = "langate.user"
    verbose_name = _("User module")
    default_auto_field = "django.db.models.BigAutoField"
