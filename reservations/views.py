# reservations/views.py

from django.shortcuts import render
from django.contrib.auth import authenticate, get_user_model
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .models import Room, Booking
from .serializers import RoomSerializer, UserSerializer, BookingSerializer, ProfileSerializer
from django.db.models import Q, Count
from datetime import datetime
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

# --- Page-serving views ---
def index_view(request): return render(request, 'index.html')
def rooms_view(request): return render(request, 'rooms.html')
def dining_view(request): return render(request, 'dining.html')
def spa_view(request): return render(request, 'spa.html')
def booking_view(request): return render(request, 'booking.html')
def confirmation_view(request): return render(request, 'confirmation.html')
def checkout_view(request): return render(request, 'checkout.html')
def thank_you_view(request): return render(request, 'thank-you.html')
def account_view(request): return render(request, 'account.html')


# --- API VIEWS ---
class SignupView(generics.CreateAPIView):
    serializer_class = UserSerializer

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'username': user.username}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = ProfileSerializer(request.user, context={'request': request})
        return Response(serializer.data)
    def put(self, request):
        user = request.user
        serializer = ProfileSerializer(user, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CheckAvailabilityView(APIView):
    def post(self, request):
        check_in = request.data.get('check_in_date')
        check_out = request.data.get('check_out_date')
        if not check_in or not check_out:
            return Response({'error': 'Please provide both check-in and check-out dates.'}, status=status.HTTP_400_BAD_REQUEST)
        check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
        check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
        conflicting_bookings = Booking.objects.filter(
            Q(check_in_date__lt=check_out_date) & Q(check_out_date__gt=check_in_date)
        )
        booked_room_counts = conflicting_bookings.values('room__id').annotate(count=Count('id'))
        booked_rooms_dict = {item['room__id']: item['count'] for item in booked_room_counts}
        available_rooms = []
        all_rooms = Room.objects.all()
        for room in all_rooms:
            booked_count = booked_rooms_dict.get(room.id, 0)
            if room.quantity > booked_count:
                available_rooms.append(room)
        serializer = RoomSerializer(available_rooms, many=True, context={'request': request})
        return Response(serializer.data)

class CreateBookingView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# --- THIS IS THE CORRECTED BOOKING HISTORY VIEW ---
class BookingHistoryView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookingSerializer

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by('-check_in_date')

    # This new method correctly provides the necessary context to the serializer
    # so it can build the full image URLs.
    def get_serializer_context(self):
        context = super(BookingHistoryView, self).get_serializer_context()
        context.update({"request": self.request})
        return context

class BookingCancelView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk, user=request.user)
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found.'}, status=status.HTTP_404_NOT_FOUND)
        cancellation_deadline = booking.check_in_date - timedelta(days=5)
        if timezone.now().date() > cancellation_deadline:
            return Response({'error': 'This booking is within 5 days and cannot be cancelled online.'}, status=status.HTTP_400_BAD_REQUEST)
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RoomListView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer