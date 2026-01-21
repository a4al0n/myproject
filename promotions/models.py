from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from core.models import Product


class Promotion(models.Model):
    """Акция на товар"""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='promotions',
        verbose_name='Товар'
    )
    title = models.CharField('Название акции', max_length=200)
    description = models.TextField('Описание акции')
    discount_percent = models.DecimalField(
        'Процент скидки',
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    start_date = models.DateTimeField('Дата начала')
    end_date = models.DateTimeField('Дата окончания')
    is_active = models.BooleanField('Активна', default=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} - {self.product.name}'

    @property
    def is_valid(self):
        """Проверка, действует ли акция в данный момент"""
        now = timezone.now()
        return (
            self.is_active and
            self.start_date <= now <= self.end_date
        )

    def save(self, *args, **kwargs):
        """Проверка при сохранении"""
        if self.start_date >= self.end_date:
            raise ValueError('Дата начала должна быть раньше даты окончания')
        super().save(*args, **kwargs)