from django.urls import path, re_path
from .views import (
    TourList, tourPackageList, BookTour, 
    BookingList, BookingDetail, SubmitPayment, TourListView
    )

urlpatterns = [
    path("list", TourList.as_view(), name="tourlist"),
    path("<id>/packages", tourPackageList, name="packages"),
    path('book', BookTour.as_view(), name='book-tour'),
    path('bookings', BookingList.as_view(), name='booking-list'),
    path('booking/<pk>/detail', BookingDetail.as_view(), name='booking-detail'),
    path('booking/<pk>/pay', SubmitPayment.as_view() , name="submit-payment"),
    re_path(r'$', TourListView.as_view(), name="agents" )
]
