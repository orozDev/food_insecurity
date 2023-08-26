from django.urls import path, include
from rest_framework import routers
from . import api

router = routers.DefaultRouter()
router.register('users', api.UserViewSet)

urlpatterns = [
    path('profile/', api.ProfileApiView.as_view()),
    path('login/', api.LoginApi.as_view()),
    path('register/', api.RegisterApi.as_view()),
    path('', include(router.urls)),
]
