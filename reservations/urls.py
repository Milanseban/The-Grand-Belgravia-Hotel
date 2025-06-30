# reservations/urls.py

from django.urls import path
from .views import *

urlpatterns = [
    # --- API Endpoints ---
    path('api/signup/', SignupView.as_view(), name='signup'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/profile/', ProfileView.as_view(), name='profile'),
    path('api/rooms/', RoomListView.as_view(), name='room-list-api'),
    path('api/check-availability/', CheckAvailabilityView.as_view(), name='check-availability'),
    path('api/bookings/create/', CreateBookingView.as_view(), name='create-booking'),
    path('api/my-bookings/', BookingHistoryView.as_view(), name='my-bookings'),
    path('api/bookings/<int:pk>/cancel/', BookingCancelView.as_view(), name='cancel-booking'), # <-- ADD THIS LINE

    # --- Page-serving URLs ---
    path('rooms/', rooms_view, name='rooms'),
    path('dining/', dining_view, name='dining'),
    path('spa/', spa_view, name='spa'),
    path('booking/', booking_view, name='booking'),
    path('confirmation/', confirmation_view, name='confirmation'),
    path('checkout/', checkout_view, name='checkout'),
    path('thank-you/', thank_you_view, name='thank-you'),
    path('account/', account_view, name='account'),
]