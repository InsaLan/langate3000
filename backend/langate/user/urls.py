"""url for user"""
from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.UserRegister.as_view(), name="/register"),
    path("login/", views.UserLogin.as_view(), name="/login"),
    path("logout/", views.UserLogout.as_view(), name="/logout"),
    path("data/<int:pk>/", views.UserView.as_view(), name="/"),
    path("me/", views.UserMe.as_view(), name="me"),
    path("get-csrf/", views.get_csrf, name="get-csrf"),
]
