from .views import BookingViewSet
from rest_framework import routers 
from django.urls import path
router  =  routers.DefaultRouter()
router.register(r'booking', BookingViewSet),
   
urlpatterns = [
    #path('register/', RegisterAPI.as_view(), name='register'),
    ]

urlpatterns += router.urls