# hotel_backend/urls.py

from django.contrib import admin
from django.urls import path, include
from reservations.views import index_view
from django.conf import settings             # <-- ADD THIS IMPORT
from django.conf.urls.static import static # <-- ADD THIS IMPORT

urlpatterns = [
    path('', index_view, name='home'),
    path('admin/', admin.site.urls),
    path('', include('reservations.urls')),
]

# --- THIS IS THE CRUCIAL PART THAT WAS MISSING ---
# This line tells Django to serve static files (like your images)
# during development (when DEBUG is True).
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)