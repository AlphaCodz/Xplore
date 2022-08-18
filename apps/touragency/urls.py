from django.urls import path
from . import views
from .views import RegisterTourAgency, TokenObtainPairView

urlpatterns = [
    path('agency/<int:id>', views.AgencyDetails, name='agencies'),
    path('touragency/reg', RegisterTourAgency.as_view(), name="regtouragency"),
    path('agency/login/', TokenObtainPairView.as_view(), name="agencylogin")
]
