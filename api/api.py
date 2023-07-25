from rest_framework import viewsets, filters, status
from api.paginations import StandardResultsSetPagination
from api.mixins import PaginationBreaker, PermissionByAction
from django_filters.rest_framework import DjangoFilterBackend
from django.core.files.storage import FileSystemStorage
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from api.permissions import IsOwner, IsAdmin, IsOwnerProducer
from api.serializers import ProductSerializer, CategorySerializer, ProducerSerializer
from core.models import Product, ProductImages, Category, Producer


class ProductViewSet(PaginationBreaker, PermissionByAction, viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.OrderingFilter,
                       filters.SearchFilter]
    filterset_fields = ['producer', 'is_published']
    search_fields = ['name', 'content']
    ordering_fields = ['price', 'rating']
    permission_classes = {
        'create': [IsAuthenticated],
        'list': [AllowAny],
        'update': [IsAuthenticated, IsOwner],
        'retrieve': [AllowAny],
        'destroy': [IsAuthenticated, IsOwner],
    }
    pagination_class = StandardResultsSetPagination

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        headers = self.get_success_headers(serializer.data)
        newsImageSystem = FileSystemStorage('media/product_images/')
        for image in request.data.get('images', []):
            newsImageSystem.save(image.name, image)
            ProductImages.objects.create(product=product, image=image)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CategoryViewSet(PaginationBreaker, PermissionByAction, viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = {
        'create': [IsAuthenticated, IsAdmin],
        'list': [AllowAny],
        'update': [IsAuthenticated, IsAdmin],
        'retrieve': [AllowAny],
        'destroy': [IsAuthenticated, IsAdmin],
    }
    pagination_class = StandardResultsSetPagination


class ProducerViewSet(PaginationBreaker, PermissionByAction, viewsets.ModelViewSet):
    queryset = Producer.objects.all()
    serializer_class = ProducerSerializer
    permission_classes = {
        'create': [IsAuthenticated],
        'list': [AllowAny],
        'update': [IsAuthenticated, IsOwnerProducer],
        'retrieve': [AllowAny],
        'destroy': [IsAuthenticated, IsAdmin, IsOwnerProducer],
    }
    pagination_class = StandardResultsSetPagination
