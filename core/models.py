from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """Категория товаров"""
    name = models.CharField('Название', max_length=200)
    slug = models.SlugField('URL', unique=True)
    description = models.TextField('Описание', blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    """Товар"""
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Категория'
    )
    name = models.CharField('Название', max_length=200)
    slug = models.SlugField('URL', unique=True)
    description = models.TextField('Описание')
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    image = models.ImageField('Изображение', upload_to='products/', blank=True, null=True)
    stock = models.PositiveIntegerField('Количество на складе', default=0)
    available = models.BooleanField('Доступен', default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def average_rating(self):
        """Средний рейтинг товара из отзывов"""
        try:
            from reviews.models import Review
            reviews = Review.objects.filter(product=self)
            if reviews.exists():
                return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        except:
            pass
        return None

    @property
    def active_promotion(self):
        """Активная акция на товар"""
        try:
            from promotions.models import Promotion
            from django.utils import timezone
            promotion = Promotion.objects.filter(
                product=self,
                is_active=True,
                start_date__lte=timezone.now(),
                end_date__gte=timezone.now()
            ).first()
            return promotion
        except:
            pass
        return None

    @property
    def discounted_price(self):
        """Цена со скидкой если есть акция"""
        promotion = self.active_promotion
        if promotion:
            discount = self.price * (promotion.discount_percent / 100)
            return self.price - discount
        return self.price