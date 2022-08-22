from django.urls import path, re_path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from .views import RegisterTourAgency, AddTour, TourDetail, approve_booking

urlpatterns = [
    path('<int:id>', views.AgencyDetails, name='agencies'),
    path('touragency/register', RegisterTourAgency.as_view(), name="regtouragency"),
    path('add/tour', AddTour.as_view(), name="addtour"),
    path('tours/<int:pk>', TourDetail.as_view(), name="tours" ),    
    path('all_bookings/<status>', views.all_bookings, name="bookings"),
    path('approve/<int:pk>', approve_booking, name="approve-booking"),
]
 
urlpatterns = format_suffix_patterns(urlpatterns)