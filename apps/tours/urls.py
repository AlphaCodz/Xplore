from django.urls import path
from .views import TourList, tourPackageList, BookTour

urlpatterns = [
    path("list", TourList.as_view(), name="tourlist"),
    path("<id>/packages", tourPackageList, name="touragents"),
    path('book', BookTour.as_view(), name='book-tour')
]