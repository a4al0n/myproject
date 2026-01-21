from django.contrib import admin
from .models import Promotion


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ['title', 'product', 'discount_percent', 'start_date', 'end_date', 'is_active']
    list_filter = ['is_active', 'start_date', 'end_date']
    search_fields = ['title', 'description', 'product__name']
    list_editable = ['is_active']
    date_hierarchy = 'start_date'
    readonly_fields = ['created_at']