from rest_framework import serializers
from .models import Promotion


class PromotionSerializer(serializers.ModelSerializer):
    """Сериализатор для акций"""
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(
        source='product.price',
        max_digits=10,
        decimal_places=2,
        read_only=True
    )
    is_valid = serializers.BooleanField(read_only=True)

    # Расчет цены со скидкой
    discounted_price = serializers.SerializerMethodField()

    class Meta:
        model = Promotion
        fields = [
            'id', 'product', 'product_name', 'product_price',
            'title', 'description', 'discount_percent',
            'start_date', 'end_date', 'is_active', 'is_valid',
            'discounted_price', 'created_at'
        ]

    def get_discounted_price(self, obj):
        """Вычисление цены со скидкой"""
        original_price = obj.product.price
        discount = original_price * (obj.discount_percent / 100)
        return float(original_price - discount)