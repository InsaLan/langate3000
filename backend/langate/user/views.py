"""User module API Endpoints"""

from django.contrib.auth import login, logout
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET
from rest_framework import generics, permissions, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from langate.user.serializers import (
    UserLoginSerializer,
    UserSerializer,
)

from .models import User, Role

@require_GET
@ensure_csrf_cookie
def get_csrf(request):
    """
    Returns a response setting CSRF cookie in headers
    """
    return JsonResponse({"csrf": _("CSRF cookie set")})


# Filter, can only acces this view when user.role == 'admin' or 'staff'
class StaffPermission(permissions.BasePermission):
    """
    Custom permission to only allow staff or admin to access the view
    """

    def has_permission(self, request, view):
        """
        Check if the user has the permission to access the view
        """
        if request.user.is_authenticated:
            return request.user.role in [Role.ADMIN, Role.STAFF]
        return False

class UserView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    permission_classes = [StaffPermission]
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

        return Response(user)

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
