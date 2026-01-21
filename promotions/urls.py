from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'promotions'

# REST API роутер
router = DefaultRouter()
router.register(r'api', views.PromotionViewSet, basename='promotion-api')

# URL паттерны
urlpatterns = [
    # Веб-интерфейс
    path('', views.promotion_list, name='promotion_list'),
    path('<int:promotion_id>/', views.promotion_detail, name='promotion_detail'),
    path('product/<int:product_id>/', views.product_promotions, name='product_promotions'),

    # REST API
    path('', include(router.urls)),
]