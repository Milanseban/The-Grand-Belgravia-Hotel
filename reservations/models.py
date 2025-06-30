# reservations/models.py

from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    capacity = models.IntegerField()
    quantity = models.IntegerField(default=1)

    # THIS IS THE CORRECTED PROPERTY
    @property
    def image_url(self):
        # This now only returns the simple, relative path for local images
        # We will add the full Unsplash URLs in the serializer
        image_map = {
            "Junior Suite":           'images/image3.jpg',
            "Family Room":            'images/image2.jpg',
            # We add all our known local images here
        }
        return image_map.get(self.name) # Returns the path, or None if not a local image

    def __str__(self):
        return self.name

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    guests = models.IntegerField()
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Booking for {self.room.name} by {self.user.username}'