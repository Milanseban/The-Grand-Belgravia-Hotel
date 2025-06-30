# reservations/serializers.py

from rest_framework import serializers
from .models import Room, Booking
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    # ... (this class is unchanged)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    # ... (this class is unchanged)
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    username = serializers.CharField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ['username', 'email']

    def update(self, instance, validated_data):
        # ... (this method is unchanged)
        return instance


# --- THIS IS THE FINAL, CORRECTED ROOM SERIALIZER ---
class RoomSerializer(serializers.ModelSerializer):
    # This new field will generate the full image URL automatically
    image_full_url = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ['id', 'name', 'description', 'price_per_night', 'capacity', 'quantity', 'image_full_url']

    def get_image_full_url(self, obj):
        request = self.context.get('request')

        # This is a map of web URLs for rooms that don't have a local image
        unsplash_map = {
            "Deluxe King Room": "https://images.unsplash.com/photo-1596394516093-501ba68a0ba6?q=80&w=2070",
            "Executive Suite": "https://images.unsplash.com/photo-1618773928121-c32242e63f39?q=80&w=2070",
            "The Belgravia Penthouse": "https://images.unsplash.com/photo-1611892440504-42a792e24d32?q=80&w=2070"
        }

        # First, check if there is a local image path from the model's property
        local_image_path = obj.image_url
        if local_image_path:
            if request is None:
                return ""
            return request.build_absolute_uri(f'/static/{local_image_path}')

        # If no local path, fall back to the Unsplash map
        return unsplash_map.get(obj.name, "")


class BookingSerializer(serializers.ModelSerializer):
    room = RoomSerializer(read_only=True)
    room_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'user', 'room', 'room_id', 'check_in_date', 'check_out_date', 'guests', 'booking_date']
        read_only_fields = ['user', 'booking_date']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # This is the crucial line that passes the 'request' context to the RoomSerializer
        representation['room'] = RoomSerializer(instance.room, context=self.context).data
        return representation