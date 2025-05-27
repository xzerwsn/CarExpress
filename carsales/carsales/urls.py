from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mainapp.urls')),  # Используем mainapp вместо cars
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)