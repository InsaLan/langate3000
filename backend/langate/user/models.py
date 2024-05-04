"""
Module for the definition of models tied to users
"""
from datetime import datetime

from django.contrib.auth.base_user import AbstractBaseUser as AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator

class UserManager(BaseUserManager):
    """
    Managers the User objects (kind of like a serializer but not quite that)
    """

    # pylint: disable=unused-argument
    def create_user(
        self, username, password, password_validation=None, **extra_fields
    ):
        """
        check that all required fields are present and create an user
        """
        if not username:
            raise ValueError(_("A username is required"))
        if not password:
            raise ValueError(_("A password is required"))
        user = self.model(
            username=username,
            date_joined=timezone.make_aware(datetime.now()),
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        """
        Check that all required fields are present and create a superuser
        """
        if password is None:
            raise TypeError(_("Superusers must have a password."))
        user = self.create_user(username, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    A user is simply our own abstraction defined above the standard Django User class.
    """

    username_validator: UnicodeUsernameValidator = UnicodeUsernameValidator()

    username = models.CharField(
        max_length=150,
        unique=True,
    )
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        """Meta options"""

        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    USERNAME_FIELD = "username"
    is_staff = models.BooleanField(
        verbose_name="Part of the insalan team", default=False
    )
    is_superuser = models.BooleanField(
        verbose_name="Admin of the insalan team", default=False
    )
    is_active = models.BooleanField(default=True)
    objects = UserManager()
