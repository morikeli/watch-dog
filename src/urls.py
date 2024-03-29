from django.urls import path, include
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings


urlpatterns = [
    path('auth/', include('accounts.urls')),
    path('', include('core.urls')),
    path('api/', include('api.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
