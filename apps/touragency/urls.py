from django.urls import path, re_path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from .views import RegisterTourAgency, AddTour, TourDetail, approve_booking, decline_booking, GenerateToken, Agents

urlpatterns = [
    path('<int:id>', views.AgencyDetails, name='agencies'),
    path('touragency/register', RegisterTourAgency.as_view(), name="regtouragency"),
    path('add/tour', AddTour.as_view(), name="addtour"),
    path('tours/<int:pk>', TourDetail.as_view(), name="tours" ),    
    path('all_bookings/<status>', views.all_bookings, name="bookings"),
    path('approve/<int:pk>', views.approve_booking, name="approve-booking"),
    path('decline/<int:pk>', views.decline_booking, name="decline-booking"),
    path('generate/token', views.GenerateToken, name="token"),
    path('agent/<pk>', views.Agents, name="agent")
    
]
 
urlpatterns = format_suffix_patterns(urlpatterns)