from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Review
from core.models import Product
from .serializers import ReviewSerializer


# Веб-интерфейс
def review_list(request):
    """Список всех отзывов"""
    reviews = Review.objects.select_related('user', 'product').all()
    return render(request, 'reviews/review_list.html', {'reviews': reviews})


def product_reviews(request, product_id):
    """Отзывы для конкретного товара"""
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product).select_related('user')
    return render(request, 'reviews/product_reviews.html', {
        'product': product,
        'reviews': reviews
    })


@login_required
def add_review(request, product_id):
    """Добавление отзыва"""
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        text = request.POST.get('text')
        rating = request.POST.get('rating')

        if text and rating:
            try:
                Review.objects.update_or_create(
                    user=request.user,
                    product=product,
                    defaults={'text': text, 'rating': int(rating)}
                )
                messages.success(request, 'Отзыв успешно добавлен!')
                return redirect('reviews:product_reviews', product_id=product.id)
            except Exception as e:
                messages.error(request, f'Ошибка при добавлении отзыва: {e}')
        else:
            messages.error(request, 'Заполните все поля!')

    return render(request, 'reviews/add_review.html', {'product': product})


# REST API
class ReviewViewSet(viewsets.ModelViewSet):
    """API для работы с отзывами"""
    queryset = Review.objects.select_related('user', 'product').all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def by_product(self, request):
        """Получить отзывы для конкретного товара"""
        product_id = request.query_params.get('product_id')
        if product_id:
            reviews = self.queryset.filter(product_id=product_id)
            serializer = self.get_serializer(reviews, many=True)
            return Response(serializer.data)
        return Response({'error': 'product_id is required'}, status=400)

    @action(detail=False, methods=['get'])
    def my_reviews(self, request):
        """Получить отзывы текущего пользователя"""
        if request.user.is_authenticated:
            reviews = self.queryset.filter(user=request.user)
            serializer = self.get_serializer(reviews, many=True)
            return Response(serializer.data)
        return Response({'error': 'Authentication required'}, status=401)