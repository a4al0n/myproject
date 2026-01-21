from django.conf import settings


def modules_context(request):
    """
    Добавляет информацию о доступных модулях в контекст шаблонов
    """
    return {
        'modules_config': settings.MODULES_CONFIG,
        'reviews_enabled': settings.MODULES_CONFIG.get('reviews', {}).get('enabled', False),
        'promotions_enabled': settings.MODULES_CONFIG.get('promotions', {}).get('enabled', False),
    }