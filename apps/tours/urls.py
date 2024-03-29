from django.urls import path
from .views import (
    TourList, tourPackageList, BookTour, 
    BookingList, BookingDetail, SubmitPayment
    )

urlpatterns = [
    path("list", TourList.as_view(), name="tourlist"),
    path("<id>/packages", tourPackageList, name="packages"),
    path('book', BookTour.as_view(), name='book-tour'),
    path('bookings', BookingList.as_view(), name='booking-list'),
    path('booking/<pk>/detail', BookingDetail.as_view(), name='booking-detail'),
    path('booking/<pk>/pay', SubmitPayment.as_view() , name="submit-payment"),
]