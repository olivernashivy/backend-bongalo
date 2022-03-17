from pyexpat import model
from django.contrib import admin

# Register your models here.
from .models import Booking



class BookingAdmin(admin.ModelAdmin):
    list_display = ('added_by', 'room_type',  'location', 'price')

admin.site.register(Booking, BookingAdmin)