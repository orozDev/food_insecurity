from rest_framework import serializers
from core.models import Product, Category, Producer


class ProductSerializer(serializers.ModelSerializer):
    images = serializers.ListSerializer(child=serializers.ImageField())

    class Meta:
        model = Product
        fields = '__all__'

    def create(self, validated_data):
        validated_data.pop('images', None)
        return Product.objects.create(**validated_data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProducerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producer
        fields = '__all__'
