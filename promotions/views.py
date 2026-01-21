from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Promotion
from core.models import Product
from .serializers import PromotionSerializer


# Веб-интерфейс
def promotion_list(request):
    """Список всех активных акций"""
    now = timezone.now()
    promotions = Promotion.objects.filter(
        is_active=True,
        start_date__lte=now,
        end_date__gte=now
    ).select_related('product')
    return render(request, 'promotions/promotion_list.html', {'promotions': promotions})


def promotion_detail(request, promotion_id):
    """Детали акции"""
    promotion = get_object_or_404(Promotion, id=promotion_id)
    return render(request, 'promotions/promotion_detail.html', {'promotion': promotion})


def product_promotions(request, product_id):
    """Акции для конкретного товара"""
    product = get_object_or_404(Product, id=product_id)
    now = timezone.now()
    promotions = Promotion.objects.filter(
        product=product,
        is_active=True,
        start_date__lte=now,
        end_date__gte=now
    )
    return render(request, 'promotions/product_promotions.html', {
        'product': product,
        'promotions': promotions
    })


# REST API
class PromotionViewSet(viewsets.ReadOnlyModelViewSet):
    """API для просмотра акций (только чтение)"""
    queryset = Promotion.objects.select_related('product').all()
    serializer_class = PromotionSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """Фильтрация по активным акциям"""
        queryset = super().get_queryset()
        active_only = self.request.query_params.get('active', 'false')

        if active_only.lower() == 'true':
            now = timezone.now()
            queryset = queryset.filter(
                is_active=True,
                start_date__lte=now,
                end_date__gte=now
            )

        return queryset

    @action(detail=False, methods=['get'])
    def by_product(self, request):
        """Получить акции для конкретного товара"""
        product_id = request.query_params.get('product_id')
        if product_id:
            now = timezone.now()
            promotions = self.queryset.filter(
                product_id=product_id,
                is_active=True,
                start_date__lte=now,
                end_date__gte=now
            )
            serializer = self.get_serializer(promotions, many=True)
            return Response(serializer.data)
        return Response({'error': 'product_id is required'}, status=400)

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Получить предстоящие акции"""
        now = timezone.now()
        promotions = self.queryset.filter(
            is_active=True,
            start_date__gt=now
        ).order_by('start_date')
        serializer = self.get_serializer(promotions, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def expired(self, request):
        """Получить завершившиеся акции"""
        now = timezone.now()
        promotions = self.queryset.filter(
            end_date__lt=now
        ).order_by('-end_date')
        serializer = self.get_serializer(promotions, many=True)
        return Response(serializer.data)