from rest_framework import serializers
from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий"""

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'created_at']


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор для товаров"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    discounted_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        read_only=True
    )

    class Meta:
        model = Product
        fields = [
            'id', 'category', 'category_name', 'name', 'slug',
            'description', 'price', 'discounted_price', 'image',
            'stock', 'available', 'average_rating',
            'created_at', 'updated_at'
        ]