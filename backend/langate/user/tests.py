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

from langate.user.models import User, Role


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
        u.role = Role.STAFF

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
        self.assertTrue(u.has_usable_password())
        self.assertTrue(u.check_password("IUseAVerySecurePassword"))
        self.assertTrue(u.is_active)
        self.assertEqual(u.role, Role.PLAYER)


    def test_get_existing_minimal_user(self):
        """
        Test getting all the fields of an user created with only the required fields
        """
        u: User = User.objects.get(username="anotherplayer")
        self.assertEqual(u.get_username(), "anotherplayer")
        self.assertTrue(u.has_usable_password())
        self.assertTrue(u.check_password("ThisIsPassword"))
        self.assertTrue(u.is_active)
        self.assertEqual(u.role, Role.PLAYER)

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
