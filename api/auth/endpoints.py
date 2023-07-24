from django.urls import path
from rest_framework import routers
from . import api

urlpatterns = [
    path('profile/', api.ProfileApiView.as_view()),
    path('login/', api.LoginApi.as_view()),
    path('register/', api.RegisterApi.as_view()),
]
