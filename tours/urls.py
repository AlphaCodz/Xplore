from django.urls import path
from .views import TourList, tourPackageList

urlpatterns = [
    path("list", TourList.as_view(), name="tourlist"),
    path("<id>/packages", tourPackageList, name="touragents"),
]