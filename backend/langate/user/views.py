"""User module API Endpoints"""

import sys

from datetime import datetime

from django.contrib.auth import login, logout
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import PermissionDenied, BadRequest
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET
from rest_framework import generics, permissions, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ValidationError

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from langate.user.serializers import (
    GroupSerializer,
    PermissionSerializer,
    UserLoginSerializer,
    UserRegisterSerializer,
    UserSerializer,
)

from .models import User, UserManager

@require_GET
@ensure_csrf_cookie
def get_csrf(request):
    """
    Returns a response setting CSRF cookie in headers
    """
    return JsonResponse({"csrf": _("CSRF cookie set")})


class UserView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = [SessionAuthentication]
    serializer_class = UserSerializer


class UserMe(generics.RetrieveAPIView):
    """
    API endpoint that allows a logged in user to get and set some of their own
    account fields.
    """

    authentication_classes = [SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request):
        """
        Returns an user's own informations
        """
        user = UserSerializer(request.user, context={"request": request}).data

        user_groups = []
        for group in request.user.groups.all():
            user_groups.append(group.name)

        user["groups"] = user_groups

        return Response(user)

class PermissionViewSet(generics.ListCreateAPIView):
    """
    Django's `Permission` ViewSet to be able to add them to the admin panel
    """

    queryset = Permission.objects.all().order_by("name")
    serializer_class = PermissionSerializer
    permission_classes = [permissions.IsAdminUser]


class GroupViewSet(generics.ListCreateAPIView):
    """
    Django's `Group` ViewSet to be able to add them to the admin panel
    """

    queryset = Group.objects.all().order_by("name")
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAdminUser]

class UserRegister(generics.CreateAPIView):
    """
    API endpoint that allows user creation.
    """

    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegisterSerializer


class UserLogin(APIView):
    """
    API endpoint that allows user login.
    """

    permission_classes = [permissions.AllowAny]
    authentication_classes = [SessionAuthentication]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "username": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description=_("Username")
                ),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description=_("Password")
                ),
            },
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "user": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description=_("User logged in")
                    )
                }
            ),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "user": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description=_("Invalid data format")
                        )
                    )
                }
            ),
            404: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "user": openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(
                            type=openapi.TYPE_STRING,
                            description=_("Bad Username or password")
                        )
                    )
                }
            )
        }
    )
    def post(self, request):
        """
        Submit a login form
        """
        data = request.data
        serializer = UserLoginSerializer(data=data, context={"request": request})
        if serializer.is_valid():
            user = serializer.check_validity(data)
            if user is None:
                return Response(
                    {"user": [_("Bad Username or password")]},
                    status=status.HTTP_404_NOT_FOUND,
                )
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        return Response(
            {"user": [_("Invalid data format")]},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserLogout(APIView):
    """
    API endpoint that allows a user to logout.
    """

    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        """
        Will logout an user.
        """
        logout(request)
        return Response(status=status.HTTP_200_OK)
