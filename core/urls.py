from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/videos/', include('videos.urls')),
    path('api-auth/', include('rest_framework.urls')),  # Optional: DRF login/logout
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)