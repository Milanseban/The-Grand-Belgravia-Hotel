# reservations/models.py
from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    capacity = models.IntegerField()
    quantity = models.IntegerField(default=1)

    @property
    def image_url(self):
        # This maps room names to their respective image files
        image_map = {
            "Junior Suite": 'images/image3.jpeg',
            "Family Room": 'images/image2.jpg',
            "Deluxe King Room": 'images/image1.jpeg'
        }
        return image_map.get(self.name)

    def __str__(self):
        return self.name


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    guest_name = models.CharField(max_length=255, null=True, blank=True)
    guest_email = models.EmailField(null=True, blank=True)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    guests = models.IntegerField()
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user:
            return f'Booking for {self.room.name} by {self.user.username}'
        else:
            return f'Guest Booking for {self.room.name} by {self.guest_email}'