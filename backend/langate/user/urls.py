"""url for user"""
from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.UserLogin.as_view(), name="/login"),
    path("logout/", views.UserLogout.as_view(), name="/logout"),
    path("me/", views.UserMe.as_view(), name="me"),
    path("get-csrf/", views.get_csrf, name="get-csrf"),
    path("users/", views.UserList.as_view(), name="users"),
    path("users/<int:pk>/", views.UserView.as_view(), name="/"),
    path("change-password/<int:pk>/", views.ChangePassword.as_view(), name="change-password"),
]
