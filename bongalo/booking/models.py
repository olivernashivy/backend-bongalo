from django.db import models
# Create your models here.
class Booking(models.Model):
    # apartment,secondary unity, unique space
    added_by = models.ForeignKey('users.User', null=True, blank=True, related_name="booking_added", on_delete=models.SET_NULL)
    room_type = models.CharField(max_length=80, blank=True, null= True)
    number_of_guests  = models.CharField(default="1", max_length=70)
    location = models.CharField(max_length=80, blank=True, null= True)
    guests = models.IntegerField(default=1, blank=True, null= True)
    beds = models.IntegerField(default=1, blank=True, null= True)
    bedrooms = models.IntegerField(default=1, blank=True, null= True)
    price = models.IntegerField(default=0)
    country = models.CharField(max_length=140,null=True, blank=True)
    street = models.CharField(max_length=140,null=True, blank=True)
    suite_code = models.CharField(max_length=140,null=True, blank=True)
    ammenities = models.TextField(null=True, blank=True)
    facilities = models.TextField(null=True, blank=True)
    house_rules = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'booking by {self.added_by}'
