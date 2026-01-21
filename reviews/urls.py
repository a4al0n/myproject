from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'reviews'

# REST API роутер
router = DefaultRouter()
router.register(r'api', views.ReviewViewSet, basename='review-api')

# URL паттерны
urlpatterns = [
    # Веб-интерфейс
    path('', views.review_list, name='review_list'),
    path('product/<int:product_id>/', views.product_reviews, name='product_reviews'),
    path('add/<int:product_id>/', views.add_review, name='add_review'),

    # REST API
    path('', include(router.urls)),
]