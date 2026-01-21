from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'core'

# REST API роутер
router = DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='product-api')
router.register(r'categories', views.CategoryViewSet, basename='category-api')

# URL паттерны
urlpatterns = [
    # Веб-интерфейс
    path('', views.index, name='index'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('categories/', views.category_list, name='category_list'),
    path('modules/', views.modules_management, name='modules_management'),

    # REST API
    path('api/', include(router.urls)),
]