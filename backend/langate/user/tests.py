"""User Tests Module"""
import json
import re

from typing import Dict
from django.test import TestCase
from django.core import mail
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Permission

from rest_framework.test import APIClient
from rest_framework import serializers

from langate.user.models import User


class UserTestCase(TestCase):
    """
    Tests of the User model
    """

    def setUp(self):
        """
        Create some base users to do operations on
        """
        u: User = User.objects.create_user(
            username="staffplayer",
            password="^ThisIsAnAdminPassword42$",
        )
        u.is_staff = True

        User.objects.create_user(
            username="randomplayer",
            password="IUseAVerySecurePassword",
        )
        User.objects.create_user(
            username="anotherplayer",
            password="ThisIsPassword",
        )

    def test_get_existing_full_user(self):
        """
        Test getting all the fields of an already created user
        """
        u: User = User.objects.get(username="randomplayer")
        self.assertEqual(u.get_username(), "randomplayer")
        self.assertEqual(u.get_user_permissions(), set())
        self.assertTrue(u.has_usable_password())
        self.assertTrue(u.check_password("IUseAVerySecurePassword"))
        self.assertTrue(u.is_active)
        self.assertFalse(u.is_staff)

    def test_get_existing_minimal_user(self):
        """
        Test getting all the fields of an user created with only the required fields
        """
        u: User = User.objects.get(username="anotherplayer")
        self.assertEqual(u.get_username(), "anotherplayer")
        self.assertEqual(u.get_user_permissions(), set())
        self.assertTrue(u.has_usable_password())
        self.assertTrue(u.check_password("ThisIsPassword"))
        self.assertTrue(u.is_active)
        self.assertFalse(u.is_staff)

    def test_get_non_existing_user(self):
        """
        Test that getting an user which does not exist throws an `User.DoesNotExist` error
        """
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(username="idontexist")


class UserEndToEndTestCase(TestCase):
    """
    Test cases of the API endpoints and workflows related to user model
    """

    client: APIClient

    def setUp(self):
        """
        Create a player to test getters
        """
        self.client = APIClient()
        user = User.objects.create_user(
            username="randomplayer",
            password="IUseAVerySecurePassword",
            is_active=True,
        )

    def test_register_invalid_data(self):
        """
        Test trying to register a few invalid users
        """

        def send_invalid_data(data):
            request = self.client.post("/user/register/", data, format="json")
            self.assertEqual(request.status_code, 400)
        send_invalid_data({})
        send_invalid_data({"username": "newuser"})

    def test_register_valid_account(self):
        """
        Test registering valid users
        """

        def send_valid_data(data, check_fields=[]):
            """
            Helper function that will request a register and check its output
            """
            request = self.client.post("/user/register/", data, format="json")

            self.assertEqual(request.status_code, 201)

            created_data: Dict = request.data
            for k, v in check_fields:
                self.assertEqual(created_data[k], v)

        send_valid_data(
            {
                "username": "newplayer",
                "password": "1111qwer!",
                "password_validation": "1111qwer!",
            },
            [
                ("username", "newplayer"),
                ("is_staff", False),
                ("is_superuser", False),
                ("is_active", True),
            ],
        )
        send_valid_data(
            {
                "username": "PeachLover3003",
                "password": "1111qwer!",
                "password_validation": "1111qwer!",
            },
            [
                ("username", "PeachLover3003"),
                ("is_staff", False),
                ("is_superuser", False),
                ("is_active", True),
            ],
        )

    def test_register_read_only_fields(self):
        """
        Test that the read-only register fields are indeed read-only
        """

        def send_valid_data(data, check_fields=[]):
            request = self.client.post("/user/register/", data, format="json")

            self.assertEqual(request.status_code, 201)

            created_data: Dict = request.data
            for k, v in check_fields:
                self.assertEqual(created_data[k], v)

        send_valid_data(
            {
                "username": "newplayer",
                "password": "1111qwer!",
                "password_validation": "1111qwer!",
                "is_staff": "true",
                "is_superuser": "true",
                "is_active": "false",
            },
            [
                ("username", "newplayer"),
                ("is_staff", False),
                ("is_superuser", False),
                ("is_active", True),
            ],
        )

    def test_login_invalid_account(self):
        """
        Try to login with invalid requests
        """

        def send_valid_data(data):
            request = self.client.post("/user/login/", data, format="json")

            self.assertEqual(request.status_code, 404)
            self.assertEqual(
                request.data["user"][0],
                _("Bad Username or password"),
            )

        send_valid_data(
            {
                "username": "newplayer",
                "password": "1111qwer!",
            }
        )

    def test_login_account(self):
        """
        Test that when everything is ok, an user is able to login
        """
        user = User.objects.create_user(
            username="newplayer",
            password="1111qwer!",
            is_active=True,
        )

        def send_valid_data(data):
            request = self.client.post("/user/login/", data, format="json")

            self.assertTrue("sessionid" in self.client.cookies)

        send_valid_data(
            {
                "username": "newplayer",
                "password": "1111qwer!",
            }
        )
