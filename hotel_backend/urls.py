from django.contrib import admin
from django.urls import path, include
from reservations.views import index_view
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index_view, name='home'),
    path('admin/', admin.site.urls),
    path('', include('reservations.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)