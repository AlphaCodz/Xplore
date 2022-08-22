from django.urls import path, re_path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from .views import RegisterTourAgency, TokenObtainPairView, AddTour, TourDetail, all_bookings

urlpatterns = [
    path('<int:id>', views.AgencyDetails, name='agencies'),
    path('reg/', RegisterTourAgency.as_view(), name="regtouragency"),
    path('login/', TokenObtainPairView.as_view(), name="agencylogin"),
    path('add/tour', AddTour.as_view(), name="addTour"),
    path('tours/<int:pk>/', TourDetail.as_view(), name="tours" ),    
     path('all-bookings/<status>', views.all_bookings, name='all-bookings'),
]
 
urlpatterns = format_suffix_patterns(urlpatterns)