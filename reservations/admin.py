# reservations/admin.py

from django.contrib import admin
from .models import Room, Booking

# This is the line that was missing.
# It tells Django to show the Room and Booking models in the admin panel.
admin.site.register(Room)
admin.site.register(Booking)