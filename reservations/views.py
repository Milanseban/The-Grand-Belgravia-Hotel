from django.shortcuts import render
from django.contrib.auth import authenticate, get_user_model
from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import Room, Booking
from .serializers import RoomSerializer, UserSerializer, BookingSerializer, ProfileSerializer
from django.db.models import Q, Count
from datetime import datetime
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

def index_view(request): return render(request, 'index.html')
def rooms_view(request): return render(request, 'rooms.html')
def dining_view(request): return render(request, 'dining.html')
def spa_view(request): return render(request, 'spa.html')
def booking_view(request): return render(request, 'booking.html')
def confirmation_view(request): return render(request, 'confirmation.html')
def checkout_view(request): return render(request, 'checkout.html')
def thank_you_view(request): return render(request, 'thank-you.html')
def account_view(request): return render(request, 'account.html')

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
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
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
            return Response({'error': 'Please provide dates.'}, status=status.HTTP_400_BAD_REQUEST)
        check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date()
        check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date()
        conflicting_bookings = Booking.objects.filter(check_in_date__lt=check_out_date, check_out_date__gt=check_in_date)
        booked_counts = conflicting_bookings.values('room_id').annotate(count=Count('room_id'))
        booked_dict = {item['room_id']: item['count'] for item in booked_counts}
        available_rooms = [room for room in Room.objects.all() if room.quantity > booked_dict.get(room.id, 0)]
        serializer = RoomSerializer(available_rooms, many=True, context={'request': request})
        return Response(serializer.data)

class CreateBookingView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = BookingSerializer
    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
        else:
            serializer.save()

class BookingHistoryView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BookingSerializer
    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user).order_by('-check_in_date')
    def get_serializer_context(self):
        return {'request': self.request}

class BookingCancelView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk, user=request.user)
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found.'}, status=status.HTTP_404_NOT_FOUND)
        cancellation_deadline = booking.check_in_date - timedelta(days=5)
        if timezone.now().date() > cancellation_deadline:
            return Response({'error': 'This booking cannot be cancelled online.'}, status=status.HTTP_400_BAD_REQUEST)
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RoomListView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer