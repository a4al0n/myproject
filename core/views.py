from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets, permissions
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


# Веб-интерфейс
def index(request):
    """Главная страница"""
    products = Product.objects.filter(available=True)[:8]
    categories = Category.objects.all()
    return render(request, 'core/index.html', {
        'products': products,
        'categories': categories
    })


def product_list(request):
    """Список товаров"""
    products = Product.objects.filter(available=True)
    category_id = request.GET.get('category')

    if category_id:
        products = products.filter(category_id=category_id)

    categories = Category.objects.all()
    return render(request, 'core/product_list.html', {
        'products': products,
        'categories': categories
    })


def product_detail(request, product_id):
    """Детальная страница товара"""
    product = get_object_or_404(Product, id=product_id)

    # Получаем связанные данные из модулей, если они включены
    context = {'product': product}

    try:
        from reviews.models import Review
        reviews = Review.objects.filter(product=product).select_related('user')
        context['reviews'] = reviews
        context['reviews_enabled'] = True
    except:
        context['reviews_enabled'] = False

    try:
        from promotions.models import Promotion
        from django.utils import timezone
        now = timezone.now()
        promotions = Promotion.objects.filter(
            product=product,
            is_active=True,
            start_date__lte=now,
            end_date__gte=now
        )
        context['promotions'] = promotions
        context['promotions_enabled'] = True
    except:
        context['promotions_enabled'] = False

    return render(request, 'core/product_detail.html', context)


def category_list(request):
    """Список категорий"""
    categories = Category.objects.all()
    return render(request, 'core/category_list.html', {'categories': categories})


def modules_management(request):
    """Страница управления модулями"""
    from django.conf import settings
    return render(request, 'core/modules_management.html', {
        'modules': settings.MODULES_CONFIG
    })


# REST API
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """API для товаров"""
    queryset = Product.objects.filter(available=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """API для категорий"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]