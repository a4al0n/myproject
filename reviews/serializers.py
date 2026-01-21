from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для отзывов"""
    user_username = serializers.CharField(source='user.username', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'user', 'user_username', 'product', 'product_name',
            'text', 'rating', 'created_at', 'updated_at'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']

    def validate_rating(self, value):
        """Валидация рейтинга"""
        if value < 1 or value > 5:
            raise serializers.ValidationError('Рейтинг должен быть от 1 до 5')
        return value