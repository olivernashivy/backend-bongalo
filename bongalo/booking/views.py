from .serializers import BookingSerializer
from rest_framework import viewsets, mixins, filters
from .models import Booking

class BookingViewSet(  
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer