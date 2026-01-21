from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]

# Динамическое подключение модулей на основе конфигурации
if settings.MODULES_CONFIG.get('reviews', {}).get('enabled', False):
    urlpatterns.append(path('reviews/', include('reviews.urls')))

if settings.MODULES_CONFIG.get('promotions', {}).get('enabled', False):
    urlpatterns.append(path('promotions/', include('promotions.urls')))

# Статические и медиа файлы
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])