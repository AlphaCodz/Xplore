from django.urls import path, re_path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from .views import RegisterTourAgency, TokenObtainPairView, AddTour, TourDetail

urlpatterns = [
    path('<int:id>', views.AgencyDetails, name='agencies'),
    path('touragency/register', RegisterTourAgency.as_view(), name="regtouragency"),
    path('login/', TokenObtainPairView.as_view(), name="agencylogin"),
    path('add/tour', AddTour.as_view(), name="addtour"),
    path('tours/<int:pk>/', TourDetail.as_view(), name="tours" ),    
]
 
urlpatterns = format_suffix_patterns(urlpatterns)