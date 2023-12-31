from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authtoken.models import Token
from rest_framework import status, viewsets, filters
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from api.mixins import PaginationBreaker
from .serializers import LoginSerializer, UserSerializer, ProfileSerializer, RegisterUserSerializer
from account.models import User
from ..paginations import StandardResultsSetPagination


class LoginApi(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        login_serializer = self.serializer_class(data=request.data)
        login_serializer.is_valid(raise_exception=True)
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user:
            serializer = UserSerializer(user, many=False, context={'request': request})
            token = Token.objects.get_or_create(user=user)[0].key
            data = {**serializer.data, 'token': f'{token}'}
            return Response(data, status.HTTP_200_OK)
        return Response({'login': _('Не существует пользователя или неверный пароль')},
                        status.HTTP_400_BAD_REQUEST)


class RegisterApi(GenericAPIView):

    serializer_class = RegisterUserSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        response_serializer = UserSerializer(user, many=False, context={'request': request})
        token = Token.objects.get_or_create(user=user)[0].key
        data = {**response_serializer.data, 'token': f'{token}'}
        return Response(data, status.HTTP_201_CREATED)


class ProfileApiView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    response_serializer = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        serializer = self.response_serializer(request.user, many=False, context={'request': request})
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        response_serializer = self.response_serializer(instance, many=False, context={'request': request})
        return Response(response_serializer.data)

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        response_serializer = self.response_serializer(instance, many=False, context={'request': request})
        return Response(response_serializer.data)


class UserViewSet(PaginationBreaker, viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter]
    ordering_fields = ['created_at']
    search_fields = ['phone', 'first_name', 'last_name', 'email', 'username']
    permission_classes = (AllowAny,)